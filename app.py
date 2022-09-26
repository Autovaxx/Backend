import json
from selenium import webdriver
import os

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.chrome.service import Service
# serv = Service("chromedriver.exe")
# opts = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=serv, options=opts)

# Setting chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

# # Connecting to this page
driver.get("https://www.google.com/search?q=mississauga+weather&rlz=1C1UEAD_enCA995CA995&oq=miss&aqs=chrome.0.69i59j46i433i512j69i57j69i59j69i61j69i65j69i61j69i60.520j0j7&sourceid=chrome&ie=UTF-8")

# # # Script Variables
# # city = 'Mississauga weather'
# delay = 10
# location_x = '//div[@id="wob_loc"]'
# date_time_x = '//div[@id="wob_dts"]'
# info_x = '//div[@class="Ab33Nc"]'
# # input_x = '//input[@class="gLFyf gsfi"]'

# # # Entering city name and hitting enter key 
# # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, input_x))).send_keys(city)
# # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, input_x))).send_keys(u'\ue007') 

# # # Grabbing weather data 
# location = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, location_x))).text
# date_time = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, date_time_x))).text
# weather_details = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, info_x))).text

# Python object storing weather data
# details_obj = [{
#     "location": location,
#     "date_time": date_time,
#     "weather": weather_details
# }]
# details_obj = [{
#     "location": "HI",
#     "date_time": "BYE",
#     "weather": "YO"
# }]
# Closing selenim instance after data is fetched/process is closed
# driver.close()

# Converting object to json
details_obj_json = json.dumps(driver.page_source)

# Printing object so its in the I/O stream for node to fetch
print(details_obj_json[10])

driver.close()
