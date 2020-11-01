import requests
import time
from bs4 import BeautifulSoup as bs
from SCPageParser import parsePage
import psycopg2

def crawl(endNumber = -1):
	#DB 연결
	try:
		conn = psycopg2.connect(database="dsidb", user="postgres", password="developer#!", host="121.129.214.6", port="8432")
		conn.autocommit = True
		cur = conn.cursor()
	except Exception as inst:
		print(inst)
		return 1

	pageNumber = 1

	while(1):
		#제안과제 리스트 파싱
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
		#페이지에 더 이상 Entry가 없는 경우 종료
		if(len(elements) == 0):
			break
		for element in elements:
			url = element['data-href']
			region = element['data-citytitle'].strip(' ')
			uid = element['data-propoistionuid']
			target_pages.append({'URL': url, 'REGION': region, 'UID': uid})

		#각 페이지를 수집
		for targetPage in target_pages:
			url = 'https://www.socialchange.kr/%s' % targetPage['URL']
			try:
				req = requests.get(url)
				page = req.text
			except Exception as inst:
				print(inst)
				continue
			try:
				#f = open('dump/%s.txt' % (targetPage['REGION'] + '-' + targetPage['UID']), 'w', encoding='utf-8')
				#for key in result:
				#	f.write('%s: %s\n' % (key, result[key]))
				#f.close()
				#############DB에 입력##############
				result = parsePage(page, url, targetPage['REGION'])
				sql = "INSERT INTO crawling_sckr (%s, %s, %s, %s, %s, %s, '')" % (targetPage['UID'], result['location'], result['title'], result['date'], result['contents'], result['url'])
				cur.execute(sql)
				###################################
			except Exception as inst:
				print(inst)
				print('FAIL TO PARSE PAGE #%s' % targetPage['UID'])
		#endNumber가 정의 되어 있을 경우, endNumber에서 탐색 종료 
		if pageNumber == endNumber:
			break
		#페이지 넘김
		targetPage.clear()
		pageNumber += 1

	conn.close()

if __name__ == '__main__':
	print('Start Module Testing for SCCrawler.', flush=True)
	crawl(1)
	print('Done.', flush=True)
		
		
