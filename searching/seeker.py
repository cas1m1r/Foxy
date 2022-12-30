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


class ImageFinder:
	home = 'http://duckduckgo.com'

	def __init__(self, term):
		self.idir = f'{term.upper().replace(" ","_")}'
		self.base = f'{self.home}/{term}'
		self.browser = self.open_browser()
		self.pages = self.search_term(term)

	def open_browser(self):
		# can set options here
		return Firefox()


	def search_term(self, query):
		self.browser.get(f'{self.base}?ia=images&ia=images')
		random_sleep(3)
		self.browser.find_element(By.CSS_SELECTOR,'.js-zci-link--images').click()
		random_sleep(3)
		# find all image links 
		ilinks = parse_element('<img class="tile--img__img  js-lazyload" ', self.browser.page_source)
		self.browser.close()
		print('[+] Found following links:')
		links = []
		if not os.path.isdir(self.idir):
			os.mkdir(self.idir)
		i = 1
		for url in ilinks:
			self.browser = Firefox()
			page = f'https://{url}'
			# print(page)
			page = url.replace('"','').split('src=//')[-1].split(' ')[0]
			link = f'https://{page}'
			# print(f'\t-> Checking out {link}')
			links.append(link)
			self.browser.get(link)
			# pause
			random_sleep(1)
			# save page 
			with open(f'{self.idir}/result{i}.png','wb') as f:
				f.write(self.browser.get_screenshot_as_png())
				f.close()
				print(f'\t(saved image)')
			i += 1
			# return or close browser 
			self.browser.close()
		return links

def parse_element(item, data):
	occurences = []
	offset = len(item)
	for i in re.finditer(item, data):
		occurences.append(data[i.start()+offset:].split('</')[0].split(' ')[0])
	return occurences

def random_sleep(max_time:int):
	time.sleep(random.randint(1, max_time) + random.randint(0,max_time))

def random_scroll(browser):
	dims = browser.get_window_size()
	H = int(random.randint(20,95)/100 * dims['height'])
	browser.execute_script(f"window.scrollTo(0,{H})")
	return browser

if __name__ == '__main__':
	if len(sys.argv)>1:
		try:
			search = ImageFinder(' '.join(sys.argv[1:]))
		except KeyboardInterrupt:
			print(f'Moving on...')
			exit()