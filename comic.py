#!python3
# coding=utf8

class Comic(object):
    root = 'http://www.mhkkm.la/riben/wuyiniao/'
    def __init__(self):
        self.comic_id = ''
        self.comic_url = Comic.root + self.comic_id + '.html'

    def content_comic_index(self):
        pass