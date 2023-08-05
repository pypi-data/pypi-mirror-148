#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/26 11:25
# @Author  : Adyan
# @File    : redis_conn.py


import json
import time

import redis


class ReidsClient(object):
    """
    ReidsClient(
        name='proxy',
        config={ "HOST": "ip", "PORT": 6379, "DB": 11 }
        )
    ree.get(2)
    """

    def __init__(self, config, name=None):
        """
        :param config:  { "HOST": "ip", "PORT": 6379, "DB": 11 }
        :param name:  "name"
        """
        host = config.get('HOST', 'localhost')
        port = config.get('PORT', 6379)
        db = config.get('DB', 0)
        password = config.get('PAW', None)
        if password:
            self.redis_conn = redis.Redis(host=host, port=port, password=password)
        else:
            self.redis_conn = redis.Redis(host=host, port=port, db=db)
        self.name = name

    def get(self, count):
        """
        获取count个数据，同时将这些数据删除
        :param count:
        :return:
        """
        lst = [i.decode('utf-8') for i in self.redis_conn.lrange(self.name, 0, count - 1)]
        self.redis_conn.ltrim(self.name, count, -1)
        return lst

    def cyclic(self):
        """

        :return:
        """
        value = self.get(1)
        for i in value:
            tim = int(list(json.loads(i).keys())[0])
            if int(time.time()) < tim + 3600:
                self.put(i)
        return value[0]

    def put(self, param):
        """
        尾部添加一个数据
        :param param:
        :return:
        """
        self.redis_conn.rpush(self.name, param)

    def sput(self, param):
        """
        :param param:
        :return:
        """
        self.redis_conn.sadd(self.name, param)

    @property
    def queue_len(self):
        try:
            return self.redis_conn.llen(self.name)
        except:
            return self.redis_conn.scard(self.name)
