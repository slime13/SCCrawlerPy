import requests
from bs4 import BeautifulSoup as bs

"""

"""

def removeSpace(str):
	result = str.replace('\r', '')
	result = result.replace('\n', '')
	result = result.replace('\t', '')
	return result

def parsePage(page, url, region):
	result = {'location': None, 'title': None, 'date': None, 'motivation': None, 'contents': None, 'url': None, 'category': 'NULL'}
	soup = bs(page, 'html.parser')
	
	result['url'] = url
	result['location'] = region

	_title_ = soup.select('h3.title_main')[0].text
	_title_ = removeSpace(_title_)
	result['title'] = _title_

	_date_ = soup.select('p.date')[0].text
	_time_ = soup.select('p.time')[0].text

	_date_ = _date_.replace('년 ', '-').replace('월 ', '-').replace('일', '')
	_time_ = _time_.replace('시 ', ':').replace('분', '') + ':00'
	result['date'] = _date_ + 'T' + _time_


	_motivation_ = removeSpace(soup.select('div.summaryContents')[0].text)
	result['motivation'] = bytes(_motivation_, 'utf-8').decode('utf-8', 'ignore')

	_contents_ = soup.select('div.step_wrap div.step_box')[0]
	for div in _contents_.findAll('div', {'class': 'hwp_editor_board_content'}):
		div.decompose()
	result['contents'] = bytes(_contents_.get_text(), 'utf-8').decode('utf-8', 'ignore').replace('\n', '')
	result['contents'] = result['contents'].replace("'", "''").strip()
	return result

if __name__ == '__main__':

	print('Start Module Testing for SCPageParser.')
	region = 'gwangju'
	id = 1938
	url = "https://www.socialchange.kr/%s/guest/proposition/view?id=%s" % (region,str(id))
	try:
		req = requests.get(url)
		page = req.text
	except:
		print('BAD ID.')

	result = parsePage(page, url, '대구')
	
	f = open('dump/test.txt', 'w', encoding='utf-8')

	for key in result:
		f.write('%s: %s\n' % (key, result[key]))