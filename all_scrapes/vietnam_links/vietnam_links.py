from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

CHROMEDRIVER_PATH = './chromedriver.exe'
filename = 'links/vietnam_links.txt'
options = Options()
options.headless = False
tab_ids = ['menu2', 'menu3', 'menu4', 'menu6', 'menu7']
master_links = []

driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)


def singleTabScrape(this_id):
    tabButton = driver.find_element_by_id(this_id).find_element_by_xpath('..')
    tabButton.click()
    sleep(4)
    checkButton_state = driver.find_elements_by_css_selector(
        '.pager.lfr-pagination-buttons > li')[1]
    next_button_disabled = checkButton_state.get_attribute(
        'class') == 'disabled'
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


def main():

    # goto homepage
    driver.get('https://ncov.moh.gov.vn/')
    initial_cancel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, 'onesignal-slidedown-cancel-button')))
    initial_cancel_button.click()
    for tab_id in tab_ids:
        singleTabScrape(tab_id)

    # write to file
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(','.join(master_links))
    driver.quit()


if __name__ == '__main__':
    main()
