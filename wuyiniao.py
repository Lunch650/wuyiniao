# encoding: utf-8
import time
import requests
import BeautifulSoup
import Queue
import threading
import MySQLdb
import os
from collections import Iterable
from bs4 import BeautifulSoup

def insertComic(comic_name,comic_url):
	conn = MySQLdb.connect(
	host = 'localhost',
	user = 'root',
	db = 'sexcomic',
	)
	cur = conn.cursor()
	sql = 'INSERT INTO comics(comic_name,comic_url) VALUES(%s,%s)'
	cur.execute(sql,(comic_name,comic_url))
	cur.close()
	conn.commit()
	conn.close()

def getname(comic_temp):
	return str(time.time())[:10].strip()
	# if len(comic_temp.split('之')) > 1:
	# 	comic_modify =  ''.join(comic_temp.split('之',1)[1:])
	# elif len(comic_temp.split('：')) > 1:
	# 	if len(comic_temp.split(':')) > 1:
	# 		comic_modify = ''.join(comic_temp.split(':')[-1:])
	# 	else:
	# 		comic_modify = ''.join(comic_temp.split('：')[-1:])
	# elif len(comic_temp.split('漫画大全')) > 1:
	# 	comic_modify = ''.join(comic_temp.split('漫画大全',1)[1:])
	# else:
	# 	comic_modify = comic_temp
	# if comic_modify == '':
	# 	return str(time.time())[:10]
	# else:
		

def downloadcomic(comic_url):
	print 'the downloadcomic:',comic_url,'is running...'
	comic = requests.get(comic_url,headers,timeout=60)
	comic_soup = BeautifulSoup(comic.content,'lxml',from_encoding='gb18030')
	try:
		comic_pagelist = int(comic_soup.find('ul',class_='pagelist').li.a.get_text()[1:-3])
	except Exception as e:
		print 'the Error:',e
		return None
	comic_name = getname(comic_soup.h1.get_text().encode('utf-8'))#截取漫画名称，如果为空则名称为当前时间戳
	comic_path = LOG_PATH[:-13]+comic_name
	
	try:
		print 'try to mkdir'
		mkdircomic(comic_path,comic_name)
	except:
		'can\'t mkdir:'+comic_name
		return None

	for singlepage in range(2,comic_pagelist+1):
		singlepage_url = comic_url[:-5]+'_'+str(singlepage)+'.html'
		comic_page = requests.get(singlepage_url,headers)
		comic_page_soup = BeautifulSoup(comic_page.content,'lxml',from_encoding='gb18030')
		img_url = comic_page_soup.find(id='imgshow').img['src']
		img_name = str(singlepage)
		while len(img_name)<3:
			img_name = '0'+img_name
		img_path = comic_path+'\\'+img_name+'.jpg'
		try:
			img_r = requests.get(img_url)
			img_down = open(img_path,'wb')
			img_down.write(img_r.content)
			img_down.close()
		except Exception as e:
			print 'can\' down img'+comic_path+'\\'+img_name
			print 'Error:',e

def createthread(cate_comics):
	q = Queue.Queue()
	threads = []
	threads_count = 3
	init_thread = cate_comics[:threads_count]
	for comic_url in cate_comics[threads_count:len(cate_comics)]:
		q.put(comic_url)

	for i in range(threads_count):
		t = threading.Thread(target=downloadcomic,args=(init_thread[i],))
		threads.append(t)

	for i in range(threads_count):
		threads[i].start()
		time.sleep(1)
		print 'the thread',i,'is running...'

	while not q.empty():
		for i in range(threads_count):
			if not threads[i].isAlive():
				print 'the Thread',i,'is dead...'
				threads.pop(i)
				new_url = q.get()
				t = threading.Thread(target=downloadcomic,args=(new_url,))
				threads.insert(i,t)
				threads[i].start()
		time.sleep(30)

	for i in range(threads_count):
		threads[i].join()

def mkdircomic(comic_path,comic_name):
	#---------#创建漫画文件夹#---------#
	if not os.path.exists(comic_path):
		os.mkdir(comic_path)


def findcomic(page_url):
	###获取该页面中每个漫画地址###
	page = requests.get(page_url,headers)
	pagesoup = BeautifulSoup(page.content,'lxml',from_encoding='gb18030')
	comics = pagesoup.find_all('a',class_='pic show')
	for comic in comics:
		cate_comics.append('http://www.xiemanwang.com'+comic['href'].strip())

def main():
	global cate_comics
	global LOG_PATH
	LOG_PATH = 'E:\\Lunch\\Demo\\Python\\Crawl\\Comics\\comic_log.txt'
	comics_sort = {'benzi':'9',
	'lifanku':'15',
	'gongkou':'16',
	'shaonv':'2',
	'shenshi':'18',
	'wuyiniao':'14',
	}
	url = 'http://www.xiemanwang.com/benzi/'

	r = requests.get(url,headers)
	soup = BeautifulSoup(r.content,'lxml',from_encoding="gb18030")
	cate_comics = []
	pagenum = int(soup.find('span',class_='pageinfo').strong.get_text())#获取类别下共有多少页

	for i in range(pagenum):#获取该类别下所有漫画并存入cate_comics列表
		page_url = url+'list_'+comics_sort['benzi']+'_'+str(i+1)+'.html'#组装页面地址
		print 'Num.'+str(i)+':'+page_url
		try:
			findcomic(page_url)
		except:
			print page_url+' wrong'
			continue

	createthread(cate_comics)
	# for i in range(threads_count):
	# 	page_url = url[:-6]+str(i+1)+'.html'
	# 	t = threading.Thread(target=findcomic,args=(page_url,))
	# 	threads.append(t)
	# for i in range(threads_count):
	# 	threads[i].start()
	# for i in range(threads_count):
	# 	threads[i].join()
#url[:-6]+str(i)+'.html'


	#hrefs = soup.find_all('a',class_='pic show')

if __name__ == '__main__':
	global headers
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Connection':'keep-alive',
	'Accept-Encoding':'gzip,deflate',
	}
	main()
