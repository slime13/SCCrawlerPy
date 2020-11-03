import requests
import time
from bs4 import BeautifulSoup as bs
from SCPageParser import parsePage
import psycopg2

"""

"""

def crawl(endNumber = -1):

	try:
		conn = psycopg2.connect(database="dsidb", user="postgres", password="developer#!", host="121.129.214.6", port="8432")
		conn.autocommit = True
		cur = conn.cursor()
	except Exception as inst:
		print(inst)
		return 1

	pageNumber = 1
	MAX_DUPLICATION = 10
	dupeCount = 0

	while(1):

		target_pages = []
		url = 'https://www.socialchange.kr/guest?page=%d&currentPageNo=1&process=B&orderField=regDate&orderType=desc' % pageNumber
		try:
			req = requests.get(url)
			page = req.text
			soup = bs(page, 'html.parser')
		except Exception as inst:
			print(inst)
			break
		elements = soup.select('a.hotView');

		if(len(elements) == 0):
			break
		for element in elements:
			url = element['data-href']
			region = element['data-citytitle'].strip(' ')
			uid = element['data-propoistionuid']
			target_pages.append({'URL': url, 'REGION': region, 'UID': uid})

		for targetPage in target_pages:
			url = 'https://www.socialchange.kr/%s' % targetPage['URL']
			try:
				req = requests.get(url)
				page = req.text
			except Exception as inst:
				print(inst)
				continue
			try:
				sql = "SELECT * FROM crawling_sckr WHERE board_sn = '%s'" % targetPage['UID']
				cur.execute(sql)
				rows = cur.fetchall()
				if(len(rows) != 0):
					dupeCount += 1
					continue
				result = parsePage(page, url, targetPage['REGION'])
				sql = "INSERT INTO crawling_sckr VALUES (%s, '%s', '%s', '%s', '%s', '%s', '')" % (targetPage['UID'], result['location'], result['title'], result['date'], result['contents'], result['url'])
				cur.execute(sql)
			except Exception as inst:
				print(inst)
				print('FAIL TO PARSE PAGE #%s' % targetPage['UID'])
		if pageNumber == endNumber:
			break
		if dupeCount >= MAX_DUPLICATION:
			print('Exceeded max duplication count. Aborting crawling.')
			break
		targetPage.clear()
		pageNumber += 1

	conn.close()

if __name__ == '__main__':
	print('Start Module Testing for SCCrawler.')
	crawl(1)
	print('Done.')
		
		
