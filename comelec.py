from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


REGION = 2
PROVINCE = 3
MUNICIPALITY = 4

def click_filter_btn(area):
    xpath = '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[4]/div'
    xpath += '[' + str(area) + ']'
    xpath += '/nav-filter/div/span/div/div/span'
    region_filter_button = driver.find_element(By.XPATH, xpath)
    region_filter_button.click()

def choose_area(area, option): 
    xpath = '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[4]/div'
    xpath += '[' + str(area) + ']'
    xpath += '/nav-filter/div/span/div/div/div[2]/ul/li'
    xpath += '[' + str(option) + ']'
    elem = driver.find_element(By.XPATH, xpath)
    elem.click()


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
cService = webdriver.ChromeService(executable_path='/Users/clarissa/Developer/Projects/Ulirat-Comelec-Data/chromedriver')
driver = webdriver.Chrome(service = cService, options=chrome_options)
driver.get('https://2022electionresults.comelec.gov.ph/#/coc/0')
driver.implicitly_wait(10)

click_filter_btn(REGION)
choose_area(REGION, 1)
click_filter_btn(PROVINCE)
choose_area(PROVINCE, 1)
click_filter_btn(MUNICIPALITY)
choose_area(MUNICIPALITY, 1)

time.sleep(1)


soup = BeautifulSoup(driver.page_source, 'html.parser')
candidates = soup.select('.text-left .candidate-result')
print([candidate.get_text() for candidate in candidates])


