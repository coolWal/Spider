#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# __author__ = 'liuyuantuo@baidu.com'

import logging
import logging.handlers
import os


class Logger(object):
    """spider日志处理类

    该类用于spider的日志处理

    Attributes:
        logfile, 需要构建的日志路径
        settings，其他的设置，是个字典，取出来日志设置需要的字段
    """
    def __init__(self):
        self.logger = None

    def init(self, log_file):
        """
            初始化一份logger instance
        """
        level = logging.INFO
        backup = 7
        when = 'D'
        formater = "%(levelname)s: %(asctime)s: %(filename)s: %(lineno)d * %(thread)d %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(formater, datefmt)
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

        path_name = os.path.dirname(log_file)

        if not os.path.isdir(path_name) and len(path_name) != 0:
            os.makedirs(path_name)

        handler = logging.handlers.TimedRotatingFileHandler(log_file + ".log",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        handler = logging.handlers.TimedRotatingFileHandler(log_file + ".log.wf",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)