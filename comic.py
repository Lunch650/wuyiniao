#!python3
# coding=utf8
import requests
import os
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
        # 返回漫画页数
        return int(self.comic_index_content.find('ul', class_='pagelist').li.text[1:-3])

    def title(self):
        # 返回漫画标题
        return self.comic_index_content.find('h1').text

    def pages(self):
        # 返回漫画各页地址，返回的数据格式为List
        pic_pages = [self.comic_url]
        for num in range(2, self.comic_num_pages + 1):
            pic_pages.append(self.comic_url[:-5] + '_' + str(num) + '.html')
        return pic_pages

    def mkdir(self):
        # 创建文件夹
        root_path = 'E:\\Lunch\\Comics\\wuyiniao\\'
        if not os.path.exists(root_path + self.comic_id):
            try:
                os.mkdir(root_path + self.comic_id)
            except OSError as e:
                print('创建文件夹失败,原因:', e)
        else:
            print(self.comic_id + '的文件夹已存在')


    @staticmethod
    def pic_from_page(url):
        # 返回页面中的图片地址
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
    c = Comic('7391')
    print(c.comic_num_pages)
    print(c.comic_title)
    pic_content = requests.get(Comic.pic_from_page(c.pages()[0]), stream=True)
    with open('E:\\Lunch\\Comics\\wuyiniao\\' + c.comic_id + '1.jpg', 'wb') as pic_file:
        for p in pic_content:
            print(p)

