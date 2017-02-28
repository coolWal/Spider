#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# __author__ = 'liuyuantuo@baidu.com'


class Local(object):
    """
        local类，用于从本地获取数据，指定pdf地址以及json数据地址
    """
    def __init__(self, **kwargs):
        # 本地的pdf地址
        self.pdf_data_file = kwargs['pdf_data_file']
        # 经过node输出的json文件
        self.node_data_file = kwargs['node_data_file']

    
