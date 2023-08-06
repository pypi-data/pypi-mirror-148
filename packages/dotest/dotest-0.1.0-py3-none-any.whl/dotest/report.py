#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Authors: Minghao Zhao

import pytest
import re
import os

from dotest import tools


cwd = os.getcwd()


class ReportPlugin:
    def __init__(self, testset):
        self.testset = testset
        self.testcase = {}
        self.re = re.compile(r'[\[](.*?)[\]]', re.S)

    def parser_testset(self):
        _, testcase = tools.parser_testset(self.testset)
        for case in testcase[0]["testgroup"]:
            case["status"] = "passed"
            self.testcase[case["case_id"]] = case

    def post_result(self, body):
        import json
        # print(json.dumps(body, indent=2))
        return

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        id = int(re.findall(self.re, item.nodeid)[0])
        self.testcase[id]["nodeid"] = item.nodeid
        result = yield
        report = result.get_result()
        if report.outcome != "passed":
            if self.testcase[id]["status"] == "passed":
                self.testcase[id]["status"] = report.outcome
                self.testcase[id]["step"] = report.when
                self.testcase[id]["errmsg"] = report.longreprtext
                # print(self.testcase[id])
                # if self.testcase[id]["step"] == "teardown":
                #    import pdb
                #    pdb.set_trace()
        if report.when == "teardown":
            print(report)
            self.post_result(self.testcase[id])


if __name__ == "__main__":
    print("i'm main")

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
