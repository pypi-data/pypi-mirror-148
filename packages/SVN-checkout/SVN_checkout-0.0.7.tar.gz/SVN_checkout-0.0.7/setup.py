import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(README):
    return open(os.path.join(os.path.dirname(__file__), README)).read()

files = ["Agco-Pypi_package/*"]

setup(
    name = "SVN_checkout",
    version = "0.0.7",
    author = "Himanshu Yadav",
    author_email = "h.yadav@technologyandstrategy.com",
    description = "To checkout files from SVN Repository based on Project M2, S2 & MOD.",
    
    license = "BSD",
    keywords = "SVN_repo_checkout",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=["SVN_checkout"],
    package_data = {'Agco-Pypi_package': ['/SVN_checkout/db.yaml']},
    long_description=read('README.md'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: BSD License",
    ],
    
    include_package_data= True,
    install_requires=["request" , "yaml", "subprocess", "argparse", "os"],
    
)