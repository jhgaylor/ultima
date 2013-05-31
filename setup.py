import os
#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = "Ultima",
    version = "0.1",
    author = "Jake Gaylor",
    author_email = "jake@codegur.us",
    description = "It's like SOAP for JSON.",
    url = "https://github.com/jhgaylor/ultima/",
    dependancy_links = [],
    install_requires = [ln for ln in open('requirements.txt')],
    packages = find_packages(),
    #package_data=package_data,
    include_package_data = True,
)