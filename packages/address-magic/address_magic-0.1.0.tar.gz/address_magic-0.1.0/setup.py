#!/usr/bin/env python3
import pathlib
from setuptools import setup, find_packages

CWD = pathlib.Path(__file__).parent
README = (CWD / "README.md").read_text()

setup(
    name="address_magic",
    version="0.1.0",
    description="address parsing",
    long_description=README,
    author="Unseen Giants",
    packages=find_packages(),
    license="MIT",
    install_requires=["postal"],
    author_email="incoming+unseen-giants-ungi-utils-26498131-issue-@incoming.gitlab.com")
