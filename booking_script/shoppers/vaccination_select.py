import sys
sys.path.append('..')
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import main as mainScript
# XPATH DOSAGE
dosage_amount_xpath = '//h1[@class="appointmentTypeSelectionstyles__TitleContainer-sc-clkvs7-3 cBbZEX"]'

# Stores the vaccination name and the web element
vax_elem_dict = {}

# Error handling method - TBC 
def no_elem_found():
    print("No vaccination elements were found on the page")


# Finding the elements using XPATH when they load on page
def find_vaccination_elements(driver, delay):
    try:
        vax_elements = WebDriverWait(driver, delay).until(
            EC.visibility_of_all_elements_located((By.XPATH, dosage_amount_xpath)))
    except NoSuchElementException:
        no_elem_found()
    else:
        update_elem_dict(vax_elements)


# Function that sets the vaccination name(key) and element scraped (value) based on vaccination name scraped
def update_elem_dict(elements):
    for elem in elements:
        vax_elem_dict[elem.text] = elem


# Matches user selected vax with a vaccine on the page
def match_user_selected_vax():
    user_in = "Pfizer Dose 2"
    elem_key_list = [*vax_elem_dict]
    selected_vax = ""

    for key in elem_key_list:

        if user_in in key:
            selected_vax = key

    return selected_vax

# Matches the user selected vax element and clicks the element 
def click_selected_vax():
    selected_vaccine = match_user_selected_vax()

    vax_elem_dict[selected_vaccine].click()

# Main run-time -> Calls all other methods 
def select_vaccine_script(driver):
    delay = 10

    find_vaccination_elements(driver, delay)

    click_selected_vax()

    # Fetch and click dynamically generated continue button
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, "button"))).click()


# Returns the amount of additional vaccination form fills required
def get_dose_number():

    selected_vax = match_user_selected_vax()

    if 'Dose 1' in selected_vax:
        return 0
    elif 'Dose 2' in selected_vax:
        return 1
    else:
        return 2


