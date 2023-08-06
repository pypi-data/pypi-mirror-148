#!/usr/bin/env python3
import pathlib
from setuptools import setup, find_packages

CWD = pathlib.Path(__file__).parent
README = (CWD / "README.md").read_text()

setup(
    name="address-magic",
    version="0.1.1",
    description="address parsing",
    long_description=README,
    author="Nsaspy",
    py_modules=['address_magic'],
    license="MIT",
    install_requires=["postal"])
