#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Minghao Zhao
import time
import pytest
import os

from loguru import logger
from dotest import tools

cwd = os.getcwd()


class Logger:
    def __init__(self):
        self.log_dir = os.path.join(cwd, "log")
        self.log_path = None
        self.logid = []

    def remove_history_log_file(self, days=3):
        for filename in os.listdir(self.log_dir):
            log_path = os.path.join(self.log_dir, filename)
            if os.path.getmtime(log_path) < time.time() - 3600 * 24 * days:
                if filename.startswith("20") and filename.find("log") > 0:
                    os.remove(log_path)

    def init_logger(self, nodeid):
        logger.remove()
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        log_path = os.path.join(self.log_dir,
                                time.strftime("%Y%m%d%H%M%S", time.localtime()) + "." +
                                nodeid.split("/")[-1].split("[")[
                                    0] + ".log")
        my_format = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                     "<level>{level: <8}</level> | "
                     "{process:>6}:{thread:<10} | "
                     "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
        # 后续更多的logger参数需要暴露出来
        self.logid.append(logger.add(log_path, format=my_format, rotation="1 GB", retention="2 days"))
        self.remove_history_log_file()

    def pytest_runtest_setup(self, item):
        self.init_logger(item.nodeid)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        result = yield
        report = result.get_result()
        logger.debug("{} run {} {}".format(item.nodeid, report.when, report.outcome))
        if report.outcome != "passed":
            logger.error(report.longreprtext)

    def pytest_runtest_logfinish(self, nodeid, location):
        while len(self.logid) > 0:
            logger.remove(self.logid.pop())


if __name__ == "__main__":
    print("i'm main")

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
