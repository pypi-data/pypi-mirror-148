#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Authors: Minghao Zhao

import pytest
import random
import re
import os

from dotest import tools


cwd = os.getcwd()


class GeneratePlugin:
    def __init__(self, testset, shuffle=False):
        self.testset = testset
        self.shuffle = shuffle
        self.re = re.compile(r'[\[](.*?)[\]]', re.S)
        self.case_list = []  # main used
        self.case_param = {}  # only used pytest_generate_tests

    def parser_testset(self):
        pytest.testbed, testcase = tools.parser_testset(self.testset)
        self.testcase = testcase[0]["testgroup"]
        self.case_list = [os.path.join(cwd, unit["name"]) for unit in self.testcase]
        for case in self.testcase:
            if case["name"] not in self.case_param:
                self.case_param[case["name"]] = []
            self.case_param[case["name"]].append(case)

    def pytest_generate_tests(self, metafunc):
        if metafunc.definition.nodeid in self.case_param:
            if len(metafunc.fixturenames) and "parametrize" in metafunc.fixturenames:
                argnames = "parametrize"
                argvalues = [unitcase["parametrize"] for unitcase in self.case_param[metafunc.definition.nodeid]]
                ids = [unitcase["case_id"] for unitcase in self.case_param[metafunc.definition.nodeid]]
                metafunc.parametrize(argnames, argvalues, ids=ids)
            elif "parametrize" in self.case_param[metafunc.definition.nodeid][0]:
                argnames = list(self.case_param[metafunc.definition.nodeid][0]["parametrize"].keys())
                argvalues = []
                ids = []
                for unitcase in self.case_param[metafunc.definition.nodeid]:
                    argvalues.append(unitcase["parametrize"])
                    ids.append(unitcase["case_id"])
                metafunc.parametrize(argnames, argvalues, ids=ids)
            else:
                metafunc.fixturenames.append("__dotest_repeat")
                ids = [unitcase["case_id"] for unitcase in self.case_param[metafunc.definition.nodeid]]
                metafunc.parametrize('__dotest_repeat', ids, ids=ids)
            del self.case_param[metafunc.definition.nodeid]
        else:
            metafunc.fixturenames.append("__dotest_repeat")
            for case in self.case_param:
                if case in metafunc.definition.nodeid:
                    for i in range(len(self.case_param[case])):
                        if "case.{}".format(metafunc.definition.nodeid) not in self.case_param[case][i]:
                            ids = [self.case_param[case][i]["case_id"]]
                            self.case_param[case][i]["case.{}".format(metafunc.definition.nodeid)] = True
                            metafunc.parametrize('__dotest_repeat', ids, ids=ids)
                            return
            for case in self.case_param:
                if case in metafunc.definition.nodeid:
                    for i in range(len(self.case_param[case])):
                        ids = [self.case_param[case][i]["case_id"]]
                        metafunc.parametrize('__dotest_repeat', ids, ids=ids)
                        return
            metafunc.parametrize('__dotest_repeat', [9999], ids=[9999])

    def pytest_collection_modifyitems(self, items):
        items.sort(key=lambda item: int(re.findall(self.re, item.nodeid)[0]))
        if self.shuffle:
            random.shuffle(items)

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        KNOWN_TYPES = (
            "failed",
            "passed",
            "skipped",
            "deselected",
            "xfailed",
            "xpassed",
            "warnings",
            "error",
        )
        if not getattr(pytest, "dotest_stats", None):
            pytest.dotest_stats = {}

        for stats_type in KNOWN_TYPES:
            if len(terminalreporter.stats.get(stats_type, [])) and stats_type in pytest.dotest_stats:
                terminalreporter.stats[stats_type] += pytest.dotest_stats[stats_type]
            elif not len(terminalreporter.stats.get(stats_type, [])) and stats_type in pytest.dotest_stats:
                terminalreporter.stats[stats_type] = pytest.dotest_stats[stats_type]
        pytest.dotest_stats = terminalreporter.stats

if __name__ == "__main__":
    print("i'm main")

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
