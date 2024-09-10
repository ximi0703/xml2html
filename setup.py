#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: test.py
# Date: 2024/9/10
# Author: chuanwen.peng
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="xml2html",
    version="0.0.1",
    description="Generate html file from xml reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="chuanwen.peng",
    author_email="3386993382@qq.com",
    url="https://github.com/ximi0703/xml2html",
    install_requires=["jinja2"],
    packages=["xml2html"],
    package_data={"xml2html": ["template.html"]},
    include_package_data=True,
    entry_points={"console_scripts": ["xml2html=xml2html.__main__:main"]},
)
