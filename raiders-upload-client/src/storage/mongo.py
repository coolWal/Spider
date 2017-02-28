#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# __author__ = 'liuyuantuo@baidu.com'
"""
    mongo操作基础类
"""

import pymongo


class Base(object):
    """
        该类是用于进行链接mongo db
        主要是在mongo中查询数据以及插入数据
    """
    def __init__(self, **kwargs):
        self.client = pymongo.MongoClient(host=kwargs['host'], port=int(kwargs['port']))


class DDL(Base):
    """
        该类的方法是DDL相关，用于建立db和collection
        需要注意的是，该DDL不需要CRATE方法，因为会自动建立，在DML中不要做DB和COLLECTIONS的强校验即可
    """
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def drop(self, **kwargs):
        """
            :desc
                create方法，用于建立数据库和collections
            :arg
                db: 数据库名
                collection: 数据集合名
                key: 检索的key
                object_id: mongo中的对象ID，与上面的key是或关系，两者需要至少存在一个
            :return
                values: 返还的是在mongo中存储的数据
        """
        if 'db' in kwargs.keys():
            # 使用该方法就能直接建立db
            self.client.drop_database(kwargs['db'])
        elif 'collection' in kwargs.keys():
            self.client[kwargs['db']].drop_collection(kwargs['collection'])

    def add_index(self, db, collection, index_keys, is_unique=False):
        """
            :desc
                添加index方法，在collection上建立索引
            :arg
                db: 数据库名
                collection: 数据集合名
                index_keys: 使用的索引名称，可以是string也可以是list，但是list的元素一定要大于两个
                is_unique: 索引是否唯一
            :return
                values: 返还的是在mongo中存储的数据
        """
        # 进行db和collection的相关处理
        self.client[db][collection].ensure_index(index_keys, unique=is_unique)

class DML(Base):
    """
        该类是DML方法，用于对数据集合的操作
    """
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def _params_check(self, db, collection):
        """
            :arg
                db: 数据库名
                collection: 数据集合名
                key: 检索的key
                object_id: mongo中的对象ID，与上面的key是或关系，两者需要至少存在一个
            :return
                values: 返还的是在mongo中存储的数据
        """
        # 检索相关名称
        db_list = self.client.database_names()
        if db not in db_list:
            raise Exception("can not find db:{} in mongo!".format(db))
        collection_list = self.client[db].collection_names()
        if collection not in collection_list:
            raise Exception("can not find collection:{} in mongo".format(collection))

    def get(self, db, collection, key=None, object_id=None):
        """
            :desc
                get方法
            :arg
                db: 数据库名
                collection: 数据集合名
                key: 检索的key
                object_id: mongo中的对象ID，与上面的key是或关系，两者需要至少存在一个
            :return
                values: 返还的是在mongo中存储的数据
        """
        # 参数检查
        self._params_check(db, collection)
        collect_info = self.client[db][collection]
        # 加入相关类型判断，直接使用断言来断言类型即可
        assert key is None or isinstance(key, dict)

        if key is None and object_id is None:
            raise Exception("key and object id can not be all empty!")

        # 检索对应的内容
        if key is not None:
            return collect_info.find(key)
        else:
            return collect_info.find(dict(_id=object_id))

    def add(self, db, collection, values):
        """
            :desc
                add方法，向mongo db插入一条记录
            :arg
                db: 数据库名
                collection: 集合名
                values: 需要塞入相关，可以是dict也可以是json字符串
            :return
                object_id: 返回的对象名
        """
        # self._params_check(db, collection)
        assert isinstance(values, dict)
        # 插入数据集合中
        collect_info = self.client[db][collection]
        object_id = collect_info.insert_one(values)
        return object_id.inserted_id

    def update(self, db, collection, query, values):
        """
            :desc
                update方法，更新mongo db的记录
            :arg
                db: 数据库名
                collection: 集合名
                query: 查询条件，需要是dict传入
                values: 需要塞入相关，可以是dict也可以是json字符串
            :return
                object_id: 返回的对象名
        """
        self._params_check(db, collection)
        assert isinstance(values, dict) and isinstance(query, dict)
        # 插入数据集合中
        collect_info = self.client[db][collection]
        collect_info.update(query, values)

    def delete(self, db, collection, query):
        """
            :desc
                delete方法，删除mongo db的一条记录
            :arg
                db: 数据库名
                collection: 集合名
                query: 查询条件，需要是dict传入
                values: 需要塞入相关，可以是dict也可以是json字符串
            :return
                object_id: 返回的对象名
        """
        self._params_check(db, collection)
        # 插入数据集合中
        collect_info = self.client[db][collection]
        collect_info.remove(query)