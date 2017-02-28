#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# __author__ = 'liuyuantuo@baidu.com'
import argparse


class ArgsParser(object):
    """
    Summary:
        用于命令参数解析的类
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def parser(self, args):
        """
        该函数用于重载
        Brief"
            用户的命令行参数设置

        Args:
            args: 用户输入对应的configure

        Returns:
            返回一个dict
            例如{'configure': 'test.conf'}
        """

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--configure', help="配置文件选项")
        self.parser.add_argument('--version', '-v',
                            action="version",
                            version="raiders upload system 1.0",
                            help="系统版本号")
        return self.parser.parse_args(args)