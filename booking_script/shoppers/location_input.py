import time
import sys
sys.path.append('..')
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import main as mainScript

# Sample user input


# Geolocation element X-PATH
location_xpath = '//input[@placeholder="Search"]'

def location_input_script(driver, delay):


    user_postalcode = mainScript.userDataDict['address']['postalCode']

    elem_geolocation = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, location_xpath)))

    # Entering the postal code in the MedMe app
    elem_geolocation.send_keys(user_postalcode)

    # Submitting the postal code so the map displays location
    elem_geolocation.send_keys(Keys.ENTER)

