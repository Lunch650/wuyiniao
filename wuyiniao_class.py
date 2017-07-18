# -*- coding:utf-8 -*-  
import requests
import Queue
import os
import time
from bs4 import BeautifulSoup

class Comic():
	
	def __init__(self,comic_url):
		#初始化，获取漫画名字及页数
		self.comic_url = comic_url

		def comic_soup():
			comic = requests.get(self.comic_url,HEADERS)
			comic_soup = BeautifulSoup(comic.content,'lxml',from_encoding='gb18030')
			return comic_soup

		def cutname():
			temp_name = comic_soup().h1.get_text().encode('utf-8')
			filterwords = ['：',':','之','漫画','大全','全集','无翼鸟','_']
			for filterword in filterwords:
				if temp_name.split(filterword,1) > 1:
					temp_name = temp_name.split(filterword)[-1]
			if temp_name == '':
				return str(time.time())[:10].strip()
			else:
				return temp_name

		self.comic_name = cutname().decode('utf-8')
		self.comic_page = int(comic_soup().find('ul',class_='pagelist').li.a.get_text()[1:-3])
		self.comic_path = COMIC_ROOT_PATH+self.comic_name+'\\'
		self.isfinished = False

	def mkcomicdir(self):
		if os.path.exists(self.comic_path):
			for x in os.walk(self.comic_path):
				pass
			if len(x[2]) == self.comic_page:
				self.isfinished = True
				return None
		else:
			try:
				os.makedirs(self.comic_path)
			except:
				print 'wrong'

	def getpages(self):
		for x in range(2,self.comic_page):
			page_url = ''.join(list(self.comic_url).insert(-5,'_'+str(x)))
			try:
				page = requests.get()



if __name__ == '__main__':
	global HEADERS,COMIC_ROOT_PATH
	HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Connection':'keep-alive',
	'Accept-Encoding':'gzip,deflate',
	}
	COMIC_ROOT_PATH = 'E:\\Lunch\\Demo\\Python\\Crawl\\Comics\\'

	pre_url = 'http://www.mhkkm.com/riben/wuyiniao/list_49_'
	index = requests.get('http://www.mhkkm.com/riben/wuyiniao/')
	soup = BeautifulSoup(index.content,'lxml')
	pages_num = int(soup.find('span',class_='pageinfo').strong.get_text())
	comic_urls = []
	for x in range(1,2):
		page_url = pre_url+str(x)+'.html'
		page = requests.get(page_url,HEADERS)
		page_comics = BeautifulSoup(page.content,'lxml').find_all('a',class_='pic show')
		for page_comic in page_comics:
			comic_url = 'http://www.mhkkm.com'+page_comic['href']
			comic_urls.append(comic_url)
	comic_urls = list(set(comic_urls))   #去除重复的超链接
	for comic_url in comic_urls:
		mycomic = Comic(comic_url)
		mycomic.mkcomicdir()
