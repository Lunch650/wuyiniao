#!python3
# coding=utf8
import requests
from bs4 import BeautifulSoup


class Comic(object):
    root = 'http://www.mhkkm.la/riben/wuyiniao/'

    def __init__(self, comic_id):
        self.id = comic_id
        self.url = Comic.root + self.id + '.html'
        self.num_pages = int(Comic.content_comic_index(self.url).find('ul', class_='pagelist').li.text[1:-3])
        self.title = Comic.content_comic_index(self.url).find('h1').text

    @staticmethod
    def content_comic_index(url):
        r = None
        while r is None:
            try:
                r = requests.get(url, timeout=5)
            except requests.Timeout:
                print("Timeout,retry")
        return BeautifulSoup(r.content, 'lxml')


if __name__ == '__main__':
    c = Comic('7390')
    print(c.num_pages)