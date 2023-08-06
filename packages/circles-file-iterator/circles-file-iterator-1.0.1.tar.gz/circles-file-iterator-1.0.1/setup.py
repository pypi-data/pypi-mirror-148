import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Requirements
REQS = [req.split('==')[0] for req in open((HERE / "requirements.txt"), 'r').readlines()]

# This call to setup() does all the work
setup(
    name="circles-file-iterator",
    version="1.0.1",
    description="Allows to iterate over CyVerse CIRCLES files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/codingrosquick/circles_file_handler",
    author="Noe Carras",
    author_email="carras.noe@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["circles_file_iterator"],
    include_package_data=True,
    install_requires=REQS,
)