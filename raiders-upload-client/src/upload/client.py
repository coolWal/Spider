#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# __author__ = 'liuyuantuo@baidu.com'

"""
    基础的client类
"""

import os
import requests
import hashlib
import time
import socket
import pymongo
from common.argsparse import ArgsParser
from common.configure import Configure
from common.logger import Logger
from storage.mongo import DDL
from storage.mongo import DML
from storage.file import File


class Client(ArgsParser, Logger):
    """
        基类包括两个功能：
        1. 初始化mongo资源过程，主要用于新品类建设的时候，设置资源
        2. 基于已经建立的品类，进行资源的上传
        *************************************************************
        整体上传流程基类，包括如下部分：
        1.初始化本地资源，主要是load configure相关
        2.根据指定的上传类型，判断是从什么地方读取数据，需要支持从spider中，本地，外部接口读取数据
        3.将图片和pdf数据存储到本地的web server的静态资源中
        4.将所有的数据存储到mongodb中
        5.向web server发起post请求，将相关地址代入
        *************************************************************
        初始化mongo db库的过程：
        1.设置db和collections
        2.设置索引
    """
    def __init__(self):
        # 这里显式调用初始化
        ArgsParser.__init__(self)
        Logger.__init__(self)
        code_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # 获取到配置文件的目录地址
        self.configure_path = os.path.dirname(code_path) + os.sep + "conf"

    def storage_init(self, **kwargs):
        """
            资源初始化，用于mongo的初始化，如果后期非mongo的，可以重载这个函数
        """
        storage_configure_file = self.configure_path + os.sep + "storage.ini"
        # 如果输入的kwargs为空，默认直接从配置里面取出来
        if len(kwargs) == 0:
            storage_configure = Configure.parser(storage_configure_file)
        else:
            storage_configure = kwargs['storage_configure']
        # 建立与db的链接
        ddl_instance = DDL(host=storage_configure['mongo']['host'],
                           port=storage_configure['mongo']['port'])
        # 进行初始化的操作，主要是建库相关，默认的方法支持的是mongo的建库
        ddl_instance.add_index(kwargs['db'], kwargs['collection'], kwargs['index'])

    def get_source_data(self, **kwargs):
        """
            该函数用于重载，继承该类后，直接重载该函数，即可实现不同的输入源
        """
        pass

    def save_images(self, module, image_list, uuid):
        """
            该函数用于存储图片文件相关，放入到client所在机器的server的静态资源目录下
            :arg
                image_list: 图片地址，默认都是url，有需要可以进行重构
                module: 用来标识指定的module名字的，比如攻略可以指定为游戏品类等
                uuid: 作为唯一的标识用来处理
            :return
                local_path_list: 返回的是本地的存储地址，用于标识自己所处的web server的静态资源位置
                                 注意，这里是按照图片顺序进行排列，所以之后一定要严格按照有序性来上传Hiphotos
        """
        assert isinstance(image_list, list)
        storage_configure_file = self.configure_path + os.sep + "storage.ini"
        storage_configure = Configure.parser(storage_configure_file)
        image_index = 0
        local_path_list = []
        for image_url in image_list:
            print image_url
            response = requests.get(image_url)
            content = response.content
            # 图片名字以url的md5来命名
            image_index += 1
            local_path = storage_configure['static_resource']['image'] + os.sep + module
            web_path_prefix = storage_configure['static_resource']['image_web_prefix']
            if not os.path.isdir(local_path):
                os.mkdir(local_path)
            # 存储外网的图片到本地
            local_file = File.storage_in_local("{}_{}.pic".format(uuid, image_index),
                                               content,
                                               local_path)
            local_file = local_file.replace(web_path_prefix, "")
            local_file = storage_configure['static_resource']['host'] + local_file
            # 得到所有图片地址
            local_path_list.append(local_file)
        return local_path_list

    def save_pdf(self, module, pdf_file, uuid):
        """
            该函数用于存储pdf相关，需要注意的是，考虑到pdf都比较大，且可以重新生成，指定了pdf之后，该函数会直接move走
            :arg
                pdf_file: 输入的pdf文件
                module: 用来标识指定的module名字的，比如攻略可以指定为游戏品类等
                uuid: 作为文件前缀的唯一标识
            :return
                local_path_list: 返回的是本地的存储地址，用于标识自己所处的web server的静态资源位置
                                 注意，这里是按照图片顺序进行排列，所以之后一定要严格按照有序性来上传Hiphotos
        """
        assert os.path.isfile(pdf_file)
        storage_configure_file = self.configure_path + os.sep + "storage.ini"
        storage_configure = Configure.parser(storage_configure_file)
        local_path = storage_configure['static_resource']['pdf'] + os.sep + module
        web_path_prefix = storage_configure['static_resource']['pdf_web_prefix']
        # 移动pdf文件到指定的目录下
        local_file = File.storage_copy_file(pdf_file, local_path,
                                            "{}_{}".format(uuid, os.path.basename(pdf_file)))
        # 去掉前缀
        local_file = local_file.replace(web_path_prefix, "")
        local_file = storage_configure['static_resource']['host'] + local_file
        return local_file

    def insert_mongo(self, db, collection, image_urls, pdf_url, args):
        """
            该函数用于将处理后的数据存储到mongo中，包括image url和pdf url
            :arg
                image_urls: 图片的存储list
                pdf_url: pdf的存储地址
                args: 之前node解析出来的数据，以及一些其他数据
            :return
                object_id: 返回mongo的对象ID，用于Post请求
        """
        storage_configure_file = self.configure_path + os.sep + "storage.ini"
        storage_configure = Configure.parser(storage_configure_file)
        ddl_instance = DDL(host=storage_configure['mongo']['host'],
                           port=storage_configure['mongo']['port'])
        dml_instance = DML(host=storage_configure['mongo']['host'],
                           port=storage_configure['mongo']['port'])
        now_time = int(time.time())
        values = dict(
            source_url=args['source_url'],
            title=args['title'],
            description=args['description'],
            # 注意这里存储的是转储到客户端的
            client_image_list=image_urls,
            # 这里存储的是原始的链接地址
            original_image_list=args['image_list'],
            pdf_url=pdf_url,
            content=args['content'],
            tags=args['tags'],
            cover=args['cover'],
            publisher=args['publisher'],
            publish_time=args['publish_time'],
            task=args['task'],
            # 新增列表页url
            list_url=args['list_url'],
            # 新增状态码，初始化的状态都是0，server init data之后会重置值
            status=0,
            # 新增修改后的content，用于server端进行回调修改MONGODB，减小工作量
            server_deal_content='',
            # 新增hostname，用于标记客户端
            client_host=socket.getfqdn(socket.gethostname()),
            # 新增创建时间和更新时间，在客户端回调的时候，也需要修改更新时间
            create_time=now_time,
            update_time=now_time,
        )
        object_id = dml_instance.add(db, collection, values)
        # 对source url加入唯一索引
        ddl_instance.add_index(db, collection, 'source_url', is_unique=True)
        # 对其他字段加入普通索引，但是这里注意要加入升序，降序字段
        ddl_instance.add_index(db, collection, [('status', pymongo.DESCENDING),
                                                ('create_time', pymongo.ASCENDING),
                                                ('update_time', pymongo.ASCENDING)])
        return str(object_id)

    def request_server(self, db, collection, object_id):
        """
            该函数用于将处理后的数据存储到mongo中，包括image url和pdf url
            :arg
                image_urls: 图片的存储list
                pdf_url: pdf的存储地址
                args: 之前node解析出来的数据，以及一些其他数据
            :return
                object_id: 返回mongo的对象ID，用于Post请求
        """
        data = dict(
            db=db,
            collection=collection,
            object_id=object_id,
        )
        business_configure_file = self.configure_path + os.sep + "business.ini"
        business_configure = Configure.parser(business_configure_file)
        server_url = business_configure['server']['host']
        ret = requests.post(server_url, data)
        print ret.content

    def upload(self, **kwargs):
        """
            进行资源的上传操作的总入口，其框架是不会发生变化的，可以对内部调用的函数进行重载即可
        """
        # 读取待上传的数据
        source_data = self.get_source_data(**kwargs)
        url_md5sum = hashlib.md5()
        url_md5sum.update(source_data['source_url'])
        url_md5sum = url_md5sum.hexdigest()
        # 存储图片
        image_urls = self.save_images(kwargs['module'], source_data['image_list'], url_md5sum)
        # 存储pdf
        pdf_url = self.save_pdf(kwargs['module'], source_data['pdf_file'], url_md5sum)
        # 存储原始数据到mongo中
        object_id = self.insert_mongo(kwargs['db'],
                                      kwargs['module'],
                                      image_urls,
                                      pdf_url,
                                      source_data)
        # 发起post请求，等待业务流程即可，请求过去之后，可以考虑在后面是异步过程
        self.request_server(kwargs['db'], kwargs['module'], object_id)

