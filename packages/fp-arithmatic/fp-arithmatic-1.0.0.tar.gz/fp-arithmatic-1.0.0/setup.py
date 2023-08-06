from setuptools import setup, find_packages
from os import path

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name = "fp-arithmatic",
    version="1.0.0",
    packages = ["fp_arithmatic"], # include library only
    install_requires=["numpy"],  # dependencies
    python_requires='>=3.6',
    description="A simple arithmatic library",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url ="",
    author="Faizan Patel",
    license="MIT"
)