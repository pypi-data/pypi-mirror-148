#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Authors: Minghao Zhao

from dotest.generate import GeneratePlugin
from dotest.report import ReportPlugin
from dotest.logger import Logger


def parse_testset(s):
    """check"""
    return s


def pytest_addoption(parser):
    group = parser.getgroup("do test")
    group._addoption(
        "-t",
        "--testset",
        dest="testset",
        metavar="testset",
        action="store",
        type=parse_testset,
        help="testset filepath"
    )
    group.addoption(
        "--report",
        dest="report",
        nargs='?',
        default=False,
        const=True,
        help="report filepath"
    )
    group.addoption(
        "--logger",
        dest="logger",
        nargs='*',
        default=False,
        help="logger init"
    )
    group.addoption(
        "--shuffle",
        action="store_true",
        help="shuffle the order of case before run"
    )


def pytest_configure(config):
    if config.getoption("testset"):
        testset = config.getoption("testset")
        generate1 = GeneratePlugin(testset, config.getoption("shuffle"))
        generate1.parser_testset()
        config.args = generate1.case_list
        config.pluginmanager.register(generate1)

        if config.getoption("report"):
            report = ReportPlugin(testset)
            report.parser_testset()
            config.pluginmanager.register(report)

    if isinstance(config.getoption("logger"), list):
        logger = Logger()
        config.pluginmanager.register(logger)


def main():
    pass


if __name__ == "__main__":
    main()
    print("i'm main")

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
