from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'This package is used for performing exploratory data analysis'
LONG_DESCRIPTION = 'This package is used for performing exploratory data analysis. It contains functions to perform imputation, statistical tests'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="Imputation",
    version=VERSION,
    author="Saisakul Chernbumroong",
    author_email="s.chernbumroong@bham.ac.uk",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)