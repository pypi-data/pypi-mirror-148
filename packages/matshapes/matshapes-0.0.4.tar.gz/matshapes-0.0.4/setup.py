from setuptools import find_packages, setup
 
# Package meta-data.
NAME = 'matshapes'
DESCRIPTION = 'Test by Rosenberg Strang.'
URL = ''
EMAIL = 'rosenbergstrang@gmail.com'
AUTHOR = 'Rosenberg Strang'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.4'

# What packages are required for this module to be executed?
REQUIRED = []

# Setting.
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    license=""
)