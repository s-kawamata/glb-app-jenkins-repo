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



elm = driver.find_elements_by_xpath("//div[contains(text(), 's_kawamata@ap-com.co.jp')]")

if elm:
    print("ログイン済みです。")
    break
else:
    print("ログインされていません。ログインを行いGitにPushします")

#ログイン開始
  #ここからSSO処理
  driver.find_element_by_xpath("//*[contains(text(), 'ログイン')]").click()
  time.sleep(5)  
  driver.find_element_by_xpath("//*[contains(text(), '次へ')]").click()
  time.sleep(5)
  driver.find_element_by_id("password").click()
  driver.find_element_by_xpath("//input[@name='Passwd']").send_keys(goolge_pw, Keys.ENTER)
  time.sleep(5)