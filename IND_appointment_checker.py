import time
import requests
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

def listToString(list):
    result = ""
    for elem in list:
        result += elem + ", "
    return result

def send_line_notify(message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_token}'}
    data = {'message': f'message: {message}'}
    requests.post(line_notify_api, headers = headers, data = data)

def html_display(html_str):
    with open(html_dir, mode="w") as f:
        f.write(html_str)
    webbrowser.open(html_dir)

#fix definition
cd = "this file location"
html_dir = cd + '/index.html'
line_token = "your line token"
page_url = 'https://oap.ind.nl/oap/en/#/doc'

op = webdriver.ChromeOptions()
op.add_experimental_option('excludeSwitches', ['enable-logging']) #hidden USB error message
op.add_argument('--headless') #hidden browser

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)
driver.get(page_url)
dropdown = driver.find_element("name", "desk")
select = Select(dropdown)

count = 0
while True:
    count += 1
    try:
        select.select_by_value("2: Object") #prep select
        time.sleep(1)
        select.select_by_value("1: Object") #main select
        time.sleep(1)
        page_source = driver.page_source
        #html_display(page_source)
        soup = BeautifulSoup(page_source, 'html.parser')
        abvl_btn = soup.find_all('button', class_='btn btn-sm available btn-default')
        date_list = [elem.find('span').text for elem in abvl_btn]
        abvl_date = listToString(date_list)
        if len(date_list) > 0:
            send_line_notify(abvl_date + '\n' + page_url)
        print(str(count) + ":working")
    except Exception as e:
        print(str(count) + ":error")