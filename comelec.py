from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time


REGION = 2
PROVINCE = 3
MUNICIPALITY = 4

PRESIDENT = '+5587'
VICE_PRES = '+5588'
SENATOR = '+5589'
PARTY_LIST = '+11172'
MEMBER_HOR = 'MEMBER, HOUSE OF REPRESENTATIVES'
GOVERNOR = 'PROVINCIAL GOVERNOR'
VICE_GOV = 'PROVINCIAL VICE-GOVERNOR'
SANG_PANLA = 'PANLALAWIGAN'
MAYOR = 'MAYOR'
VICE_MAYOR = 'VICE-MAYOR'
SANG_BAYAN = 'BAYAN'


def setup(): 
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    cService = webdriver.ChromeService(executable_path='/Users/clarissa/Developer/Projects/Ulirat-Comelec-Data/chromedriver')
   
    driver = webdriver.Chrome(service = cService, options=chrome_options)
    driver.get('https://2022electionresults.comelec.gov.ph/#/coc/0')
    driver.implicitly_wait(10)

    return driver

def choose_area(reg, prov, mun):
    click_filter_btn(REGION)
    click_dropdown(REGION, reg)
    click_filter_btn(PROVINCE)
    click_dropdown(PROVINCE, prov)
    click_filter_btn(MUNICIPALITY)
    click_dropdown(MUNICIPALITY, mun)

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

def get_data_div(position):
    if position in [PRESIDENT, VICE_PRES, SENATOR, PARTY_LIST]:
        div_id = "'resultDiv.'" + position
        results_div = soup.find(id=div_id)
        return results_div
    
    div = soup.select(':-soup-contains("' + position + '")')[-1]

    # Previous line goes to VICE-MAYOR if position is MAYOR
    # Manually navigate to the div I need
    if position == MAYOR:
        div = div.parent.parent
        div = div.parent.parent.parent.find_previous_sibling()
        div = div.findChild("span", {'class': 'ng-binding'})
    
    return div.parent.parent.find_next_sibling()

def get_vote_data(position):
    results_div = get_data_div(position).findChild("div")
    results = results_div.findChildren("div", {'class': 'candidate-result'})

    df = pd.DataFrame(columns=['Candidate','Votes','Percentage'])

    for i in range(0, len(results), 3):
        row = pd.DataFrame({'Candidate':[results[i].text],
                            'Votes': [clean(results[i+1])],
                            'Percentage': [clean(results[i+2])]})
        df = pd.concat([df, row], ignore_index=True)

    return df

def get_stats(position):
    stats_div = get_data_div(position).findChild("div", {'id': 'generalStatisticsVoters'})
    stats = stats_div.findChildren("div", {'class': 'ng-binding'})

    df = pd.DataFrame({stats[1]: [stats[2]],
                       stats[3]: [stats[4]],
                       stats[5]: [stats[6]],
                       stats[7]: [stats[8]]})

    return df

def get_name(area):
    xpath = ' //*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[4]/div'
    xpath += '[' + str(area) + ']'
    xpath += '/nav-filter/div/span/span'
    name = driver.find_element(By.XPATH, xpath)
    return name.text


driver = setup()
choose_area(1, 1, 1)

time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')

pres_votes = get_vote_data(PRESIDENT)

filename = 'data/' + get_name(REGION) + '/' + get_name(PROVINCE) + '.xlsx'
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "DELETE"

ws = wb.create_sheet(get_name(MUNICIPALITY)) 
ws.cell(column=1, row=ws.max_row, value="PRESIDENT")


del wb["DELETE"]
wb.save(filename)

with pd.ExcelWriter(filename, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
    pres_votes.to_excel(writer, sheet_name=get_name(MUNICIPALITY), startrow=ws.max_row) 


# to stack the dataframes on top of eachother
# https://stackoverflow.com/questions/67519829/writing-multiple-data-frame-in-same-excel-sheet-one-below-other-in-python


