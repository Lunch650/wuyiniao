#!python3
# coding=utf8
import requests
import os
from bs4 import BeautifulSoup


class Comic(object):
    root = 'http://www.mhkkm.la/riben/wuyiniao/'
    fold_path = 'E:\\Lunch\\Comics\\wuyiniao\\'

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
        if not os.path.exists(Comic.fold_path + self.comic_id):
            try:
                os.mkdir(Comic.fold_path + self.comic_id)
            except OSError as e:
                print('创建文件夹失败,原因:', e)
        else:
            print(self.comic_id + '的文件夹已存在,不用创建了')

    def pic_down(self):
        # 下载图片
        pics = self.pics()
        pic_content = None
        s = requests.session()
        for index, pic in enumerate(pics):
            while pic_content is None:
                try:
                    pic_content = s.get(pic, stream=True)
                except requests.Timeout:
                    print('pic,Timeout,Retry')
            with open(Comic.fold_path + self.comic_id + '\\' + Comic.file_name(str(index)) + '.jpg', 'wb') as file:
                for content in pic_content:
                    file.write(content)
            pic_content = None

    def pics(self):
        # 返回页面中的图片地址
        pic_urls = []
        for page in self.pages():
            pic_urls.append(Comic.page_soup(page).select('span#t_right')[0].next_sibling.next_sibling['src'])
        return pic_urls

    @staticmethod
    def page_soup(url):
        r = None
        while r is None:
            try:
                r = requests.get(url, timeout=5)
            except requests.Timeout:
                print(url, "Timeout,retry")
        return BeautifulSoup(r.content, 'lxml')

    @staticmethod
    def file_name(page):
        while len(page) < 3:
            page = '0' + page
        return page

if __name__ == '__main__':
    for i in range(4330, 4331):
        c = Comic(str(i))
        c.mkdir()
        c.pic_down()