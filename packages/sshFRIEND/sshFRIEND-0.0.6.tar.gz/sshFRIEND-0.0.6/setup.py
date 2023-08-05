import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    with open("README.md") as f:
        return f.read()

setup(
    name = "sshFRIEND",
    version = "0.0.6",
    author = "David Johnnes",
    author_email = "david.johnnes@gmail.com",
    description = ("A generic and platform agnostic SSH module to access and send commands to remote devices that support OpenSSH"),
    license = "BSD",
    keywords = "ssh access, ssh remote command execution",
    url = "",
    packages=['sshFRIEND'],
    long_description=read('README'),
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
)