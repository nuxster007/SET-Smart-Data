import pandas as pd
from datetime import datetime, timedelta
import os, sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains

#from chromedriver_py import binary_path
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options


FINANCIAL_SUMMARY_URL = "https://www.set.or.th/th/market/product/stock/quote/@COMPANY_SYMBOL@/major-shareholders"

opts = Options()

opts.add_argument("--start-minimized")
opts.add_argument("user-agent=EM")
#opts.add_argument("headless")
#opts.add_argument("window-size=1200x900")

driver = webdriver.Chrome(executable_path="drivers\\chromedriver.exe", chrome_options = opts)
driver.get(FINANCIAL_SUMMARY_URL.replace("@COMPANY_SYMBOL@","TU"))

content = driver.execute_script("return document.documentElement.outerHTML;")
dfs = pd.read_html(content)

s = 0

