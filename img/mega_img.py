import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib import request
import ssl

from selenium.webdriver.support.wait import WebDriverWait

#인증서 검증 비활성화
ssl._creat_default_https_context = ssl._create_unverified_context
IMG = "C:/Users/KDT103/Desktop/coding/0. 프로젝트/개인프로젝트/mega_kiosk/img/food"
WEB_DRIVER_PATH = 'chromedriver.exe'

s = Service(WEB_DRIVER_PATH)
driver = webdriver.Chrome(service=s)

# driver.get('https://www.mega-mgccoffee.com/menu/?menu_category1=1&menu_category2=1')
driver.get('https://www.mega-mgccoffee.com/menu/?menu_category1=2&menu_category2=2')


# imgs = driver.find_elements(By.CLASS_NAME, 'board_page_next')
first_imgs = WebDriverWait(driver, timeout=100).until(
   lambda d: d.find_elements(By.CSS_SELECTOR, '#menu_list > li> a > div > div.cont_gallery_list_img > img'))
first_name = WebDriverWait(driver, timeout=100).until(
    lambda d: d.find_elements(By.CSS_SELECTOR, '#menu_list > li > a > div > div.cont_text_box > div > div.cont_text_inner.text_wrap.cont_text_title > div > b'))
# for i in first_imgs:
#     print(i.get_attribute('src'))
# print(len(first_name))
# first_temp = WebDriverWait(driver, timeout=9999).until(
#     lambda d: d.find_elements(By.CSS_SELECTOR, '#menu_list > li > a > div > div.cont_gallery_list_img > div')
# )
# first_temp.inser
# print(len(first_temp))
# print()


for cnt, i in enumerate(first_imgs):
    url_ = i.get_attribute('src')
    request.urlretrieve(url_, IMG + f'/{first_name[cnt].text}.jpg')
#
print(len(first_imgs))
print(len(first_name))
print('------------------')

def get_img():

    next_btn = driver.find_element(By.CLASS_NAME, 'board_page_next')
    next_btn.click()
    SCROLL_PAUSE_TIME = 1
    # 스크롤 높이 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 스크롤 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 스크롤 내리는 시간
        time.sleep(SCROLL_PAUSE_TIME)
        # 새로운 스크롤 높이 가져오기
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

    time.sleep(2)
    imgs = WebDriverWait(driver, timeout=9999).until(
       lambda d: d.find_elements(By.CSS_SELECTOR, '#menu_list > li> a > div > div.cont_gallery_list_img > img'))
    name = WebDriverWait(driver, timeout=100).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, '#menu_list > li > a > div > div.cont_text_box > div > div.cont_text_inner.text_wrap.cont_text_title > div > b')
    )
    temp = WebDriverWait(driver, timeout=9999).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, '#menu_list > li > a > div > div.cont_gallery_list_img > div')
    )
    # print(len(imgs))
    #
    for cnt, i in enumerate(imgs):
        url_ = i.get_attribute('src')
        print(name[cnt].text)
        request.urlretrieve(url_, IMG +f'/{temp[cnt].text}_{name[cnt].text}.jpg')

    print(len(imgs))
    print(len(name))


for i in range(5):
    get_img()

    #
    print(len(first_imgs))
    print(len(first_name))
    print('------------------')



driver.close()