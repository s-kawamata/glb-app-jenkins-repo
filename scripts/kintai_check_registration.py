import os
import sys
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime, date, timedelta
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import user_info
import user_list
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

#起動させた一ヶ月前の年月を取得

now = datetime.now()
last_month = now - relativedelta(months=1)
last_month_str = last_month.strftime('%Y年%m月')


# Firefox
options = Options()
firefox_profile = "./yckwb8hz.default-release"
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

print("ログイン完了しました")
time.sleep(7)

#勤務表のタブをクリック
driver.find_element_by_xpath('//*[@id="01r5F000000g5DS_Tab"]/a').click()

driver.implicitly_wait(10)

#メンバリスト分繰り返し処理を開始
for i in user_list.nameList:

    #社員名横のプルダウンをクリック
    driver.find_element_by_xpath('//*[@id="empListButton"]').click()

    time.sleep(3)



    #別ウインドウをアクティブに
    newhandles = driver.window_handles
    driver.switch_to.window(newhandles [1])

    time.sleep(3)


    #前月のボタンをクリック
    select = Select(driver.find_element_by_xpath("//*[@class='ts-month-select']"))
    select.select_by_visible_text(f'{last_month_str}')

    time.sleep(5)


    #メンバ名を検索、クリック
    driver.find_element_by_link_text(i).click()


    #元のウインドウに戻る
    driver.switch_to.window(newhandles [0])

    time.sleep(3)

    #お知らせウィンドウが開いていた場合は閉じる
    notification_window = driver.find_elements_by_xpath("//div[@data-dojo-attach-point='titleBar']/*[contains(text(), 'お知らせ')]")

    if notification_window:
        y_loca = driver.find_element_by_xpath("//tr[@id='dialogInfoBottom']//button[@class='std-button2 close_button']")
        driver.execute_script("window.scrollTo(0, " + str(y_loca.location['y']) + ");")
        y_loca.click()
    else:
        pass

    #承認ステータスを確認し、未確定であればフラグを立てる

    status = driver.find_element_by_xpath('//*[@id="monthlyStatus"]').get_attribute("textContent")

    if status == '未確定':
        print(i + 'さんはまだ' + last_month_str + 'の勤怠を提出していません')
    else :
        print(i + 'さんはすでに' + last_month_str + 'の勤怠を提出しています')




#完了処理
print("処理が正常に完了しました。")
driver.quit()
