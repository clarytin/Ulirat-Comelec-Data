from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time


REGION = 2
PROVINCE = 3
MUNICIPALITY = 4

PRES = '+5587'

def setup(): 
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    cService = webdriver.ChromeService(executable_path='/Users/clarissa/Developer/Projects/Ulirat-Comelec-Data/chromedriver')
   
    driver = webdriver.Chrome(service = cService, options=chrome_options)
    driver.get('https://2022electionresults.comelec.gov.ph/#/coc/0')
    driver.implicitly_wait(10)

    return driver

def choose_area():
    click_filter_btn(REGION)
    click_dropdown(REGION, 1)
    click_filter_btn(PROVINCE)
    click_dropdown(PROVINCE, 1)
    click_filter_btn(MUNICIPALITY)
    click_dropdown(MUNICIPALITY, 1)

def click_filter_btn(area):
    xpath = '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[4]/div'
    xpath += '[' + str(area) + ']'
    xpath += '/nav-filter/div/span/div/div/span'
    region_filter_button = driver.find_element(By.XPATH, xpath)
    region_filter_button.click()

def click_dropdown(area, option): 
    xpath = '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[4]/div'
    xpath += '[' + str(area) + ']'
    xpath += '/nav-filter/div/span/div/div/div[2]/ul/li'
    xpath += '[' + str(option) + ']'
    elem = driver.find_element(By.XPATH, xpath)
    elem.click()

def clean(data):
    return data.getText()[1:-1]

def get_vote_data(position):
    div_id = "'resultDiv.'" + position
    results_div = soup.find(id=div_id).findChild("div")
    results = results_div.findChildren("div", {'class': 'candidate-result'})

    df = pd.DataFrame(columns=['Candidate','Votes','Percentage'])

    for i in range(0, len(results), 3):
        row = pd.DataFrame({'Candidate':[results[i]],
                            'Votes': [clean(results[i+1])],
                            'Percentage': [clean(results[i+2])]})
        df = pd.concat([df, row], ignore_index=True)

    return df

driver = setup()
choose_area()

time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')

pres_df = get_vote_data(PRES)
print(pres_df)



