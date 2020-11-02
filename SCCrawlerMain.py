import SCCrawler
import time
import re
import threading

"""

"""

CRAWLING_PERIOD = None
MULTIPLIER = (31536000, 259200, 86400, 3600)
crawlingInterval = 0

def threadStarter():
	threading.Timer(crawlingInterval, threadStarter).start()
	SCCrawler.crawl()
	print('Crawling done. (%s)' % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), flush=True)

if __name__ == '__main__':
	
	configFile = open('config.ini', 'r', encoding='utf-8')
	lines = configFile.readlines()

	#설정파일 읽기
	for line in lines:
		if (line[0] == '#' or line[0] == '\n'):
			continue
		line = line.replace(' ', '')
		line = line.replace('\n', '')
		if (line.find('CRAWL_PERIOD=') != -1):
			line = line.strip('CRAWL_PERIOD=')
			y = int(re.findall(r'\d+y', line)[0].strip('y')) if len(re.findall(r'\d+y', line)) > 0 else 0
			m = int(re.findall(r'\d+m', line)[0].strip('m')) if len(re.findall(r'\d+m', line)) > 0 else 0
			d = int(re.findall(r'\d+d', line)[0].strip('d')) if len(re.findall(r'\d+d', line)) > 0 else 0
			h = int(re.findall(r'\d+h', line)[0].strip('h')) if len(re.findall(r'\d+h', line)) > 0 else 0
			CRAWLING_PERIOD = (y, m, d, h)
	configFile.close()

	crawlingInterval = MULTIPLIER[0] * CRAWLING_PERIOD[0] + MULTIPLIER[1] * CRAWLING_PERIOD[1] + MULTIPLIER[2] * CRAWLING_PERIOD[2] + MULTIPLIER[3] * CRAWLING_PERIOD[3]
	threadStarter()