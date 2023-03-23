#!/usr/bin/env python
import re
from Tokens.vk.tokens import token
import vk_captchasolver as vc
from selenium.webdriver.common.by import By
from time import sleep
import requests
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse(driver):
    users_url = []
    i = 1

    for element in driver.find_elements(By.XPATH, '//*[@id="div1"]'):

        i = i + +1
        e = element.find_element(By.CLASS_NAME, "task-avatar")
        users_url.append(e.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
        if i > 20:
            break
    print(users_url)

    for url1 in users_url:
        print(url1)
        sleep(2)
        # url1 = driver.current_url ### Забрать ссылку из адресной строки
        result = re.search(r"/([a-z]+)(-?\d+)_(\d+)", url1)
        type_name, owner_id, item_id = result.groups()
        if type_name == "wall":
            type_name = "post"
        url = 'https://api.vk.com/method/likes.add?type=%s&owner_id=%s&item_id=%s&v=5.131&access_token=%s' % (
            type_name, owner_id, item_id, token)
        req = requests.post(url).json()
        print(req)
        try:
            if req != req['response']['likes']:
                continue
        except:

            error = req['error']['error_code']
            if error == 14:
                # print("error")
                captcha_sid = req['error']['captcha_sid']
                captcha_img = req['error']['captcha_img']

                with open('newfile.jpg', 'wb') as target:
                    a = requests.post(f'{captcha_img}')
                    target.write(a.content)
                captcha_key = vc.solve(image='newfile.jpg')
                print(f"Капча : {captcha_key}")
                url = 'https://api.vk.com/method/likes.add?captcha_sid=%s&captcha_key=%s&type=%s&owner_id=%s&item_id=%s&v=5.131&access_token=%s' % (
                    captcha_sid, captcha_key, type_name, owner_id, item_id, token)
                req = requests.post(url).json()

            print(req)

    for item in driver.find_elements(By.XPATH, '// *[ @ id = "div2"] / div / div[2] / a[1]')[:20]:
        sleep(4)
        a = driver.execute_script("arguments[0].click();", item)
        try:

            if a == driver.find_element(By.CLASS_NAME, 'alert.alert-danger'):
                print('element for U!')
                e = driver.find_element(By.CLASS_NAME, 'task-tools')
                e.find_element(By.CLASS_NAME, 'delete')
                #element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'delete')))
                e.click()
                sleep(2)
            else:

                for x in driver.find_elements(By.XPATH, '// *[ @ id = "div2"] / div / div[2] / a[2]')[:1]:
                    sleep(4)

                    driver.execute_script("arguments[0].click();", x)

                    try:
                        driver.find_element("xpath", '//*[@id="div2"]/div/div[2]/a[2]').click().send_keys(Keys.RETURN)
                    except:

                        sleep(3)
                        print("ззззз")

        except NoSuchElementException:
            print('Zero element for U!')



        # try:
        #     sleep(2)
        #     if a == driver.find_elements(By.CLASS_NAME, 'alert alert - danger'):
        #         driver.refresh()
        #
        # except:
        #     try:
        #         driver.find_element("xpath", '//*[@id="div2"]/div/div[2]/a[2]').click().send_keys(Keys.RETURN)
        #     except:
        #         driver.find_element("xpath", '//*[@id="div2"]/div/div[2]/a[2]').click()
    sleep(4)
    driver.refresh()
    sleep(2)


#http://freelikes.online/10214889
# element = driver.find_element(By.XPATH, '//*[@id="top-menu-social"]/div/ul/li[5]/a')
# driver.execute_script("arguments[0].click();", element)
#https://oauth.vk.com/authorize?client_id=51514411&redirect_uri=https://oauth.vk.com/blank.html&scope=groups,photo,audio,video,docs,notes,status,offers,questions,wall,email,ads,offline,pages,stats,notifications&response_type=token
