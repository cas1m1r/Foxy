from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
import os, sys, time, string, json, random


FIRSTNAMES = open('names.txt','r').read().split('\n')
LASTNAMES = open('lastnames.txt','r').read().split('\n')

MONTHS = {1:'January',2:'February',3:'March',4:'April',5:'Maya',6:'June',
		  7:'July', 8: 'August', 9:'September', 10:'October', 11:'November', 12:'December'}

def gen_random_bday():
	mo = random.randint(1,12)
	day = random.randint(1,28)
	year = random.randint(1980,2022)
	date = f'{mo}/{day}/{year}'
	return mo,day, year, date


def generate_random_password():
	# make a random password 
	passlength = random.randint(18, 24)
	return ''.join(random.sample(list(string.ascii_letters + string.digits), passlength))


def choose_random_name():
	return f'{FIRSTNAMES[random.randint(0, len(FIRSTNAMES)-2)]} {LASTNAMES[random.randint(0, len(LASTNAMES)-2)]}'


def make_throwaway_yahoo(browser, uname):
	# Accept Cookies
	time.sleep(random.randint(1,5))
	browser.find_element(By.CLASS_NAME,'btn').click()
	time.sleep(4)
	# Click Sign in
	time.sleep(random.randint(1,5))
	browser.find_element(By.CLASS_NAME,'_yb_lxaxg').click()
	
	# click and enter username
	browser.find_element(By.ID,'login-username').send_keys(uname)
	time.sleep(random.randint(1,5))

	browser.find_element(By.ID,'createacc').click()
	time.sleep(3)
	time.sleep(random.randint(1,5))

	throwpass = generate_random_password()

	# choose a random first name:
	first_name = FIRSTNAMES[random.randint(0, len(FIRSTNAMES)-2)]
	last_name = LASTNAMES[random.randint(0, len(LASTNAMES)-2)]
	browser.find_element(By.ID,'usernamereg-firstName').send_keys(first_name)
	time.sleep(random.randint(1,5))
	browser.find_element(By.ID, 'usernamereg-lastName').send_keys(last_name)
	time.sleep(random.randint(2,5))
	browser.find_element(By.ID,'usernamereg-userId').send_keys(uname)
	time.sleep(random.randint(2,5))
	browser.find_element(By.ID, 'usernamereg-password').send_keys(throwpass)

	m,d,year,date = gen_random_bday()
	time.sleep(random.randint(1,3))
	browser.find_element(By.ID, 'usernamereg-birthYear').send_keys(year)
	print(f'Creating email {uname}@yahoo.com')
	print(f'Name: {first_name}, Password: {throwpass}, Birthday: {date}')
	time.sleep(random.randint(1,3))
	browser.find_element(By.ID, 'reg-submit-button').click()
	user = {'name': f'{first_name} {last_name}',
			'pass': throwpass, 
			'email': uname,
			'bday': date}
	return user


def make_throwaway_aol(browser, uname):
	# browse to the registration page
	url = 'https://www.aol.com/'
	browser.get(url)
	time.sleep(random.randint(1,5))
	browser.find_element(By.CLASS_NAME, 'profile-button').click()
	time.sleep(4)
	time.sleep(random.randint(1,5))
	browser.find_element(By.ID, 'createacc').click()
	time.sleep(random.randint(2,5))

	# make a fake name and birthday 
	name = FIRSTNAMES[random.randint(0, len(FIRSTNAMES)-2)]
	first_name = name[0].upper() + name[1:]
	last_name = LASTNAMES[random.randint(0, len(LASTNAMES)-2)]
	throwpass = generate_random_password()
	m,d,year,date = gen_random_bday()

	# enter it into the form
	browser.find_element(By.ID,'usernamereg-firstName').send_keys(first_name)
	time.sleep(random.randint(1,5))
	browser.find_element(By.ID,'usernamereg-lastName').send_keys(last_name)
	time.sleep(random.randint(1,5))
	browser.find_element(By.ID,'usernamereg-yid').send_keys(uname)
	time.sleep(random.randint(1,5))
	browser.find_element(By.ID, 'password-container').send_keys(throwpass)

	browser.find_element(By.ID, 'usernamereg-phone').send_keys('7742469077')
	time.sleep(random.randint(1,5))
	browser.find_element(By.CSS_SELECTOR,'select#usernamereg-month').send_keys(MONTHS[m])
	time.sleep(random.randint(1,5))
	browser.find_element(By.ID,'usernamereg-day').send_keys(d)
	time.sleep(random.randint(1,5))
	browser.find_element(By.ID,'usernamereg-year').send_keys(year)
	print(f'Creating email {uname}@aol.com')
	print(f'Name: {first_name} {last_name}, Password: {throwpass}, Birthday: {date}')
	user = {'name': f'{first_name} {last_name}',
			'pass': throwpass, 
			'email': f'{uname}@outlook.com',
			'bday': date}
	return user	

def make_throwaway_outlook(browser, uname):
	url = 'https://outlook.live.com/owa/?nlp=1&signup=1'
	browser.get(url)
	time.sleep(random.randint(1,5))
	browser.find_element(By.ID,'MemberName').send_keys(uname)
	time.sleep(random.randint(1,3))
	browser.find_element(By.ID, 'iSignupAction').click()
	time.sleep(random.randint(2,4))
	throwpass = generate_random_password()
	browser.find_element(By.ID, 'PasswordInput').send_keys(throwpass)
	time.sleep(random.randint(1,2))
	browser.find_element(By.ID, 'iSignupAction').click()
	time.sleep(random.randint(2,4))

	name = FIRSTNAMES[random.randint(0, len(FIRSTNAMES)-2)]
	first_name = name[0].upper() + name[1:]
	last_name = LASTNAMES[random.randint(0, len(LASTNAMES)-2)]
	browser.find_element(By.ID, 'FirstName').send_keys(first_name)
	time.sleep(random.randint(1,2))
	browser.find_element(By.ID, 'LastName').send_keys(last_name)
	time.sleep(random.randint(1,2))
	browser.find_element(By.ID, 'iSignupAction').click()

	# The Birthday selection is kinda a bitch..
	m,d,year,date = gen_random_bday()
	print(f'Creating email {uname}@outlook.com')
	print(f'Name: {first_name} {last_name}, Password: {throwpass}, Birthday: {date}')
	user = {'name': f'{first_name} {last_name}',
			'pass': throwpass, 
			'email': f'{uname}@outlook.com',
			'bday': date}
	return user	



def make_proton_throwaway(browser, uname):
	url = 'https://account.proton.me/signup?plan=free&billing=12&currency=USD&language=en'
	browser.get(url)
	time.sleep(1)
	time.sleep(random.randint(1,5))
	
	throwpass = generate_random_password()
	fname = FIRSTNAMES[random.randint(0, len(FIRSTNAMES)-2)]
	first_name = fname[0].upper() + fname[1:]
	last_name = LASTNAMES[random.randint(0, len(LASTNAMES)-2)]
	
	form = browser.switch_to.active_element
	time.sleep(random.randint(2,3))
	form.send_keys(uname)

	time.sleep(random.randint(2,3))
	browser.find_element(By.ID, 'password').send_keys(throwpass)
	time.sleep(random.randint(2,3))
	browser.find_element(By.ID, 'repeat-password').send_keys(throwpass)
	time.sleep(random.randint(2,3))
	
	form.submit()

	m,d,year,date = gen_random_bday()

	print(f'Creating email {uname}@protonmial.com')
	print(f'Name: {first_name}, Password: {throwpass}, Birthday: {date}')
	user = {'name': f'{first_name} {last_name}',
			'pass': throwpass, 
			'email': f'{uname}@protonmail.com',
			'bday': date}
	return user



def main():

	random_width = 800 + random.randint(0,500)
	random_height = 600 + random.randint(0,800)
	driver = Firefox()
	driver.set_window_size(random_width, random_height)

	if  '--create-outlook' in sys.argv:
		uname = sys.argv[-1]
		account = make_throwaway_outlook(driver, uname)
	
	if '--create-aol' in sys.argv:
		uname = sys.argv[-1]
		account = make_throwaway_aol(driver, uname)

	if '--create-proton' in sys.argv:
		uname = sys.argv[-1]
		account = make_proton_throwaway(driver, uname)


	if not os.path.isfile('throwaways.json'):
		existing = {}
		existing['acc'] = [account]
	else:
		existing = json.loads(open('throwaways.json','r').read())
		existing['acc'].append(account)

	open('throwaways.json','w').write(json.dumps(existing,indent=2))


if __name__ == '__main__':
	main()
