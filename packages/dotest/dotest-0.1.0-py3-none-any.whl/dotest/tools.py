#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Authors: Minghao Zhao

import yaml


def parser_testset(testset):
    testbed = {}
    testcase = []
    if type(testset) != str:
        return testbed, testset
    with open(testset) as fd:
        data = list(yaml.load_all(fd, Loader=yaml.FullLoader))
    for one in data:
        if type(one) == list:
            testcase = one
        if type(one) == dict:
            testbed = one
    # assert "testgroup" in testcase[0], "please check testset file"
    return dict(testbed), list(testcase)


if __name__ == "__main__":
    print("i'm main")

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
