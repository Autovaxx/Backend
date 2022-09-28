import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

serv = Service(os.environ.get("CHROMEDRIVER_PATH"))

# Setting chrome options
chrome_opts = webdriver.ChromeOptions()
chrome_opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_opts.add_argument("--headless")
chrome_opts.add_argument('window-size=1920x1080')
chrome_opts.add_argument("--disable-dev-shm-usage")
chrome_opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=serv, options=chrome_opts)

# # driver = webdriver.Chrome(service=serv, options=chrome_options)

# # # Connecting to this page
driver.get("https://www.google.com")

# # Script Variables
city = 'Mississauga weather'
delay = 10
location_x = '//div[@id="wob_loc"]'
date_time_x = '//div[@id="wob_dts"]'
info_x = '//div[@class="Ab33Nc"]'
input_x = '//input[@class="gLFyf gsfi"]'

# # Entering city name and hitting enter key 
WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, input_x))).send_keys(city)
WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, input_x))).send_keys(u'\ue007') 

# # Grabbing weather data 
location = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, location_x))).text
date_time = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, date_time_x))).text
weather_details = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, info_x))).text

# Python object storing weather data
details_obj = [{
    "location": location,
    "date_time": date_time,
    "weather": weather_details
}]


# Converting object to json
details_obj_json = json.dumps(details_obj)

# Printing object so its in the I/O stream for node to fetch
print(f'Data: ${details_obj_json}')

# Closing the browser
driver.close()


