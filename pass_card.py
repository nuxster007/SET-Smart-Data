import rahas
from selenium.webdriver.common.by import By

def LoginWeb_ByID(driver, user_tag_id, passwd_tag_id, submit_xpath, rahas_filename):
    with open(rahas_filename, "r") as f:
        s = f.read()

    info = rahas.decrypt(s)

    driver.find_element(By.ID, user_tag_id).send_keys(info[0])
    driver.find_element(By.ID, passwd_tag_id).send_keys(info[1])
    driver.find_element(By.XPATH, submit_xpath).submit()

    return driver