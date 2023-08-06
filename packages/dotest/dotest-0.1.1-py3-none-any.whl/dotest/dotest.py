#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Minghao Zhao

import pytest
import yaml
import os
import sys

from dotest import tools
from junitparser import JUnitXml

cwd = os.getcwd()


class DoTest:
    def __init__(self, testset):
        self.args = None
        self.inner_data = os.path.join(cwd, ".inner.data")
        self.testset = testset
        self.global_testbed = {}
        self.file_list = []
        self.junit_xml_list = []
        self.init_env()

    def init_env(self):
        if os.path.exists(self.inner_data):
            __import__('shutil').rmtree(self.inner_data)
        os.makedirs(self.inner_data)
        os.makedirs("{}/testset".format(self.inner_data))
        os.makedirs("{}/report_xml".format(self.inner_data))

    def parser_testset(self):
        def parser_testcases(testcases):
            # 从文件解析出来case
            new_testcases = []
            for group in testcases:
                assert type(group) == dict
                if "testgroup" in group:
                    new_testcases.append(group)
                elif "testset" in group:
                    assert group["testset"] not in self.file_list, "The file[{}] has a loop".format(group["testset"])
                    self.file_list.append(group["testset"])
                    _, _testcases = tools.parser_testset(group["testset"])
                    new_testcases += _testcases
                else:
                    assert False
            # 检查case合法性 并增加node_id
            flag = False
            case_id = 1
            for i in range(len(new_testcases)):
                if "testset" in new_testcases[i]:
                    flag = True
                    break
                if "testgroup" in new_testcases[i]:
                    for j in range(len(new_testcases[i]["testgroup"])):
                        new_testcases[i]["testgroup"][j]["case_id"] = case_id
                        case_id += 1
            if flag:
                return parser_testcases(new_testcases)
            return new_testcases

        self.testbed, testcases = tools.parser_testset(self.testset)
        self.testbed.update(self.global_testbed)
        self.testcases = parser_testcases(testcases)

    def save_group_file(self, group):
        group_file = os.path.join(self.inner_data, "testset/{:04d}.group.yaml".format(group["id"]))
        with open(group_file, "w") as fd:
            yaml.dump_all([group["testbed"], group["testset"]], fd)
        return group_file

    def run_pytest(self, group):
        one_group_testset = self.save_group_file(group)
        py_args = ["--testset={}".format(one_group_testset)]
        py_args += pytest._plugin
        if self.args.junitxml:
            name = self.args.junitxml.split("/")[-1]
            junitxml="{}/report_xml/{:04d}.group.{}".format(self.inner_data, group["id"], name)
            self.junit_xml_list.append(junitxml)
            py_args += ["--junitxml={}".format(junitxml)]

        if "pytest" in group["testset"][0]:
            py_args += group["testset"][0]["pytest"].split()
        result = pytest.main(py_args)
        print("==*==" * 10)
        print(pytest._plugin)
        if result and result:
            sys.exit(result)

    def merge_xml_report(self):
        xml_report = None
        for xml_file in self.junit_xml_list:
            xml = JUnitXml.fromfile(xml_file)
            if xml_report is None:
                xml_report = xml
            else:
                xml_report += xml
        xml_dir = self.args.junitxml.rsplit("/", 1)[0]
        if not os.path.exists(xml_dir):
            os.makedirs(xml_dir)
        xml_report.write(self.args.junitxml)

    def run(self):
        self.parser_testset()
        group = {"id": 0, "testbed": self.testbed, "testset": []}
        for _group in self.testcases:
            group["testset"] = [_group]
            group["id"] += 1
            # 此处可以支持不同的测试case框架
            self.run_pytest(group)
        if self.args.junitxml:
            self.merge_xml_report()


if __name__ == "__main__":
    print("i'm main")

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
