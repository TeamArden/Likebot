#!/usr/bin/env python
from VK.groups import *
from VK.likes import *
from VK.frandse import *
from VK.repost import *
#from YouTube.likes import *
import undetected_chromedriver as uc
from Authorization.authorization import autho
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# options = uc.ChromeOptions()
# options.add_argument("'--remote-debugging-port=4444'")
# options.add_argument("--user-data-dir=/home/kali/.config/chromium")
# options.add_argument('--profile-directory=Profile 4')
# options.add_argument("--start-maximized")
# #options.headless = True
# options.add_argument('--headless')
# driver = uc.Chrome(options=options)
#https://likes.fm/#
#https://biglike.org/instr
#driver.get("https://vk.com/")

user = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36')

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("'--remote-debugging-port=80'")
chrome_options.add_argument("window-size=1200x600")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--user-data-dir=/home/kali/.config/chromium")
chrome_options.add_argument('--profile-directory=Profile 4')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

chrome_options.add_argument('--no-sandbox')

#chrome_options.add_argument('User-Agent=str(ua.chrome)')
chrome_options.add_argument(f'user-agent={user}')
servico = Service(ChromeDriverManager().install())
# check_tor =   # input("Введите ссылку :")
driver = webdriver.Chrome(service=servico, options=chrome_options)
driver.get("https://freelikes.online/")
#sleep(555)
#driver.find_element("xpath", '//*[@id="uLogin"]/span[1]/i').click()
a = driver.find_element("xpath", '//*[@id="uLogin"]/span[1]/i').click()

try:
    sleep(6)
    try:
        if a == driver.switch_to.window(driver.window_handles[1]):
            autho(driver)
            driver.find_element("xpath", '/html/body/div[1]/div[1]/section/div/div/div[1]/div/center/a[1]').click()
    except IndexError:
        print("Index out of range")
        for i in range(2):
            parse(driver)
        # for i in range(10):
        #     parse1(driver)
        for i in range(1):
            parse2(driver)

except NoSuchElementException:
        print("Element not found")


        driver.find_element("xpath", '/html/body/div[1]/div[1]/section/div/div/div[1]/div/center/a[1]').click()

        for i in range(2):
            parse(driver)
        # for i in range(10):
        #     parse1(driver)
        for i in range(1):
            parse2(driver)
    # sleep(888)
