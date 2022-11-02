import json, sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# Script imports
from shoppers import shopper_script

# Fetching user JSON data and converting it to a dictonary 
userDataJson = sys.argv[1]
userDataDict = json.loads(userDataJson)

# Storing the website URL
website = "https://shoppersdrugmart.medmeapp.com/schedule/groups/COVID-19-Vaccine"

# Selecting driver that will help us scrape the website. Webdriver for chrome.
serv = Service('D:\Python\AutoVax\chromedriver.exe')

chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_argument("--widow-size=1920,1080")

driver = webdriver.Chrome(service=serv, options=chrome_opts)
driver.maximize_window()
# Opening a chromedriver window using the command below.
driver.get(website)

# Running shoppers script
try:
    shopper_script.book_appointment(driver)
except Exception as e: 
    pass
else: 
    pass


