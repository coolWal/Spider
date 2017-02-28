#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# __author__ = 'liuyuantuo@baidu.com'
import os
import time


class File(object):
    """
        该类用于处理存储在本地文件相关
        主要存储两种类型的文件到本地：
        1.image file
        2.pdf file
    """

    @staticmethod
    def storage_in_local(file_name, content, local_path):
        """
            将文件存储到本地
            :arg
                local_path: 输入的本地存储路径
                content: 需要存储的文档内容(直接拼接好的string即可)
                file_name: 需要被存储的文件名，对应上对应的资源相关
            :return
                file_location: 返回的是文件的存储地址
        """
        if not os.path.isdir(local_path):
            os.mkdir(local_path)
        # 拼接当天0点的时间戳，所有的资源
        time_path = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 判断当天的目录是否存在
        local_path = local_path + os.sep + time_path
        try:
            if not os.path.isdir(local_path):
                os.mkdir(local_path)
        except Exception as e:
            print "[error]: create local save path failed!", e

        file_location = local_path + os.sep + file_name
        # 存储
        fd = open(file_location, "w")
        fd.write(content)
        fd.close()
        return file_location

    @staticmethod
    def storage_move_file(move_file, local_path, file_name=''):
        """
            将文件存储到本地
            :arg
                local_path: 输入的本地存储路径
                content: 需要存储的文档内容(直接拼接好的string即可)
                file_name: 需要被存储的文件名，对应上对应的资源相关
            :return
                file_location: 返回的是文件的存储地址
        """
        assert os.path.isfile(move_file)
        if not os.path.isdir(local_path):
            os.mkdir(local_path)
        # 拼接当天0点的时间戳，所有的资源
        time_path = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 判断当天的目录是否存在
        local_path = local_path + os.sep + time_path
        try:
            if not os.path.isdir(local_path):
                os.mkdir(local_path)
        except Exception as e:
            print "[error]: create local save path failed!", e

        file_location = local_path + os.sep + file_name
        err_no = os.system("mv {} {}".format(move_file, file_location))
        if 0 != err_no:
            raise Exception("mv file:{} to {} failed!".format(move_file, file_location))
        return file_location

    @staticmethod
    def storage_copy_file(copy_file, local_path, file_name=''):
        """
            将文件存储到本地
            :arg
                local_path: 输入的本地存储路径
                content: 需要存储的文档内容(直接拼接好的string即可)
                file_name: 需要被存储的文件名，对应上对应的资源相关
            :return
                file_location: 返回的是文件的存储地址
        """
        assert os.path.isfile(copy_file)
        if not os.path.isdir(local_path):
            os.mkdir(local_path)
        # 拼接当天0点的时间戳，所有的资源
        time_path = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 判断当天的目录是否存在
        local_path = local_path + os.sep + time_path
        try:
            if not os.path.isdir(local_path):
                os.mkdir(local_path)
        except Exception as e:
            print "[error]: create local save path failed!", e

        # 如果发现file name为空，直接用输入的pdf的后缀作为相关名字即可
        if len(file_name) == 0:
            file_name = os.path.basename(copy_file)
        file_location = local_path + os.sep + file_name
        err_no = os.system("cp {} {}".format(copy_file, file_location))
        if 0 != err_no:
            raise Exception("copy file:{} to {} failed!".format(copy_file, file_location))
        return file_location

    @staticmethod
    def storage_in_web(**kwargs):
        """
            todo: 用于upload到web server上，然后从server上获取即可
        """
        pass