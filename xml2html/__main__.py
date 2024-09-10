#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: test.py
# Date: 2024/9/10
# Author: chuanwen.peng
import argparse
from xml2html.xml2html.xml2html import Xml2Html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="the path of the xml file")
    parser.add_argument(
        "-o", "--output", type=str, help="the path of the generated html file"
    )
    args = parser.parse_args()
    xml2html_t = Xml2Html()
    xml2html_t.convert(args.file, args.output)


if __name__ == "__main__":
    main()
