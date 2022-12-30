from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
import random
import time

FIRSTNAMES = open('names.txt','r').read().split('\n')
LASTNAMES = open('lastnames.txt','r').read().split('\n')

def choose_random_name():
	return f'{FIRSTNAMES[random.randint(0, len(FIRSTNAMES)-2)]}', f'{LASTNAMES[random.randint(0, len(LASTNAMES)-2)]}'


def reach_out_lol(name, email, message):
	browser = Firefox()
	browser.get('https://cobratate.com/contact')
	css_name = '.input-flex-container > label:nth-child(1) > input:nth-child(1)'
	css_email = '.input-flex-container > label:nth-child(2) > input:nth-child(1)'
	
	browser.find_element(By.CSS_SELECTOR, css_name).send_keys(name)
	time.sleep(random.randint(0,3))
	browser.find_element(By.CSS_SELECTOR, css_email).send_keys(email)
	time.sleep(random.randint(0,3))
	browser.find_element(By.CSS_SELECTOR, 'textarea.form-input').send_keys(message)
	time.sleep(random.randint(0,3))
	browser.find_element(By.CSS_SELECTOR, '.button-large').click()
	time.sleep(random.randint(2,5))
	# browser.close()


def annoy_cobra():
	obnoxious = True; messages = 0
	# msg = "Hey! Just wanted to say I think you're a major fucking asshole. Take another pull of that cigar, the fight is just beginning. :)"
	msg = "Hey Fuckface!\nYou're a con artist preying on the minds of young men. Fuck you and everything you stand for. You are a leech and a toxin."
	msg += '\nSincerely,\nAnonymous'
	while obnoxious:
		try:
			first_name, last_name = choose_random_name()
			email = f'{first_name.lower()}.{last_name.lower()}{random.randint(50,99)}@gmail.com'
			print(f'[-] Sending a message to cobra tate as {email}')
			reach_out_lol(f'{first_name.upper()} {last_name.upper()}', email, msg)
			messages += 1
		except KeyboardInterrupt:
			obnoxious = False
			print(f'[!] OK... Lets knock it off')
			pass
	print(f'[+] Finished Sending {messages} emails to CobraTate')

annoy_cobra()