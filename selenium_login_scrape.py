import json
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument('--headless')

service = Service('./chromedriver')
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://scrapingclub.com/exercise/basic_login/')


WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'id_name')))

login = driver.find_element(by=By.XPATH, value='//input[@id="id_name"]')
password = driver.find_element(by=By.XPATH, value='//input[@id="id_password"]')

login.send_keys('scrapingclub')
password.send_keys('scrapingclub')

button_login = driver.find_element(by=By.XPATH, value="//button[@type='submit']")

button_login.click()



#WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/p"), "You have successfully login in, Congratulations"))

driver.get('https://scrapingclub.com/exercise/list_infinite_scroll/')

#WebDriverWait(driver, 7).until(EC.text_to_be_present_in_element((By.XPATH, "/html/head/title"), 'Scraping Infinite Scrolling Pages (Ajax) | ScrapingClub'))

actions = ActionChains(driver)

first_height = driver.execute_script("return document.body.scrollHeight;")
print(first_height)

while True:
    pause_time = random.randint(5, 7)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight;")
    print(new_height)
    if new_height == first_height:
        break
    first_height = new_height

rows = driver.find_elements(By.CLASS_NAME, value="card")

rows_list = []
try:
    for row in rows:
        image = row.find_element(By.TAG_NAME, "img").get_attribute('src')
        link = row.find_element(By.TAG_NAME, "a").get_attribute('href')
        name = row.find_element(by=By.XPATH, value=".//h4[@class='card-title']/a").text
        price = row.find_element(by=By.XPATH, value=".//h4[@class='card-title']/following-sibling::h5").text
        tmp_dict = {
            'image': image,
            'link': link,
            'name': name,
            'price': price
        }
        rows_list.append(tmp_dict)
except:# Не знаю как обойти, чтоб последний элемент card не искался
    pass

driver.quit()

with open('rows_list.json', 'w', encoding='utf-8') as jf:
    json.dump(rows_list, jf)
