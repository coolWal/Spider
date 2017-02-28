#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# __author__ = 'liuyuantuo@baidu.com'
import os
import ConfigParser


class Configure(object):
    @staticmethod
    def parser(configure_path):
        """
        Brief:
            解析配置文件

        Args:
            self.configure_path: 用户输入的文件名

        Returns:
            返回一个dict
            例如{'section': {'option1':'value1', 'option2':'value2'}}
        """
        assert (os.path.isfile(configure_path)), "[error]: file: %s is not exist!" % str(configure_path)
        config_hd = ConfigParser.ConfigParser()
        config_hd.read(configure_path)
        section_list = config_hd.sections()
        config_dict = {}
        for section in section_list:
            section_dict = {}
            option_list = config_hd.options(section)
            for option in option_list:
                section_dict.setdefault(option, config_hd.get(section, option))
            config_dict.setdefault(section, section_dict)
        return config_dict
