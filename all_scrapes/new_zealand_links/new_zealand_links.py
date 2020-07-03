from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import math
from time import sleep

CHROMEDRIVER_PATH = './chromedriver.exe'
filename = 'links/all_new_zealand_links.txt'
options = Options()
options.headless = True


def writeToFile(pageIndex, linksToWrite, pageMax):
    if pageIndex == 0:
        open(filename, 'w').close()
        with open(filename, 'a') as myFile:
            myFile.write(','.join(linksToWrite)+',')
    else:
        with open(filename, 'a') as myFile:
            if pageIndex == pageMax - 1:
                myFile.write(','.join(linksToWrite))
            else:
                myFile.write(','.join(linksToWrite)+',')


driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

driver.get(
    'https://www.health.govt.nz/search/results/coronavirus?f%5B0%5D=im_field_news_type%3A31')

elements = driver.find_elements_by_css_selector(".placeholder")

maxPageString = list(map(lambda element: element.text, elements))[2]
maxPage = math.ceil(int(maxPageString) / 10)
hrefElements = driver.find_elements_by_xpath(
    "//a[starts-with(@href, '/news-media/')]")
links = list(map(lambda elem: elem.get_attribute("href"), hrefElements))
writeToFile(0, links, maxPage)

for index in range(1, maxPage):
    nexPageElement = driver.find_elements_by_xpath(
        "//a[starts-with(@href, '/search/results/coronavirus?page=')]")[-1]
    nexPageElement.click()
    sleep(2)
    hrefElements = driver.find_elements_by_xpath(
        "//a[starts-with(@href, '/news-media/')]")
    links = list(map(lambda elem: elem.get_attribute("href"), hrefElements))
    writeToFile(index, links, maxPage)


driver.quit()
