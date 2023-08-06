"""enables scripts to remember parameter input values between invocations

It can be useful to have scripts that remember their parameters from
one invocation to the next. The package enables such a facility by
storage and retrieval of parameter values in disk files. It provides a
way to define named parameters, default values and ranges, and allows
parameters to be hidden by default if need be. It is also designed for
the case of a set of scripts sharing a common purpose, e.g. to aid
analysis of a specific type of data perhaps. In such a case, being able
to share parameter values, e.g. the name of a particular dataset,
between scripts can be very helpful.

Here is an example in which three parameters are prompted for ('device',
'npoint', 'output'). 'device' is hidden by default. The values input
by the user will be stored in a file located in a directory pointed to
by environment variable 'COMM_EG_ENV', or, if that is undefined, in a
sub-directory of the home directory called '.comm_eg'. The key class that
does most of the work is :class:`trm.cline.Cline`. It's invoked as a
context manager so that on any interruption of execution it tidies up properly
and save the parameters to disk::

  >> from trm import cline
  >> from trm.cline import Cline
  >>
  >> # get command name and arguments [extracted from sys.argv
  >> # in this instance]
  >> command, args = cline.script_args()
  >>
  >> # invoke Cline as a context manager
  >> with Cline('COMM_EG_ENV', '.comm_eg', commad, args) as cl:
  >>
  >>   # register the parameter names and properties
  >>   # 'device' is GLOBAL meaning it can be shared
  >>   # with other scripts.
  >>   cl.register('device', Cline.GLOBAL, Cline.HIDE)
  >>   cl.register('npoint', Cline.LOCAL, Cline.PROMPT)
  >>   cl.register('output', Cline.LOCAL, Cline.PROMPT)
  >>
  >>   # get their values [string, integer, string]
  >>   device = cl.get_value('device', 'plot device', 'terminal')
  >>   npoint = cl.get_value('npoint', 'number of points', 10, 1, 100)
  >>   output = cl.get_value('output', 'output file', 'save.dat')
  >>
  >> # Leave the context manager; rest of program follows
  >> print(device,npoint,output)

If this is invoked in a script called 'script.py' then the following
are all ways to invoke it:

script.py<cr>
script.py device=plot.png npoint=20<cr>
script.py device=plot.png \\<cr>
script.py 25<cr>
script.py prompt list<cr>

The first would prompt for 'npoint' and 'output'; the second for just
'output'; the third would not prompt for any of them; the fourth would
set npoint=25, and device='plot.png' from the earlier invocations; the
fifth would prompt for all parameters and list all values input.

The "LOCAL" and "GLOBAL" you will see above control where the
parameter value is stored. If "GLOBAL" then the parameter is stored in
a file that might also be accessed by other scripts, allowing parameters
to be shared by more than one script. "LOCAL" means store in a file
specific to the actual script.

"HIDE" and "PROMPT" control whether a parameter is prompted by
default.  A special keyword 'prompt' (see next) is needed to reveal a
hidden parameter, although such parameters can also be set from the
the command line if explicitly named.

A number of special keyword arguments can be used on the command line.
They are::

  list : lists all the parameter values used

  nodefs : bypasses any attempt to read or write the default files.  It is
      provided as a way to avoid clashes between multiple processes.

  prompt : forces prompting for all variables not supplied via the argument
      list passed on creation of Cline objects.

When you get prompting, <tab> allows you to complete
filenames. Entering '?'  gives the parameter range if any has been
supplied.

When 'npoint' was prompted above, a default value [1], and a minimum
and maximum [1 and 10] were supplied. If npoint is not given on the
command line, then it would be prompted in the form:

  npoint - number of points [10]: <user input here>

If '25' was entered, then next time round, you would get

  npoint - number of points [25]: <user input here>

Hitting <CR> as the input would retain the '25', hence the script
"remembers" old values which appears as the new default choice, saving
a lot of typing.

File name prompts can be simply as a string as in the example above,
but there is a also special class, :class:`trm.cline.Fname`, which
helps check on the existence of files if need be. A script prompting
for one (pre-existing) filename might start with::

  >> from trm import cline
  >> from trm.cline import Cline
  >>
  >> command, args = cline.script_args()
  >>
  >> with cline.Cline('COMM_EG_ENV', '.comm_eg', commad, args) as cl:
  >>    cl.register('fname', Cline.LOCAL, Cline.PROMPT)
  >>    fname = cl.get_value(
  >>       'fname', 'name of text file',
  >>       cline.Fname("file.txt", ".txt")
  >>    )

This would enforce the extension ".txt" so that you could type "file"
and it would be assumed to be "file.txt".

See :func:`trm.cline.Cline.get_value` for supported data types for input
which include standard numerical data types, strings, lists, tuples and
a special type :class:`trm.cline.Fname` for file input.

.. Note::

   It is possible on rare occasions to corrupt the disk files where
   the parameter values are stored. In such cases, navigate to the
   directory where they are stored (e.g. the one pointed at by
   COMM_EG_ENV or $HOME/.comm_eg if the environment variable does not
   exist and delete the files you find there. This resets all
   parameters to their starting defaults.

"""

import os
import re
import sys
import pickle
import warnings
import signal
from collections import OrderedDict

# next two lines allow tab completion of file names
import readline
readline.parse_and_bind("tab: complete")

# def complete(text,state):
#    results = ["example",None]
#    return results[state]

# readline.set_completer(complete)

def add_extension(fname, ext):
    """Add an extension ext to a file name if it is not already there, and
    returns the revised name. e.g. if fname='datafile' and ext='.dat', this
    returns 'datafile.dat'. If fname='datafile.dat', it still returns just
    'datafile.dat'.

    See: sub_extension
    """
    if len(ext) and not fname.endswith(ext):
        return f"{fname}{ext}"
    else:
        return fname

def sub_extension(fname, ext):
    """Strips the extension 'ext' from a file name if it is present, and
    returns the revised name. i.e. fname='datafile.dat', ext='.dat'
    returns 'datafile'.

    See: add_extension

    """
    if fname.endswith(ext):
        return fname[:-len(ext)]
    else:
        return fname

def clist(command):
    """Splits up a command string returning a list suitable for
    constructing Cline objects. The reason for using this rather than
    a simple string split is that it allows you to use double quotes
    to get strings with spaces through. Returns a list of strings.

    e.g. You can pass it a string like

    '120 "IP Peg" name=me 43.5'

    which will become a list:

    ['120','IP Peg','name=me','43.5']

    """

    cl = re.findall('"[^"]*"|\S+', command)
    return [c.lstrip('"').rstrip('"') for c in cl]

def script_args(args=None):
    """This is a small helper method to use at the start of an entry
    point script.

    If 'args' is None on entry, it is replaced by 'sys.argv'. It is
    then assumed that the first argument is the command name or else
    None. The command name argument is removed from args, and if not
    None, converted to just the file part of the path. It is then
    returned along with the remaining list of arguments in a two
    element tuple, i.e. (commands, args).

    """
    if args is None:
        args = sys.argv.copy()

    command = args.pop(0)
    if command is not None:
        # just keep filename part, not any path
        command = os.path.split(command)[1]

    return (command, args)

class Cline:

    """Class to handle command line inputs. In particular this allows
    storage and retrieval of input parameter values from files which
    allows different scripts to communicate parameters to each other
    through 'global' defaults, and commands to have a 'memory' between
    different invocations. To use the class you first create an
    instance, then register each parameter name, and finally get the
    input, either from the user, default values or disk. Cline can be
    (and is best) invoked as a context manager with "with". This
    saves the values when it goes out of context, which includes when
    a script is aborted during parameter entry.

    :class:`Cline` objects define the four static variables GLOBAL, LOCAL,
    PROMPT, HIDE which should be used when registering parameters to define
    their properties

    """

    # All attributes are hidden, so not publicly documented. They are::
    #
    #    _ddir    -- name of defaults directory (string)
    #    _lname   -- name of local defaults file (string)
    #    _gname   -- name of global defaults file (string)
    #    _lpars   -- parameters loaded from local default file (dict)
    #    _gpars   -- parameters loaded from global default file (dict)
    #    _cname   -- command name (string)
    #    _pbynam  -- parameter/value pairs read from arguments (dict)
    #    _pbypos  -- parameter values by position read from arguments (list)
    #    _rpars   -- Registered parameters, keyed on the parameter name.
    #                For each one a dictionary specifies whether they are
    #                to be found in the global or local default and whether
    #                they should be prompted for or not (OrderedDict)
    #    _prompt  -- force prompting or not (bool)
    #    _list    -- list the parameter name / value pairs or not (bool)
    #    _nodefs  -- controls whether disk default files will be accessed or not
    #                (True ==> no access) (bool)
    #    _usedef  -- use default rather than prompt from user. (bool)

    GLOBAL = 1
    LOCAL = 2
    PROMPT = 3
    HIDE = 4

    def __init__(self, direnv, defdir, cname, args):
        """Initialize an Cline class object

        Arguments::

           direnv : str
              environment variable pointing at a directory where
              default files will be stored.

           defdir : str
              default directory (sub-directory of HOME) if the
              enviroment variable 'direnv' is not defined

           cname : str
              the command name, which is used to generate the local
              defaults file name. If cname=None, no attempt to read or
              save defaults will be made. This allows the programmatic
              equivalent of entering 'nodefs' on the command line.

           args : list of str
              command-line arguments. The first one must be the
              command name. Their order must match the order in which
              the parameters are prompted.

        """

        # Extract special keywords 'nodefs', 'prompt' and 'list' from
        # argument list, and set flags.

        if "nodefs" in args:
            self._nodefs = True
            args = [arg for arg in args if arg != "nodefs"]
        else:
            self._nodefs = False

        if "prompt" in args:
            self._prompt = True
            args = [arg for arg in args if arg != "prompt"]
        else:
            self._prompt = False

        if "list" in args:
            self._list = True
            args = [arg for arg in args if arg != "list"]
        else:
            self._list = False

        # Store the command name
        self._cname = cname
        if self._list:
            if self._cname is not None:
                print("\n" + self._cname)
            else:
                print("\nNone")

        if not self._nodefs and self._cname is not None:

            if direnv is None and defdir is None:
                raise ClineError(
                    "no default file environment variable"
                    " or directory name supplied"
                )

            if direnv is not None and direnv in os.environ:
                self._ddir = os.environ[direnv]
            else:
                home = os.environ["HOME"]
                self._ddir = os.path.join(home, defdir)

            # read local and global default files
            self._lname = os.path.join(self._ddir, self._cname + ".def")
            try:
                with open(self._lname, "rb") as flocal:
                    self._lpars = pickle.load(flocal)
            except IOError:
                self._lpars = {}
            except (EOFError, pickle.UnpicklingError):
                warnings.warn(
                    f"""
Failed to read local defaults file {self._lname}; possible corrupted
file. Defaults local to this command will be reset. Re-run it with
'prompt' on the commandline in case hidden parameters have changed
their values.""", ClineWarning,
                )
                self._lpars = {}

            self._gname = os.path.join(self._ddir, "GLOBAL.def")
            try:
                with open(self._gname, "rb") as fglobal:
                    self._gpars = pickle.load(fglobal)
            except IOError:
                self._gpars = {}
            except (EOFError, pickle.UnpicklingError):
                warnings.warn(
                    f"""
failed to read global defaults file {self._gname}; possible corrupted
file. The global defaults will be reset. This comand and others may
have altered 'hidden' parameter values. Re-run with 'prompt' on the
command line to check.""", ClineWarning,
                )
                self._gpars = {}
        else:
            self._ddir = None
            self._lpars = {}
            self._gpars = {}

        # _pbynam and _pbypos are a dictionary of parameters defined by name
        # and a list of parameters defined by position sent in through the
        # command line arguments
        self._pbynam = {}
        self._pbypos = []

        # defines allowable parameter names
        checker = re.compile("^[a-zA-Z0-9]+=")

        for arg in args:
            if checker.match(arg):
                p, v = arg.split("=", 1)
                if p in self._pbynam:
                    raise ClineError(
                        "parameter = " + p +
                        " defined more than once in argument list."
                    )
                self._pbynam[p] = v
            else:
                self._pbypos.append(arg)

        self._rpars = OrderedDict()
        self.narg = 0
        self._usedef = False

    def list(self):
        """Returns with a list of strings listing all the parameter names and
        values separated by carriage returns. Unset parameters are
        skipped.

        """

        nc = 1
        for param in self._rpars:
            nc = max(nc, len(param))

        slist = []
        for param, info in self._rpars.items():
            # get value
            if info["g_or_l"] == Cline.GLOBAL:
                if param not in self._gpars:
                    continue
                value = self._gpars[param]
            else:
                if param not in self._lpars:
                    continue
                value = self._lpars[param]

            # write out
            slist.append("{:{:d}s} = {!s}\n".format(param, nc, value))
        return slist

    def save(self):
        """Saves parameter values to disk (if 'nodefs' has not been
        specified). Call when the final parameter has been specified.

        """

        if not self._nodefs and self._cname is not None:

            # make the default directory if need be
            try:
                if not os.path.lexists(self._ddir):
                    os.mkdir(self._ddir, 0o755)
            except OSError:
                warnings.warn(
                    "failed to create defaults directory " + self._ddir + "\n",
                    ClineWarning,
                )
            except AttributeError:
                warnings.warn(
                    "defaults directory attribute undefined;"
                    " possible programming error\n",
                    ClineWarning,
                )

            # ignore ctrl-C during writing of default files to reduce
            # chance of corruption
            signal.signal(signal.SIGINT, signal.SIG_IGN)

            # save local defaults
            try:
                with open(self._lname, "wb") as flocal:
                    pickle.dump(self._lpars, flocal)
            except (IOError, TypeError):
                warnings.warn(
                    "failed to save local parameter/value pairs to "
                    + self._lname
                    + "\n",
                    ClineWarning,
                )
            except AttributeError:
                warnings.warn(
                    "local parameter file attribute undefined;"
                    " possible programming error\n",
                    ClineWarning,
                )

            # save global defaults
            try:
                with open(self._gname, "wb") as fglobal:
                    pickle.dump(self._gpars, fglobal)
            except (IOError, TypeError):
                warnings.warn(
                    "failed to save global parameter/value pairs to "
                    + self._gname
                    + "\n",
                    ClineWarning,
                )
            except AttributeError:
                warnings.warn(
                    "global parameter file attribute undefined;"
                    " possible programming error\n",
                    ClineWarning,
                )

            # return to default behaviour
            signal.signal(signal.SIGINT, signal.SIG_DFL)

    def prompt_state(self):
        """Says whether prompting is being forced or not. Note the propting
        state does not change once an Cline is initialized, being
        fixed by the presence of 'PROMPT' on the command line or not.

        Returns True if prompting is being forced.

        """
        return self._prompt

    def register(self, param, g_or_l, p_or_h):
        """Registers a parameter as one to be expected and defines basic
        properties. You must call this once for every parameter that
        you might call 'get_value' for.

        Arguments:

          param : str
              parameter name. Must have no spaces, equal signs or quotes.

          g_or_l : int
              defines whether the parameter should be global, i.e. stored
              in a file called GLOBAL to allow access from other commands,
              or just local to this command. Use the static variables GLOBAL
              and LOCAL to set this, e.g. hipercam.cline.Cline.GLOBAL

          p_or_h : int
              defines whether the parameter is prompted for by default or
              hidden. Parameters that are rarely changed are better hidden to
              reduce clutter. The 'prompt' command-line keyword forces even
              hidden parameters to be prompted for in the rare cases that they
              need to be changed. Use the static variables PROMPT and HIDE to
              set this.

        Sometimes you may want to set the default values of hidden parameters
        unless you are happy for the set value to be retained.

        """

        if (
            param.find(" ") != -1
            or param.find("\t") != -1
            or param.find("=") != -1
            or param.find('"') != -1
            or param.find("'") != -1
        ):
            raise ClineError("Parameter = " + param + " is illegal.")

        if g_or_l != Cline.GLOBAL and g_or_l != Cline.LOCAL:
            raise ClineError(
                "g_or_l must either be Cline.GLOBAL or Cline.LOCAL"
            )

        if p_or_h != Cline.PROMPT and p_or_h != Cline.HIDE:
            raise ClineError(
                "p_or_h must either be Cline.PROMPT or Cline.HIDE"
            )

        if param in self._rpars:
            raise ClineError(
                "parameter = " + param + " has already been registered."
            )

        self._rpars[param] = {"g_or_l": g_or_l, "p_or_h": p_or_h}

    def set_default(self, param, defval):
        """Set the default value of a parameter automatically. This is often
        useful for changing hidden parameters on the fly.

        """
        if param not in self._rpars:
            raise ClineError(
                'set_default: parameter = "' + param +
                '" has not been registered.'
            )

        if self._rpars[param]["g_or_l"] == Cline.GLOBAL:
            self._gpars[param] = defval
        else:
            self._lpars[param] = defval

    def get_default(self, param, noval=None):
        """Gets the current default value of a parameter called
        'param'. Comes back with 'noval' if there is no value set.

        """
        if param not in self._rpars:
            raise ClineError(
                'set_default: parameter = "' + param +
                '" has not been registered.'
            )

        if self._rpars[param]["g_or_l"] == Cline.GLOBAL:
            defval = self._gpars.get(param, noval)
        else:
            defval = self._lpars.get(param, noval)
        return defval

    def get_value(
            self, param, prompt, defval,
            minval=None, maxval=None,
            lvals=None, fixlen=True,
            multipleof=None, ignore=None,
            enforce=True
    ):
        """Gets the value of a parameter, either from the command arguments,
        or by retrieving default values or by prompting the user as
        required. This is the main function of Cline. The value
        obtained is used to update the defaults which, if 'nodefs' has
        not been defined, are written to disk at the end of the
        command.

        Arguments::

          param : str
             parameter name.

          prompt : str
             the prompt string associated with the parameter

          defval : various
             default value if no other source can be found (e.g. at start).
             This also defines the data type of the parameter (see below for
             possibilities)

          minval : same as defval's type
             the minimum value of the parameter to allow. This is also
             the value that will be used if the user type "min". See
             also "enforce".

          maxval : same as defval's type
             the maximum value of the parameter to allow. This is also
             the value that will be used if the user type "max". See
             also "enforce".

          lvals : list
             list of possible values (exact matching used)

          fixlen : bool
             for lists or tuples, this insists that the user input has the
             same length

          multipleof : int
             specifies a number that the final value must be a multiple of
             (integers only)

          ignore : same as defval | None
             a string value that will cause the routine to immediately
             return with a None. The idea is to enable ignoring of
             parameter values based on checking for None later in the
             calling code. For Fname inputs in particular, this skips
             any checks on the existence of files. If used, one should
             put the string needed to match the value of ignore in the
             prompt. The usual value used in the hipercam pipeline is
             'none'.

          enforce : bool
             controls whether "min" and "max" are used to prevent user
             input outside the range. In some case one really does not
             want input outside of min and max, whereas in others, it
             would not matter and "min" and "max" are mainly as
             guidance.

        Data types: at the moment, only certain data types are
        recognised by this routine. These are the standard numerical
        types, 'int', 'long', 'float', the logical type 'bool' (which
        can be set with any of, case insensitively, 'true', 'yes',
        'y', '1' (all True), or 'false', 'no', 'n', '0' (all False)),
        strings, tuples, lists, and hipercam.cline.Fname objects to
        represent filenames with specific extensions. In the case of
        tuples and lists, it is the default value 'defval' which sets
        the type.

        """

        if param not in self._rpars:
            raise ClineError(
                f'parameter = "{param.upper()}" has not been registered.'
            )

        if lvals != None and defval not in lvals:
            raise ClineError(
                f"default = {defval} not in allowed list = {lvals}"
            )

        # Now get the parameter value by one of three methods

        if param in self._pbynam:
            # get value from name/value pairs read from command line
            # arguments of the form param=value
            value = self._pbynam[param]

        elif self.narg < len(self._pbypos) and (
            self._prompt or self._rpars[param]["p_or_h"] == Cline.PROMPT
        ):
            # get value from bare values in the command line such as
            # '23' '\\' indicates use the default value and also to
            # use defaults for any other unspecified parameters that
            # come later (_usedef set to True)
            if self._pbypos[self.narg] == "\\":
                if (
                    self._rpars[param]["g_or_l"] == Cline.GLOBAL
                    and param in self._gpars
                ):
                    value = self._gpars[param]
                elif (
                    self._rpars[param]["g_or_l"] == Cline.LOCAL and \
                        param in self._lpars
                ):
                    value = self._lpars[param]
                else:
                    value = defval
                self._usedef = True
            else:
                value = self._pbypos[self.narg]
            self.narg += 1

        else:
            # load default from values read from file or the initial value
            if self._rpars[param]["g_or_l"] == Cline.GLOBAL and \
               param in self._gpars:
                value = self._gpars[param]
            elif self._rpars[param]["g_or_l"] == Cline.LOCAL and \
                 param in self._lpars:
                value = self._lpars[param]
            else:
                value = defval

            # prompt user for input
            if not self._usedef and (
                self._prompt or self._rpars[param]["p_or_h"] == Cline.PROMPT
            ):
                reply = "?"
                while reply == "?":
                    reply = input(f"{param} - {prompt} [{value}]: ")
                    if reply == "\\":
                        self._usedef = True
                    elif reply == "?":
                        print()
                        qualifier = "must" if enforce else "should normally"
                        if minval is not None and maxval is not None:
                            print(
                                f'Parameter = "{param}" {qualifier} lie from {minval} to {maxval}'
                            )
                        elif minval is not None:
                            print(
                                f'Parameter = "{param}" {qualifier} be greater than {minval}'
                            )
                        elif maxval is not None:
                            print(
                                f'Parameter = "{param}" {qualifier} be less than {maxval}'
                            )
                        else:
                            print(
                                f'Parameter = "{param}" has no restriction on its value'
                            )

                        print(f'"{param}" has data type = {type(defval)}')
                        if lvals is not None:
                            print("Only the following values are allowed:")
                            print(lvals)
                        if isinstance(defval, (list, tuple)) and fixlen:
                            print(
                                f"You must enter exactly {len(defval)} values"
                            )
                        print()
                    elif reply != "":
                        if (
                            isinstance(defval, (list, tuple))
                            and fixlen
                            and len(reply.split()) != len(defval)
                        ):
                            print(
                                f"You must enter exactly {len(defval)} values."
                                " [You only entered {len(reply.split()}]"
                            )
                            reply = "?"
                        else:
                            value = reply

        if value == ignore:
            if self._rpars[param]["g_or_l"] == Cline.GLOBAL:
                self._gpars[param] = ignore
            else:
                self._lpars[param] = ignore
            return None

        # at this stage we have the value, now try to convert to the
        # right type according to the type of 'defval'
        try:
            if isinstance(defval, Fname):
                # run Fname checks
                value = defval(value)

            elif isinstance(defval, str):
                value = str(value)
                if value == "''":
                    value = ""

            elif isinstance(defval, bool):
                if isinstance(value, str):
                    if value.lower() == "true" or \
                       value.lower() == "yes" or \
                       value.lower() == "1" or \
                       value.lower() == "y":
                        value = True
                    elif value.lower() == "false" or \
                         value.lower() == "no" or \
                         value.lower() == "0" or \
                         value.lower() == "n":
                        value = False
                    else:
                        raise ClineError(
                            f'could not translate "{value}"'
                            ' to a boolean True or False.'
                        )
            elif isinstance(defval, int):
                # 'max' and 'min' will set to the maximum and minimum
                # values if they have been set handle these here
                # before attempting to convert to a float
                if isinstance(value, str):
                    if value == "min":
                        if minval is not None:
                            value = minval
                        else:
                            raise ClineError(f"{param} has no minimum value")
                    elif value == "max":
                        if maxval is not None:
                            value = maxval
                        else:
                            raise ClineError(f"{param} has no maximum value")

                value = int(value)

            elif isinstance(defval, float):
                # 'max' and 'min' will set to the maximum and minimum
                # values if they have been set handle these here
                # before attempting to convert to a float
                if isinstance(value, str):
                    if value == "min":
                        if minval is not None:
                            value = minval
                        else:
                            raise ClineError(f"{param} has no minimum value")
                    elif value == "max":
                        if maxval is not None:
                            value = maxval
                        else:
                            raise ClineError(f"{param} has no maximum value")

                value = float(value)

            elif isinstance(defval, list):
                if isinstance(value, str):
                    value = list(map(type(defval[0]), value.split()))
                else:
                    value = list(value)
            elif isinstance(defval, tuple):
                if isinstance(value, str):
                    value = tuple(map(type(defval[0]), value.split()))
                else:
                    value = tuple(value)
            else:
                raise ClineError(
                    "did not recognize the data type of the default"
                    f" supplied for parameter {param} = {type(defval)}"
                )

        except ValueError as err:
            raise ClineError(str(err))

        # ensure value is within range
        if minval != None and value < minval and enforce:
            raise ClineError(
                f"{param} = {value} < {minval}"
            )
        elif maxval != None and value > maxval and enforce:
            raise ClineError(
                f"{param} = {value} > {maxval}"
            )

        # and that it is an OK value
        if lvals != None and value not in lvals:
            raise ClineError(
                f"{value} is not one of the allowed values = {lvals}"
            )

        if multipleof != None and value % multipleof != 0:
            raise ClineError(
                f"{value} is not a multiple of {multipleof}"
            )

        # update appropriate set of defaults. In the case of Fnames,
        # strip the extension
        if self._rpars[param]["g_or_l"] == Cline.GLOBAL:
            if isinstance(defval, Fname):
                self._gpars[param] = defval.noext(value)
            else:
                self._gpars[param] = value
        else:
            if isinstance(defval, Fname):
                self._lpars[param] = defval.noext(value)
            else:
                self._lpars[param] = value

        if self._list:
            print(f"{param} = {value}")

        return value

    def get_rest(self):
        """Returns any unused command-line arguments as a list or None if
        there aren't any

        """
        if self.narg < len(self._pbypos):
            return self._pbypos[self.narg :]
        else:
            return None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.save()


class Fname(str):
    """Defines a callable parameter type for the :class:`Cline` to allow
    for some early checks on file names. This is mainly to prevent a
    whole series of parameters being input, only to find that the file
    name input in the first one is incorrect.

    """

    OLD = 0
    NEW = 1
    NOCLOBBER = 2

    def __new__(cls, root, ext="", ftype=OLD, exist=True):
        """Constructor distinct from __init__ because str is immutable. In the
        following text items in capitals such as 'OLD' are static
        variables so that one should use hipercam.cline.Fname.OLD or
        equivalent to refer to them.

        Arguments::

          root : str
             root name of file (if it ends with 'ext', an extra 'ext' will
             not be added)

          ext : str
             extension, e.g. '.dat'

          ftype : int
             OLD = existing or possibly existing file; NEW = new file which
             will overwrite anything existing; NOCLOBBER is same as NEW but
             there must not be an existing one of the specified name.

          exist : bool
             If exist=True and ftype=OLD, the file :must: exist. If
             exist=False, the file may or may not exist already.

        """

        if ftype != Fname.OLD and ftype != Fname.NEW and \
           ftype != Fname.NOCLOBBER:
            raise ClineError("ftype must be either OLD, NEW or NOCLOBBER")

        # store root with no extension
        if len(ext) and root.endswith(ext):
            fname = super().__new__(cls, root[: -len(ext)])
        else:
            fname = super().__new__(cls, root)

        return fname

    def __init__(self, root, ext="", ftype=OLD, exist=True):
        """Initialiser. In the following text items in capitals such as 'OLD'
        are static variables so that one should use
        hipercam.cline.Fname.OLD or equivalent to refer to them.

        Arguments::

          root : str
             root name of file (if it ends with 'ext', an extra 'ext' will
             not be added)

          ext : str
             extension, e.g. '.dat'

          ftype : int
             If exist=True and ftype=OLD, the file :must: exist. If
             exist=False, the file may or may not exist already.

          exist : bool
             If True, the file must exist.

        ext, ftype and exist are stored as identically-named
        attributes. 'root' is stored as the base string.

        """

        self.ext = ext
        self.ftype = ftype
        self.exist = exist

    def __call__(self, fname):
        """Given a potential file name, this first ensures that it has the
        correct extension, and then tests for its existence if need
        be, depending upon the values of `ftype` and `exist` defined
        at instantiation.

        Arguments::

           fname : str
              file name. The extension associated with the
              :class:`Fname` will be added if necessary.

        Returns the file name to use. Raises a ClineError exception if there
        are problems.

        """

        # Add extension if not already present.
        fname = add_extension(fname, self.ext)

        if self.exist and self.ftype == Fname.OLD and not os.path.exists(fname):
            raise ClineError(f"could not find file = {fname}")

        if self.ftype == Fname.NOCLOBBER and os.path.exists(fname):
            raise ClineError(f"file = {fname} already exists")

        return fname

    def noext(self, fname):
        """Returns the suggested file name, `fname`, with the extension
        removed"""
        if len(self.ext) and fname.endswith(self.ext):
            return fname[: -len(self.ext)]
        else:
            return fname

    def __getnewargs__(self):

        """Enables pickling of :class:`Fname` objects. This returns a tuple of
        arguments that are passed off to __new__

        """
        return (str(self), self.ext, self.ftype, self.exist)

class ClineError(Exception):
    """For throwing exceptions from cline"""


class ClineWarning(UserWarning):
    """For producing warnings from cline"""
