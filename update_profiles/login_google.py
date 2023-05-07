import os
import sys
import datetime
import json
from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import urllib.request
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

# Firefox
options = Options()
firefox_profile = "/Users/s_kawamata/Library/Application Support/Firefox/Profiles/yckwb8hz.default-release"
fp = webdriver.FirefoxProfile(firefox_profile)
#options.headless = True
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
driver = webdriver.Firefox(options=options,firefox_profile=fp,capabilities=firefox_capabilities)
driver.set_window_size(1920, 1080)

# Googleアクセス
driver.get('https://www.google.com/?hl=ja')
time.sleep(5)


elm = driver.find_elements_by_xpath("//div[contains(text(), 's_kawamata@ap-com.co.jp')]")

def is_logged_in(driver):
    elm = driver.find_elements_by_xpath("//div[contains(text(), 's_kawamata@ap-com.co.jp')]")
    if elm:
        print("ログイン済みです。")
        return True
    else:
        print("ログインされていません。")
        return False


if is_logged_in(driver):
    sys.exit()
else:
    #ログイン開始
    #ここからSSO処理
    driver.find_element_by_xpath("//*[contains(text(), 'ログイン')]").click()
    time.sleep(5) 
    driver.find_element_by_xpath("//*[@data-email='s_kawamata@ap-com.co.jp']").click()
    # driver.find_element_by_xpath("//*[contains(text(), '次へ')]").click()
    time.sleep(5)
    goolge_pw = "19921107Wanko"
    driver.find_element_by_id("password").click()
    driver.find_element_by_xpath("//input[@name='password']").send_keys(goolge_pw, Keys.ENTER)
    time.sleep(5)

    # Cookie の有効期限を表示する
    for cookie in driver.get_cookies():
        if cookie['name'] == 'SID':
            # cookieからエポックタイムを取得
            expiry = cookie['expiry']

            # エポックタイムをdatetimeオブジェクトに変換
            expiry_date = datetime.fromtimestamp(expiry)

            # 日付を文字列にフォーマットして表示
            print('更新前の有効期限:', expiry_date.strftime('%Y/%m/%d %H:%M:%S'))