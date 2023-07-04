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

MAYBANK_KE_LINK = "https://www.maybank-ke.co.th/"
LOCAL_PATH = "SET DATA"
DOWNLOAD_PATH = "D:\\temp_data\\SET Smart Data\\SET DATA"

opts = Options()

opts.add_argument("--start-minimized")
opts.add_argument("user-agent=EM")
#opts.add_argument("headless")
#opts.add_argument("window-size=1200x900")
opts.add_argument(f"download.default_directory={DOWNLOAD_PATH}")

prefs = {"download.default_directory" : DOWNLOAD_PATH}

opts.add_experimental_option("prefs", prefs)

#driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)
#driver = webdriver.Chrome(executable_path="C:\\__D__\\DRIVE_APP\\Python\\EDS\\SystemsHistoryAPI\\drivers\\chromedriver.exe")
driver = webdriver.Chrome(executable_path="drivers\\chromedriver.exe", chrome_options = opts)
driver.get(MAYBANK_KE_LINK)

content = driver.execute_script("return document.documentElement.outerHTML;")

rahas_filename = "maybank.enc"

if content.find("เข้าสู่ระบบ") > 0:
    submit_xpath = "/html/body/div[5]/div[2]/div[2]/div[3]/div[1]/form/input[4]"
    pass_card.LoginWeb_ByID(driver, "user", "txtPassword", submit_xpath, rahas_filename)

time.sleep(0.5)
content = driver.execute_script("return document.documentElement.outerHTML;")

# cont_xpath = "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td/p[7]/input"
# driver.find_element(By.XPATH, cont_xpath).submit()

timeout = 100
start_time = datetime.now()
while (content.find("ความเสี่ยงและข้อจำกัดความรับผิด") == -1) and  ((datetime.now()- start_time).total_seconds() < timeout):
    time.sleep(0.5)
    content = driver.execute_script("return document.documentElement.outerHTML;")

# Click confirm (ตกลง)
confirm_xpath = "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td[2]/form/table/tbody/tr/td/p[7]/input"
driver.find_element(By.XPATH, confirm_xpath).submit()

# Go to Maybank Home Page
timeout = 10
start_time = datetime.now()
while (content.find("Maybank Securities (Thailand) Plc") == -1) and  ((datetime.now()- start_time).total_seconds() < timeout):
    time.sleep(0.5)
    content = driver.execute_script("return document.documentElement.outerHTML;")

# Choose main iframe
driver.switch_to.frame(driver.find_element(By.NAME, "main"))

# Click SET SMART botton
set_smart_xpath = "/html/body/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td/table[2]/tbody/tr[2]/td"
driver.find_element(By.XPATH, set_smart_xpath).click()

time.sleep(1)

# Now SET SMART web should be opened in new window
# Ok we will switch to new window
driver.switch_to.window(driver.window_handles[1])

time.sleep(5)

action = ActionChains(driver)

#timeout = 60
#start_time = datetime.now()
#while (content.find("burger-btn") == -1) and  ((datetime.now()- start_time).total_seconds() < timeout):
#    time.sleep(3)
#    content = driver.execute_script("return document.documentElement.outerHTML;")

timeout = 60
start_time = datetime.now()
x= ""
while (x != "complete") and  ((datetime.now()- start_time).total_seconds() < timeout):
    time.sleep(3)
    x = driver.execute_script("return document.readyState")

time.sleep(20)
# Mouse hover the Company Menu

#driver.find_element(By.CLASS_NAME, "burger-btn").click()
#m = driver.find_element(By.LINK_TEXT, "Company")
#action.move_to_element(m).perform()

# Mouse hover the Company Menu
m = driver.find_element(By.LINK_TEXT, "Company")
action.move_to_element(m).perform()

# Click on sub menu Financial Statements
#n = driver.find_element(By.XPATH, "/html/body/app-root/app-default-layout/div/app-header/header/div/nav[1]/div[1]/div[2]/ul/li[2]/app-sub-menu/span/div/span/div/div[2]/div[1]/ul/li[4]/span/a")
n = driver.find_element(By.ID, "Financial Statements")
action.move_to_element(n).click().perform()
time.sleep(5)

# Loop Here 
symbol_list = ["AOT", "MEGA", "HMPRO", "UTP", "BCH", "BCP", "BBL", "PR9", "CPALL", "WHA"]
statement_botton = ["income_statement-button", "balance_sheet-button", "cash_flow-button"]

with open("done.txt", "r")as f:
    done = f.read()

done_list = [x for x in done.split("\n") if x != ""]
df_stock = pd.read_csv("set_stock_symbol.csv")
symbol_list = {row["ชื่อย่อหลักทรัพย์"] : row["ตลาด"] for idx, row in df_stock.iterrows() if row["ชื่อย่อหลักทรัพย์"] not in done_list}

first_time = True

for symbol, market in symbol_list.items():
    this_symbol_is_ok = True

    for statement in statement_botton:
        try:
            time.sleep(2)
            input_box = driver.find_element(By.ID, "input-search")
            input_box.clear()
            time.sleep(0.2)
            input_box.send_keys(symbol)
            time.sleep(0.2)
            auto_complete = driver.find_elements(By.XPATH, "/html/body/app-root/app-default-layout/div/div/app-financial-statement/div[1]/div/div[1]/div[1]/div/div[2]/div/app-input-search-autocomplete/typeahead-container/button[1]/span/strong")
            if len(auto_complete) > 0:
                auto_complete[0].click()
                time.sleep(2)

            driver.find_element(By.ID, statement).click()
            time.sleep(0.2)
            driver.find_element(By.ID, "qoq-button").click()

            driver.find_element(By.ID, "drop-down-quarter1").click()
            time.sleep(0.5)
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "item-Q1"))).click()
            driver.find_element(By.XPATH, "/html/body/app-root/app-default-layout/div/div/app-financial-statement/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div/div[1]/app-drop-down-nowrap/div/ul/li[1]/a").click()

            driver.find_element(By.ID, "drop-down-quarter2").click()
            time.sleep(0.5)
            driver.find_element(By.XPATH, "/html/body/app-root/app-default-layout/div/div/app-financial-statement/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div/div[1]/app-drop-down-nowrap/div/ul/li[4]/a").click()
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "item-Yearly"))).click()

            driver.find_element(By.ID, "drop-down-years1").click()
            time.sleep(0.5)
            driver.find_element(By.XPATH, "/html/body/app-root/app-default-layout/div/div/app-financial-statement/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div/div[2]/app-drop-down-nowrap/div/ul/li[24]/a").click()

            driver.find_element(By.ID, "drop-down-years2").click()
            time.sleep(0.5)
            driver.find_element(By.XPATH, "/html/body/app-root/app-default-layout/div/div/app-financial-statement/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div/div[2]/app-drop-down-nowrap/div/ul/li[1]/a").click()


            # Change langauge to TH
            driver.find_element(By.ID, "lang-flag-th").click()
            time.sleep(0.5)
            driver.find_element(By.ID, "export-link").click()
            time.sleep(2)
            driver.find_element(By.ID, "lang-flag-en").click()
            time.sleep(0.5)

            list_of_files = glob.glob(f"{DOWNLOAD_PATH}\\Financ*.xlsx") 
            latest_file = max(list_of_files, key=os.path.getctime)

            if not os.path.exists(f"{LOCAL_PATH}\\{market}\\{symbol}_{statement.split('-')[0]}.xlsx"):
                os.rename(latest_file, f"{LOCAL_PATH}\\{market}\\{symbol}_{statement.split('-')[0]}.xlsx")
            elif os.path.getsize(f"{LOCAL_PATH}\\{market}\\{symbol}_{statement.split('-')[0]}.xlsx") < 20*1024:
                os.remove(f"{LOCAL_PATH}\\{market}\\{symbol}_{statement.split('-')[0]}.xlsx")
                os.rename(latest_file, f"{LOCAL_PATH}\\{market}\\{symbol}_{statement.split('-')[0]}.xlsx")
            else:
                os.remove(latest_file)

        except Exception as ex:
            print(f"ERROR: {symbol}\t{ex}")
            this_symbol_is_ok = False

            try:
                #driver.get("https://sse.maybank-ke.co.th/financialStatement")
                #time.sleep(1)
                # Mouse hover the Company Menu
                #driver.find_element(By.CLASS_NAME, "burger-btn").click()
                #m = driver.find_element(By.LINK_TEXT, "Company")
                #action.move_to_element(m).perform()

                #time.sleep(1)
                driver.find_element(By.LINK_TEXT, "Company").click()
                time.sleep(1)

                #driver.find_element(By.LINK_TEXT, "Company Information").click()
                #time.sleep(1)

                # Click on sub menu Financial Statements
                #n = driver.find_element(By.XPATH, "/html/body/app-root/app-default-layout/div/app-header/header/div/nav[1]/div[1]/div[2]/ul/li[2]/app-sub-menu/span/div/span/div/div[2]/div[1]/ul/li[4]/span/a")
                #n = driver.find_element(By.ID, "Financial Statements")
                #action.move_to_element(n).click().perform()
                driver.find_element(By.ID, "Financial Statements").click()

                #driver.find_element(By.XPATH, "/html/body/app-root/app-default-layout/div/app-header/header/div/nav[2]/app-mobile-menu/div[2]/ul/li[2]/ul/li[1]/ul/li[4]/span/a").click()
                
                time.sleep(4)
            
            except:
                pass

    if this_symbol_is_ok:
        with open("done.txt", "a")as f:
            f.write(symbol + "\n")
a = 5

