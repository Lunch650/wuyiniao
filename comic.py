#!python3
# coding=utf8

class Comic(object):
    root = 'http://www.mhkkm.la/riben/wuyiniao/'
    def __init__(self, id):
        self.comic_id = id
        self.comic_url = Comic.root + self.comic_id + '.html'
        self.comic_num_pages = -1
        self.comic_title = ''

    def content_comic_index(self):
        pass