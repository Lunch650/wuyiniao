#!python3
# coding=utf8
import requests
import os
import time
from bs4 import BeautifulSoup


class Comic(object):
    root = 'http://www.mhkkm.la/riben/wuyiniao/'
    fold_path = 'E:\\Lunch\\Comics\\wuyiniao\\'
    sess = requests.Session()

    def __init__(self, comic_id):
        self.comic_id = comic_id
        self.comic_url = Comic.root + self.comic_id + '.html'
        self.comic_index_content = Comic.page_soup(self.comic_url)
        self.comic_num_pages = self.num_pages()
        self.comic_title = self.title()

    @staticmethod
    def pages_url():
        # 返回漫画列表的地址
        pages_url = [Comic.root + 'list_49_1.html']
        total_page = Comic.page_soup(pages_url[0]).find('select').find_all('option')[-1].get_text()
        for page in range(2, int(total_page) + 1):
            pages_url.append(pages_url[0][:-6] + str(page) + '.html')
        return pages_url

    @staticmethod
    def comics_id():
        comics_id = []
        for page_url in Comic.pages_url():
            comics_a = Comic.page_soup(page_url).find_all('a', class_='pic show')
            for comic_a in comics_a:
                comics_id.append(comic_a['href'][16:-5])
        return comics_id

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
                print(self.comic_id + '文件夹创建成功')
            except OSError as e:
                print('创建文件夹失败,原因:', e)
        else:
            print(self.comic_id + '的文件夹已存在,不用创建了')

    def count_pics(self):
        return len(os.listdir(Comic.fold_path + self.comic_id))

    def pic_down(self):
        # 下载图片
        if self.comic_num_pages == self.count_pics():
            print(self.comic_id + '共' + str(self.comic_num_pages) + '张图片早就下载完毕了')
        else:
            pics = self.pics()
            pic_content = None
            for index, pic in enumerate(pics):
                file_name = Comic.file_name(str(index), self.comic_id)
                if not os.path.exists(Comic.fold_path + self.comic_id + '\\' + file_name):
                    while pic_content is None:
                        try:
                            pic_content = Comic.sess.get(pic)
                        except requests.Timeout:
                            print('pic,Timeout,Retry')
                    with open(Comic.fold_path + self.comic_id + '\\' + file_name, 'wb') as file:
                        for content in pic_content:
                            file.write(content)
                            pic_content = None
                else:
                    print(file_name + '存在,不用创建了')

    def pics(self):
        # 返回页面中的图片地址
        pic_urls = []
        for page in self.pages():
            pic_urls.append(Comic.page_soup(page).
                            select('span#t_right')[0].
                            next_sibling.next_sibling['src']
                            )
        return pic_urls

    @staticmethod
    def page_soup(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/55.0.2883.87 Safari/537.36',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip,deflate',
        }
        r = None
        while r is None:
            try:
                r = Comic.sess.get(url, headers=headers, timeout=5)
            except requests.Timeout:
                print(url, 'Timeout,sleep(3),retry')
            except requests.ConnectionError:
                print(url, 'ConnErr,sleep(3),retry')
            time.sleep(5)
        return BeautifulSoup(r.content, 'lxml', from_encoding='gb18030')

    @staticmethod
    def file_name(page, comic_id):
        while len(page) < 3:
            page = '0' + page
        return comic_id + '_' + page + '.jpg'


if __name__ == '__main__':
    for c_id in Comic.comics_id():
        c = Comic(str(c_id))
        print(c.comic_id + '任务启动')
        c.mkdir()
        c.pic_down()
