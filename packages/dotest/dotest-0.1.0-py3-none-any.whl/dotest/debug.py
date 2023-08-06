#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Authors: Minghao Zhao

import pytest


class MyPlugin:
    def __init__(self):
        self.name = "my_plugin"

    def pytest_generate_tests(self, metafunc):
        metafunc.parametrize("a,b,c", [(1, 2, 3)])
        print(self.name)


def test_func_parametrize(a, b, c):
    print("{} + {} + {} = {}".format(a, b, c, a + b +c))


if __name__ == "__main__":
    cases = ["debug.py::test_func_parametrize", "-sv"]
    my = MyPlugin()
    pytest.main(cases, plugins=[my])
    cases.append("-n 1")
    pytest.main(cases, plugins=[my])
# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
