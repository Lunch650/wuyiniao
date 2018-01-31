#!python3
# coding=utf8
import pymongo


class DBUtil(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)


if __name__ == '__main__':
    util = DBUtil()
    db = util.conn.comic
