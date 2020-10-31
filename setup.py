#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup

with open("requirements.txt", "r") as fh:
    dependencies = [l.strip() for l in fh]

setup(
    name="tpass",
    version="0.0.1",
    description="Terminal UI for pass.",
    keywords="tpass",
    author="Patrick Schneeweis",
    author_email="psbleep@protonmail.com",
    url="https://github.com/psbleep/tpass",
    license="GPLv3",
    long_description=io.open("README.md", "r", encoding="utf-8").read(),
    platforms="any",
    zip_safe=False,
    include_package_data=True,
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["tpass"],
    install_requires=dependencies,
    entry_points={"console_scripts": ["tpass = tpass.__main__:main",]},
)
