import os
from setuptools import setup

# Get the long description from the README file
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='trm.cline',
    version='1.0.0',
    packages = ['trm.cline'],

    # metadata
    author='Tom Marsh',
    author_email='t.r.marsh@warwick.ac.uk',
    description="Allows scripts to remember parameter input values",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/trmrsh/trm-cline',
    
    # Choose your license
    license='BSD',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # Uses f-strings which only came in python v3.6
    python_requires='>=3.6',

)

