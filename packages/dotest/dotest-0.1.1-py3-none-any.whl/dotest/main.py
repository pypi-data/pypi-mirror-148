#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Authors: Minghao Zhao

import argparse
import pytest
import yaml
import sys
import os

from dotest.dotest import DoTest


cwd = os.getcwd()


def run_testset(args):
    # pytest._testbed = {}
    dotest = DoTest(args.testset)
    if not os.path.exists(args.testset):
        print("please check testset parametrize, the file not exist")
        sys.exit(1)
    if args.testbed:
        if not os.path.exists(args.testbed):
            print("please check testbed parametrize, the file not exist")
            sys.exit(1)
        with open(args.testbed) as fd:
            dotest.global_testbed = yaml.load(fd, Loader=yaml.FullLoader)
    dotest.args = args
    dotest.run()


def main():
    parser = argparse.ArgumentParser(prog="do test", usage="DoTest specific parameter list", add_help=False)
    # parser.add_argument("-v", "--version", dest="version", action="store_true", help="show version")
    parser.add_argument("--testset", help="testset")
    parser.add_argument("--testbed", help="testbed")
    parser.add_argument("--junitxml", help="[pytest] create junit-xml style report file at given path.")
    parser.add_argument("-h", "--help", action="store_true", help="查看完整的帮助信息（包括pytest）")

    args, pytest._plugin = parser.parse_known_args()
    pytest._plugin.extend(["-W", "ignore:Module already imported:pytest.PytestWarning"])
    if args.help:
        pytest.main(["-h"] + pytest._plugin)
        print("==" * 15 + "DoTest help" + "==" * 15)
        parser.print_help()
        sys.exit(0)

    if args.testset:
        run_testset(args)
        sys.exit(0)
    parser.print_help()


if __name__ == "__main__":
    print(cwd)
    main()

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
