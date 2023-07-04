from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains

#from chromedriver_py import binary_path
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
import pandas as pd
import glob, os
import pass_card


df_stock = pd.read_csv("set_stock_symbol.csv")
symbol_list = {row["ชื่อย่อหลักทรัพย์"] : row["ตลาด"] for idx, row in df_stock.iterrows()}

for symbol, market in symbol_list.items():
    print(symbol, market)


SET_SYMBOL_LINK = "https://www.set.or.th/th/market/get-quote/stock/"

opts = Options()

opts.add_argument("--start-minimized")
opts.add_argument("user-agent=EM")
#opts.add_argument("headless")
#opts.add_argument("window-size=1200x900")
opts.add_argument("download.default_directory=C:\\temp\\SET_Data\\")

prefs = {"download.default_directory" : "C:\\temp\\SET_Data\\"}

opts.add_experimental_option("prefs", prefs)

#driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)
#driver = webdriver.Chrome(executable_path="C:\\__D__\\DRIVE_APP\\Python\\EDS\\SystemsHistoryAPI\\drivers\\chromedriver.exe")
driver = webdriver.Chrome(executable_path="drivers\\chromedriver.exe", chrome_options = opts)
driver.get(SET_SYMBOL_LINK)

content = driver.execute_script("return document.documentElement.outerHTML;")

# timeout = 100
# start_time = datetime.now()
# while (content.find("lightbox-dialog") == -1) and  ((datetime.now()- start_time).total_seconds() < timeout):
#     time.sleep(0.5)
#     content = driver.execute_script("return document.documentElement.outerHTML;")

main_window_handle = driver.current_window_handle
#driver.switch_to.frame(driver.find_element(By.NAME, "main"))

# Scrolling to the bottom of the page
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight*1.0);")
    time.sleep(0.5)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(2)
# Click pop up
#driver.find_element(By.XPATH, "/html/body/div/div/div/div[4]/div/div[1]/button").click()
#time.sleep(1)

action = ActionChains(driver)

# Click drop down
driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div[2]/div[1]/div[1]").click()
time.sleep(0.5)

driver.switch_to.default_content
# Select 100 items per page
driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div[3]/ul/li[6]").click()

# /html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div[2]/div[3]/ul/li[9]

# /html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div[2]/div[3]/ul/li[9]/button

for page in range(9):
    # Scrolling to the bottom of the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*1.0);")
        time.sleep(0.5)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    if page > 0:
        driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div[2]/div[3]/ul/li[9]").click()

    time.sleep(3)
    content = driver.execute_script("return document.documentElement.outerHTML;")
    tables = pd.read_html(content)

    if page == 0:
        df = tables[1]
    else:
        df = pd.concat([df, tables[1]], axis=0)

print(len(df))
df.to_csv("set_stock_symbol.csv", encoding="utf-8-sig")


