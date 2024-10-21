from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
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

positions = [PRESIDENT, VICE_PRES, SENATOR, PARTY_LIST, 
             MEMBER_HOR, GOVERNOR, VICE_GOV, SANG_PANLA, MAYOR, VICE_MAYOR, SANG_BAYAN]

title = {PRESIDENT: "PRESIDENT PHILIPPINES",
         VICE_PRES: "VICE PRESIDENT PHILIPPINES",
         SENATOR: "SENATOR PHILIPPINES",
         PARTY_LIST: "PARTY LIST PHILIPPINES",
         MEMBER_HOR: "MEMBER, HOUSE OF REPRESENTATIVES",
         GOVERNOR: "PROVINCIAL GOVERNOR",
         VICE_GOV: "PROVINCIAL VICE-GOVERNOR",
         SANG_PANLA: "MEMBER, SANGGUNIANG PANLALAWIGAN",
         MAYOR: "MAYOR",
         VICE_MAYOR: "VICE-MAYOR",
         SANG_BAYAN: "MEMBER, SANGGUNIANG BAYAN"}

# Number 4 is skipped on the website
region_idx = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
global driver
global soup
global wb


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

    df = pd.DataFrame({stats[1].text: [stats[2].text],
                       stats[3].text: [stats[4].text],
                       stats[5].text: [stats[6].text],
                       stats[7].text: [stats[8].text]})

    return df

def get_name(area):
    xpath = ' //*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[4]/div'
    xpath += '[' + str(area) + ']'
    xpath += '/nav-filter/div/span/span'
    name = driver.find_element(By.XPATH, xpath)
    return name.text

def init_workbook():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "DELETE"
    wb.save(filename)
    return wb

def write_title(filename, position, curr_row):
    wb = openpyxl.load_workbook(filename)
    ws = wb[get_name(MUNICIPALITY)]
    ws.cell(column=1, row=curr_row, value=title[position])
    wb.save(filename)

def write_data(filename):
    curr_row = 1

    for position in positions:
        votes = get_vote_data(position)
        stats = get_stats(position)

        write_title(filename, position, curr_row)
        curr_row += 1

        with pd.ExcelWriter(filename, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            votes.to_excel(writer, sheet_name=get_name(MUNICIPALITY), startrow=curr_row, index=False)
            curr_row += votes.shape[0] + 2
            stats.to_excel(writer, sheet_name=get_name(MUNICIPALITY), startrow=curr_row, index=False) 
            curr_row += stats.shape[0] + 4
        



#WHAT ARE WE DOING RIGHT NOW?
#We're gonna test out print(region_name), which refers to the National Positions - "name"
#And then compare it with the dropdown Menu
#But first we check that the menu is there
#only have to check the municipality one because that's what we're working on right now 
reg = 1
prov = 1
muni = 1

failures = 0
end = False


while(muni < 3):
    try:
        driver = setup()
        choose_area(reg, prov, muni)

    except NoSuchElementException:
        driver.close()
        if failures == 2:
            break
        else:
            failures += 1
        continue

    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    target_region = driver.find_element(By.XPATH, '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[4]/div[4]/nav-filter/div/span/span')

    filename = 'data/' + get_name(REGION) + '/' + get_name(PROVINCE) + '.xlsx'

    if muni == 1:
        wb = init_workbook()
        ws = wb.create_sheet(get_name(MUNICIPALITY)) 
        del wb["DELETE"]
    else:
        wb = openpyxl.load_workbook(filename)
        ws = wb.create_sheet(get_name(MUNICIPALITY)) 


    wb.save(filename) 
    write_data(filename)
    driver.close()


    muni += 1
    failures = 0


#1. If region name doesn't match the header (national positions - ____
#2. If the thing loaded at all - load it again 3 x


# to stack the dataframes on top of eachother
# https://stackoverflow.com/questions/67519829/writing-multiple-data-frame-in-same-excel-sheet-one-below-other-in-python


