#!python3
# coding=utf8
import requests
from bs4 import BeautifulSoup


class Comic(object):
    root = 'http://www.mhkkm.la/riben/wuyiniao/'

    def __init__(self, comic_id):
        self.comic_id = comic_id
        self.comic_url = Comic.root + self.comic_id + '.html'
        self.comic_index_content = Comic.page_soup(self.comic_url)
        self.comic_num_pages = self.num_pages()
        self.comic_title = self.title()

    def num_pages(self):
        return int(self.comic_index_content.find('ul', class_='pagelist').li.text[1:-3])

    def title(self):
        return self.comic_index_content.find('h1').text

    def pic_pages(self):
        pic_pages = [self.comic_url]
        for num in range(2, self.comic_num_pages + 1):
            pic_pages.append(self.comic_url[:-5] + '_' + str(num) + '.html')
        return pic_pages

    @staticmethod
    def get_pic_url(url):
        return Comic.page_soup(url).select('span#t_right')[0].next_sibling.next_sibling['src']

    @staticmethod
    def page_soup(url):
        r = None
        while r is None:
            try:
                r = requests.get(url, timeout=5)
            except requests.Timeout:
                print(url, "Timeout,retry")
        return BeautifulSoup(r.content, 'lxml')


if __name__ == '__main__':
    c = Comic('7390')
    print(c.comic_num_pages)
    print(c.comic_title)
    print(Comic.get_pic_url(c.comic_url))
