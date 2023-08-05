from setuptools import setup, find_packages

setup(
    # the name must match the folder name 'verysimplemodule'
    name="aviHelloWorld", 
    version='0.0.1',
    author="Avi",
    author_email="jeavijenn@gmail.com",
    description='My first Python package',
    long_description='My first Python package with a slightly longer description',
    packages=find_packages(),
    
    # add any additional packages that 
    # needs to be installed along with your package.
    install_requires=[], 
    
    keywords=['python', 'first package'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ]
)