from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package long description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ib_calculator", 
        version=VERSION,
        author="Igor Balagula",
        author_email="<i_balagula@yahoo.com>",
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