#coding: utf-8
import sys

reload(sys) 
sys.setdefaultencoding('utf-8')

import SCCrawler
import time
import re
import threading

"""
Main script of SCCrawler.
"""


CRAWLING_PERIOD = None #(Year, Month, Day, Hour) readed from confing.ini
MULTIPLIER = (31536000, 259200, 86400, 3600) #Year, month, day, and hour, converted to seconds.
crawlingInterval = 0 #Crawling period, converted to seconds.

"""
Function "threadStarter()"
Create thread timer for next crawl, start crawling process. 
"""
def threadStarter():
	threading.Timer(crawlingInterval, threadStarter).start()
	SCCrawler.crawl()
	print('Crawling done. (%s)' % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

if __name__ == '__main__':

	#Read config.ini
	configFile = open('config.ini', 'r')
	lines = configFile.readlines()

	#Parse config.ini
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

	#Sum crawling period
	crawlingInterval = MULTIPLIER[0] * CRAWLING_PERIOD[0] + MULTIPLIER[1] * CRAWLING_PERIOD[1] + MULTIPLIER[2] * CRAWLING_PERIOD[2] + MULTIPLIER[3] * CRAWLING_PERIOD[3]
	
	#Start crawling
	threadStarter()