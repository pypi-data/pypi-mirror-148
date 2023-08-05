from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
        name="Data_helper_PIns", 
        version=VERSION,
        author="Sebastian Rawlinson",
        author_email="<sebastianrawlinson6@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        install_requires=["random"],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)