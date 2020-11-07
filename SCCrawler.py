#coding: utf-8

import requests
import time
from bs4 import BeautifulSoup as bs
from SCPageParser import parsePage
import psycopg2

"""
Function "crawl()"
Performs crawling on https://www.socialchange.kr
Parse list page first, take each url of documents, 
then performs crawling on each document.

* Parameters
- endNumber (Integer): 
    Define termination point of crawling process. If it is provided, crawling process ends on that page number.
    Default value = -1.
"""
def crawl(endNumber = -1):

	#Try DB connection on PostgreSQL server.
	try:
		conn = psycopg2.connect(database="dsidb", user="postgres", password="developer#!", host="121.129.214.6", port="8432")
		conn.autocommit = True
		cur = conn.cursor()
	except Exception as inst:
		print(inst)
		return 1

	#Initialize each varaibles
	pageNumber = 1 #Current page number.
	MAX_DUPLICATION = 10 #Max duplication count. If current duplication count exceeds this, terminate crawling.
	dupeCount = 0 #Current duplication count.

	while(1):
		#Target page list
		target_pages = []
		#list page url.
		url = 'https://www.socialchange.kr/guest?page=%d&currentPageNo=1&process=B&orderField=regDate&orderType=desc' % pageNumber
		#Try to get list page.
		try:
			req = requests.get(url)
			page = req.text
			soup = bs(page, 'html.parser')
		except Exception as inst:
			print(inst)
			break
		#Get list items from document.
		elements = soup.select('a.hotView');

		#If there is no list item on the document, terminate crawling.
		if(len(elements) == 0):
			break
		
		#Get list items url, city-title, uid.
		for element in elements:
			url = element['data-href']
			region = element['data-citytitle'].strip(' ')
			uid = element['data-propoistionuid']
			target_pages.append({'URL': url, 'REGION': region, 'UID': uid})


		for targetPage in target_pages:
			#Target page url.
			url = 'https://www.socialchange.kr/%s' % targetPage['URL']
			#Try to get target page document.
			try:
				req = requests.get(url)
				page = req.text
			except Exception as inst:
				print(inst)
				continue
			#Try to check duplication from DB.
			try:
				#SQL query
				sql = "SELECT * FROM crawling_sckr WHERE board_sn = '%s'" % targetPage['UID']
				#Query execution
				cur.execute(sql)
				#Get row list
				rows = cur.fetchall()
				#If length of row list is not 0 (i.e. there's a duplication), skips the insert phase and increase duplication count by 1.
				if(len(rows) != 0):
					dupeCount += 1
					continue
				#Parse document, get parse result.
				result = parsePage(page, url, targetPage['REGION'])
				#Insert query.
				sql = "INSERT INTO crawling_sckr VALUES (%s, '%s', '%s', '%s', '%s', '%s', '')" % (targetPage['UID'], result['location'], result['title'], result['date'], result['contents'], result['url'])
				#Insert data to DB.
				cur.execute(sql)
			except Exception as inst:
				print(inst)
				print('FAIL TO PARSE PAGE #%s' % targetPage['UID'])
		
		#If current page number is equal to end number, terminate crawling.
		if pageNumber == endNumber:
			break
		
		#If current duplication count exceeds this, terminate crawling.
		if dupeCount >= MAX_DUPLICATION:
			print('Exceeded max duplication count. Aborting crawling.')
			break
		
		#Clear targetPage list.
		targetPage.clear()

		#Increase page number by 1.
		pageNumber += 1

	#Close DB connection.
	conn.close()

#Testing..
if __name__ == '__main__':
	print('Start Module Testing for SCCrawler.')
	crawl(1)
	print('Done.')
		
		
