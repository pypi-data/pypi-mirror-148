from setuptools import setup, find_packages

VERSION = '1' 
DESCRIPTION = 'Writing style analyzer'
LONG_DESCRIPTION = '''This package analyzes the style of a given writing sample using "involved" and "informational" linguistic features. More information on the Github page: https://github.com/el2727/test_update'''

# Setting up
setup(
        name="test_updates", 
        version=VERSION,
        author="Ekaterina Levitskaya, Kara Kedrick, Russell J. Funk",
        author_email="test_test@email.com, test_test1@email.com, test_test_1@email.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['spacy'],
        
        keywords=['python', 'writing style'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)