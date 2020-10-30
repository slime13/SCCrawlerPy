import requests
import time
from bs4 import BeautifulSoup as bs
from SCPageParser import parsePage

def crawl():
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
				result = parsePage(page, url, targetPage['REGION'])
				f = open('dump/%s.txt' % (targetPage['REGION'] + '-' + targetPage['UID']), 'w', encoding='utf-8')
				for key in result:
					f.write('%s: %s\n' % (key, result[key]))
				f.close()
			except Exception as inst:
				print(inst)
				print('FAIL TO PARSE PAGE #%s' % targetPage['UID'])

		#페이지 넘김
		targetPage.clear()
		pageNumber += 1
	

if __name__ == '__main__':
	print('Start Module Testing for SCCrawler.', flush=True)
	time.sleep(1)
	crawl()
		
		
