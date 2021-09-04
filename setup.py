#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

setup(
    name="texttab",
    packages=["texttab"],
    package_dir={"": "src"},
    version="0.1.1",
)

