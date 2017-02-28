#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# __author__ = 'liuyuantuo@baidu.com'
"""
    该类是继承client，从本地导入数据相关
"""


import json
import sys
from argsparse.common import ArgsParse
from upload.client import Client


class LocalDataClient(Client):
    """
        从本地来读取相关文件，然后将对应的数据进行上传
    """
    def __init__(self):
        super(self.__class__, self).__init__()

    def get_source_data(self, **kwargs):
        """
            重载获取source data的函数，从本地文件中获取
            :args
                pdf_file: 输入pdf的文件地址，
                node_file: 输入node解析出来的文件地址，该文件应该是一个Json文件
        """
        # node file解析，获取到指定的值
        fd = open(kwargs['node_file'])
        # 只允许里面存在一行数据，不允许存在多行数据
        page_content = fd.readline()
        # 替换回车符号
        page_content = page_content.replace("\n", "")
        page_content_dict = json.loads(page_content)
        # page_content_dict = eval(page_content)

        # 拼接对应的字段
        source_data = dict(
            pdf_file=kwargs['pdf_file'],
            image_list=page_content_dict['image_list'],
            source_url=page_content_dict['source_url'],
            title=page_content_dict['title'],
            description=page_content_dict['description'],
            content=page_content_dict['content'],
            tags=page_content_dict['tags'],
            cover=page_content_dict['cover'],
            task=page_content_dict['task'],
            publisher=page_content_dict['publisher'],
            publish_time=page_content_dict['publish_time'],
            list_url=page_content_dict['list_url'],
        )

        return source_data

if __name__ == "__main__":
    local_data_client = LocalDataClient()
    local_data_client.upload(db=sys.argv[1],
                             module=sys.argv[2],
                             pdf_file=sys.argv[3],
                             node_file=sys.argv[4])
