from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

REGION = 2
PROVINCE = 3
DISTRICT = 4

def click_region_filter_btn():
    region_filter_button = driver.find_element(By.XPATH, '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[4]/div[2]/nav-filter/div/span/div/div/span')
    region_filter_button.click()

def choose_region(area, option):
    # For some reason, item number 4 is nothing.
    if option < 1 or option > 18 or option == 4:
        raise Exception("Invalid region")
    
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

click_region_filter_btn()
choose_region(REGION, 1)
click_region_filter_btn()
choose_region(PROVINCE, 1)



