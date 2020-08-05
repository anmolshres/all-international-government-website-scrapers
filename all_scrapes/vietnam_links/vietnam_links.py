from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import math
from time import sleep

CHROMEDRIVER_PATH = './chromedriver.exe'
filename = 'links/vietnam_links.txt'
options = Options()
options.headless = False
master_links = []

driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

driver.get('https://ncov.moh.gov.vn/web/guest/khuyen-cao')
checkButton_state = driver.find_elements_by_css_selector(
    '.pager.lfr-pagination-buttons > li')[1]
next_button_disabled = checkButton_state.get_attribute('class') == 'disabled'
while next_button_disabled == False:
    elements = driver.find_elements_by_css_selector('a')
    elements = elements[11:16]
    for elem in elements:
        master_links.append(elem.get_attribute('href'))
    checkButton_state = driver.find_elements_by_css_selector(
        '.pager.lfr-pagination-buttons > li')[1]
    next_button_disabled = checkButton_state.get_attribute(
        'class') == 'disabled'
    if next_button_disabled == False:
        button = driver.find_elements_by_css_selector(
            '.pager.lfr-pagination-buttons > li > a')[1]
        button.click()
        sleep(4)
with open(filename, 'w', encoding='utf-8') as outfile:
    outfile.write(','.join(master_links))
driver.quit()
