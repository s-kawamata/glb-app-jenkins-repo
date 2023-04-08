import os
import sys
import datetime
from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import user_info
import user_list
import user_profile
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

#今日の日付を取得し、要素検索用に加工

today = date.today()
startTimeElement = "ttvTimeSt" + str(today)


# Firefox
options = Options()
firefox_profile = user_profile.shusei_kawamata
fp = webdriver.FirefoxProfile(firefox_profile)
options.headless = True
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
driver = webdriver.Firefox(options=options,firefox_profile=fp,capabilities=firefox_capabilities)
driver.set_window_size(1920, 1080)

# Googleアクセス
driver.get('https://www.google.com/?hl=ja')

#ログイン開始
try:
  #ここからSSO処理
  time.sleep(5)
  elm = driver.find_element_by_xpath("//*[@class='gb_1e']")
  actions = ActionChains(driver)
  actions.move_to_element(elm)
  actions.perform()
  driver.find_element_by_xpath("//*[@aria-label='Google アプリ']").click()
  actions.reset_actions()
  time.sleep(5)
  iframe = driver.find_element_by_xpath("//iframe[@role='presentation']")
  driver.switch_to.frame(iframe)
  time.sleep(5)
  driver.find_element_by_xpath("//*[contains(text(), 'TeamSpirit')]").click()
  time.sleep(5)
  handle_array = driver.window_handles
  driver.switch_to.window(handle_array[1])
  
  #お知らせウィンドウが開いていた場合は閉じる
  notification_window = driver.find_elements_by_xpath("//div[@data-dojo-attach-point='titleBar']/*[contains(text(), 'お知らせ')]")
  
  if notification_window:
    y_loca = driver.find_element_by_xpath("//tr[@id='dialogInfoBottom']//button[@class='std-button2 close_button']")
    driver.execute_script("window.scrollTo(0, " + str(y_loca.location['y']) + ");")
    y_loca.click()
  else:
    pass
    
  time.sleep(5)
  elm = driver.find_elements_by_xpath("//a[@title='勤務表タブ']")
  if elm :
    pass 
  else :
    raise ValueError("ログインに失敗しました")

except NoSuchElementException as e:
  print(e)

time.sleep(7)

#勤務表のタブをクリック
driver.find_element_by_xpath("//a[@title='勤務表タブ']").click()
time.sleep(5)

#メンバリスト分繰り返し処理を開始
for i in user_list.nameList:

    #社員名横のプルダウンをクリック
    driver.find_element_by_xpath('//*[@id="empListButton"]').click()

    time.sleep(3)



    #別ウインドウをアクティブに
    newhandles = driver.window_handles
    driver.switch_to.window(newhandles [2])

    time.sleep(3)


    #メンバ名を検索、クリック
    driver.find_element_by_link_text(i).click()


    #元のウインドウに戻る
    driver.switch_to.window(newhandles [1])

    time.sleep(3)

    #お知らせウィンドウが開いていた場合は閉じる
    notification_window = driver.find_elements_by_xpath("//div[@data-dojo-attach-point='titleBar']/*[contains(text(), 'お知らせ')]")

    if notification_window:
        y_loca = driver.find_element_by_xpath("//tr[@id='dialogInfoBottom']//button[@class='std-button2 close_button']")
        driver.execute_script("window.scrollTo(0, " + str(y_loca.location['y']) + ");")
        y_loca.click()
    else:
        pass

    #勤務開始の要素を確認し、未入力であればフラグを立てる
    try:
        status = driver.find_element_by_id(startTimeElement).get_attribute("textContent")
        #print(startTimeElement)
    except:
        print('本日は休日です。もし休日出勤の場合は先に勤務申請を修正してください。')
        break

    if status == '':
        print(i + 'さんはまだ本日の勤怠開始を打刻していません')
    else :
        print(i + 'さんはすでに本日の勤怠開始を打刻しています')


#完了処理
driver.quit()
