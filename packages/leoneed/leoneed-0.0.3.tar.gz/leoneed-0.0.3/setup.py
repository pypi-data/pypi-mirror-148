#!/usr/bin/env Python
# -*- coding: utf-8 -*-
import setuptools
setuptools.setup(
    name = "leoneed",
    version = "0.0.3",
    description = "A Simple Trial on Tensor-Graph-based Network...",
    long_description = open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/sandyzikun/leoneed.git",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ],
    packages = setuptools.find_packages(),
    install_requires = ["numpy>=1.14.3", "matplotlib>=2.2.2"],
    )
