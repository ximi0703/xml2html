#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: test.py
# Date: 2024/9/10
# Author: chuanwen.peng
import os
import re
import jinja2
import xml.etree.ElementTree as ET


class Xml2Html(object):
    def __init__(self, *args, **kwargs):
        self._envrionment = jinja2.Environment()
        self._load_template()

    def _load_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "template" not in path:
            old_line = re.findall(r'.*?\n(.*?)\n\s+', content)[0]
            new_line = old_line.replace("testsuites", "testsuite").replace('sts">', 'sts"/>')
            new_line = old_line + "\n" + new_line
            content = content.replace(old_line, new_line)
        return content

    def _load_template(self):
        path = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(path, "template.html")
        self._template = self._load_file(template_path)

    def parse(self, path):
        return self.parse_content(self._load_file(path))

    def parse_content(self, content):
        result = list()
        tree = ET.fromstring(content)
        for testsuite in tree.iter(tag="testsuite"):
            _testsuite = dict(summary={}, testcases=[])
            _testsuite["summary"] = testsuite.attrib
            for testcase in testsuite.iter(tag="testcase"):
                _testcase = testcase.attrib
                # children = testcase.getchildren()
                children = testcase.iter()
                if children:
                    stdout = []
                    for child in children:
                        if child.tag == "properties":
                            property_dic = {i.attrib["name"] : i.attrib["value"] for i in child}
                            _testcase["desc"] = property_dic["desc"]
                            property_dic.pop("desc")
                            _testcase["step"] = property_dic
                        elif child.tag == "system-out":
                            stdout.append(child.text)
                        elif child.tag == "failure":
                            _testcase["status"] = child.tag
                            _testcase["text"] = child.text
                        elif child.tag == "testcase":
                            _testcase["status"] = "success"
                            _testcase["text"] = ""
                            _testcase["type"] = child.attrib.get("type")
                            _testcase["desc"] = child.attrib.get("message")

                    else:
                        _testcase["stdout"] = "\n".join(stdout)
                else:
                    _testcase["status"] = "success"

                _testsuite["testcases"].append(_testcase)

            tests = testsuite.attrib.get("tests", 0)
            errors = testsuite.attrib.get("errors", 0)
            failures = testsuite.attrib.get("failures", 0)
            skipped = testsuite.attrib.get("skip", 0) or testsuite.attrib.get(
                "skipped", 0
            )

            if int(errors):
                _testsuite["summary"]["status"] = "error"
            elif int(failures):
                _testsuite["summary"]["status"] = "failure"
            elif int(tests) == int(skipped):
                _testsuite["summary"]["status"] = "skipped"
            else:
                _testsuite["summary"]["status"] = "success"

            result.append(_testsuite)

        new_result = result.copy()
        testcase_li = []
        for r in new_result:
            if "AllTests" not in r["summary"]["name"]:
                testcase_li.append(r["testcases"])
        testcase_li_new = [item for sublist in testcase_li for item in sublist]
        all_index = result.index([i for i in result if "AllTests" == i["summary"]["name"]][0])
        result[all_index]["testcases"] = testcase_li_new
        return result

    def generate_html(self, result, embed=False):
        template = self._envrionment.from_string(self._template)
        html = template.render(embed=embed, testsuites=result)
        return html

    def _export_html(self, html, path="."):
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("File saved to {}".format(path))

    def convert(self, path, dest):
        testsuites = self.parse(path)
        html = self.generate_html(testsuites)
        self._export_html(html, dest)
