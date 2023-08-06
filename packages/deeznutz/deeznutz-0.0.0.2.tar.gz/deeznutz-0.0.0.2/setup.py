from setuptools import setup, find_packages

VERSION = '0.0.0.2' 
DESCRIPTION = 'Python package with wide array of functions to manipulate the complex environment of deez nuts'

LONG_DESCRIPTION = "I'll explain all the functionalities of this extremely wide-range utility module after setting everything up ;) Preferred usage is import deeznutz as dn"

# Setting up
setup(
        name="deeznutz", 
        version=VERSION,
        author="Lawrence Long",
        author_email="lawrence.long@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python', 'utility'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
