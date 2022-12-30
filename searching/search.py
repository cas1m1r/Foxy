from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
import selenium
import random
import urllib
import time
import json
import sys
import re
import os


class WhatInTheDuck:
	homeduck = f'https://duckduckgo.com'
	default_height = 600
	default_width  = 800

	def __init__(self, query:str, opts:dict={}):
		# setup browser
		self.browser = self.setup(opts)
		# load DuckDuckGo
		self.results = self.search_ddg(query)
		# start with first page 
		print(f'[+] Found {len(self.results["results"])} results')

	def view_results(self):
		data = {self.browser.get_current_url: {}}
		for page in self.results:
			data[self.browser.get_current_url]['cookies'] = self.browser.get_cookies() 
			print(f'[+] Visiting {link}')
			self.browser.get(link)
			# scrape page?
			random_sleep(5)
			self.browser.back()
			random_sleep(1)


	def setup(self, opts):
		if 'height' in opts.keys():
			self.default_height = opts['height']
		if 'width' in opts.keys():
			self.default_width = opts['width']
		# define browser options
		useragent = "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004)"\
					" AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"
		opts = FirefoxOptions()
		opts.set_preference("general.useragent.override", useragent)
		browser = Firefox(options=opts)
		# Change width and height based on options given
		browser.set_window_size(self.default_width, self.default_height)
		return browser


	def search_ddg(self, term):
		self.browser.get(self.homeduck)
		random_sleep(3)
		searchbox = self.browser.find_element(By.ID,'searchbox_input')
		searchbox.send_keys(term)
		random_sleep(2)
		searchbox.submit()
		search = {'search_term': term, 'results': []}
		finding = True
		page = 1
		while finding:
			try:
				self.browser.execute_script(f"window.scrollTo(0,{self.default_height + 300*(page-1)})")
				random_sleep(5)
				for r in parse_element('"LnpumSThxEWMIsDdAT17 CXMyPcQ6nDv47DKFeywM">',self.browser.page_source):
					search['results'].append(r.split(' ')[1].split('=')[1].replace('"',''))
				self.browser.find_element(By.CSS_SELECTOR,f'#rld-{page}').click()
				page += 1
			except KeyboardInterrupt:
				print(f'[+] Okay Moving on...')
				finding = False
				pass
			except:
				finding = False
				pass
			print(f'[+] Moving onto page {page} of results for {term}')
		search['results'] = list(set(search['results']))
		return search


def parse_element(item, data):
	occurences = []
	offset = len(item)
	for i in re.finditer(item, data):
		occurences.append(data[i.start()+offset:].split('</')[0])
	return occurences

def random_sleep(max_time:int):
	time.sleep(random.randint(1, max_time) + random.randint(0,max_time))

def random_scroll(browser):
	dims = browser.get_window_size()
	H = int(random.randint(20,95)/100 * dims['height'])
	browser.execute_script(f"window.scrollTo(0,{H})")
	return browser

if __name__ == '__main__':
	if len(sys.argv) > 1:
		search = WhatInTheDuck(' '.join(sys.argv[1:]), {'width':1000,'height':1100})
		search.browser.close()
		results = search.results
		if not os.path.isdir('SEARCHES'):
			os.mkdir('SEARCHES')
		f = f"SEARCHES/{' '.join(sys.argv[1:]).replace(' ','_')}.json"
		open(f,'w').write(json.dumps(results, indent=2))	
