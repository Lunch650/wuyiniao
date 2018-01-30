#!python3
# coding=utf8
import pymongo

class db_util(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)