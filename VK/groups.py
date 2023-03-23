from Tokens.vk.tokens import token
from time import sleep
import vk_captchasolver as vc
import re
from selenium.webdriver.common.by import By
import requests

def parse2(driver):
    #driver.switch_to.window(driver.window_handles[-1])
    driver.find_element("xpath",'//*[@id="top-menu"]/ul/li[2]/a').click()### Вкладка друзья
    sleep(4)

    users_url = []
    #users = driver.find_elements("xpath",'//*[@id="div1"]')
    # print(users)
    i = 1

        #element = driver.find_element("xpath", '//*[@id="div1"]')
    for element in driver.find_elements(By.XPATH, '//*[@id="div1"]'):

        i = i++1
        e = element.find_element(By.CLASS_NAME, "task-avatar")
        users_url.append(e.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
        if i > 10:

            break
    print(users_url)

    sleep(1)

    pattern = r'(?<=vk\.com\/)((?:club)(\d+)|.*)'
    for x in users_url:
        id = ([x for x in re.search(pattern, x).groups() if x != None][-1])

        if id.isalpha():

            screen = f'https://api.vk.com/method/utils.resolveScreenName?screen_name={id}&v=5.131&access_token={token}'
            req = requests.post(screen).json()#{"response":{"object_id":136134,
            id = req["response"]["object_id"]

        url = f'https://api.vk.com/method/groups.join?group_id={id}&text=test&v=5.131&access_token={token}'
        req = requests.post(url).json()
        print(req)
        try:
            if req != req['response']:
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
                url = f'https://api.vk.com/method/groups.join?captcha_sid={captcha_sid}&captcha_key={captcha_key}&group_id={id}&text=test&v=5.131&access_token={token}'
                req = requests.post(url).json()

            print(req)
    for item in driver.find_elements(By.XPATH, '// *[ @ id = "div2"] / div / div[2] / a[1]')[:10]:
        sleep(7)
        driver.execute_script("arguments[0].click();", item)
        from selenium.common.exceptions import NoSuchElementException
        try:
            driver.find_element(By.CLASS_NAME, 'alert.alert-danger')
            print('element for U!')
            #driver.find_element("xpath", '//*[@id="div2"]/div/div[2]/a[2]').click()
        except NoSuchElementException:
            print('Zero element for U!')
    sleep(4)
    driver.refresh()
    sleep(2)