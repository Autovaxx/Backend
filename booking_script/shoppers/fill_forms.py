import time
import sys
sys.path.append('..')

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import main as mainScript

# Sample form input data
gender_opts_list = ["Male", "Female", "Self-Identify"]

# Personal info
firstName = mainScript.userDataDict['user_profile']['firstName']
lastName = mainScript.userDataDict['user_profile']['lastName']
gender = mainScript.userDataDict['user_profile']['gender']
DOB = mainScript.userDataDict['user_profile']['dateOfBirth']


# Address
unitNumb = mainScript.userDataDict['address']['unitNumber']
streetNumb =  mainScript.userDataDict['address']['streetNumber']
streetName = mainScript.userDataDict['address']['streetName']
country = mainScript.userDataDict['address']['country']
city = mainScript.userDataDict['address']['city']
province = mainScript.userDataDict['address']['provinceState']
user_postalcode = mainScript.userDataDict['address']['postalCode']
poBox = True

# Contact Details
email = mainScript.userDataDict['email']
phone = mainScript.userDataDict['user_profile']['phoneNumber']

# Emergency Contact
firstECName = mainScript.userDataDict['emergency contact']['firstName']
lastECName = mainScript.userDataDict['emergency contact']['lastName']
relationEC = mainScript.userDataDict['emergency contact']['relationship']
phoneEC = mainScript.userDataDict['emergency contact']['phoneNumber']


# Note --> Potentially Condense code length
def input_personal_info(driver):
    delay = 15
    # Fetching form elements and inputting keys
    # PERSONAL INFO
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        "//input[@name='firstName']"))).send_keys(firstName)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        "//input[@name='lastName']"))).send_keys(lastName)

    Select(WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//select[@name="genderName"]')))).select_by_visible_text(gender)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="birthDate"]'))).send_keys(DOB)

    # ADDRESS
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="address.unit"]'))).send_keys(unitNumb)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="address.streetNumber"]'))).send_keys(streetNumb)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="address.streetName"]'))).send_keys(streetName)

    Select(WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//select[@name="address.country"]')))).select_by_visible_text(country)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="address.city"]'))).send_keys(city)

    Select(WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//select[@name="address.province"]')))).select_by_visible_text(province)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="address.postalCode"]'))).send_keys(user_postalcode)

    # CONTACT DETAILS
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="email"]'))).send_keys(email)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="phone.cell"]'))).send_keys(phone)

    # EMERGENCY CONTACT
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="emergencyContact.firstName"]'))).send_keys(firstECName)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="emergencyContact.lastName"]'))).send_keys(lastECName)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="emergencyContact.relationship"]'))).send_keys(relationEC)

    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//input[@name="emergencyContact.phone"]'))).send_keys(phoneEC)

    # Clicks dynamically generated continue button
    click_continue_btn(driver)


# CONSENT FORM
def fill_consent_form(driver):
    delay = 15

    # Sample user data
    consent_opt_list = ['Patient', 'Guardian', 'Other']

    consent_user = consent_opt_list[0]

    # Fetch consent type and input the users selection
    elem_consent = Select(WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '//select[@name="consentCollectedBy"]'))))

    elem_consent.select_by_visible_text(consent_user)

    # Fetch consent name element and input the users fisrt and last name
    elem_consent_name = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="consentGiverName"]')))

    elem_consent_name.send_keys(firstName + " " + lastName)

    # Select newly generated continue button element and click
    click_continue_btn(driver)

    # CONFIRMATION PAGE
    # Fetch the confirmation checkbox element and select it so its checked
    consent_checkbox_XPATH = '//input[@name="reviewAndConfirmed"]'
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, consent_checkbox_XPATH))).click()


# Fetches dynamically generated continue button element and clicks it to proceed to next page
def click_continue_btn(driver):
    delay = 10

    # Continue button class to fetch
    cont_btn_c = "ismKbC"

    elem_info_cont_btn = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.CLASS_NAME, cont_btn_c)))

    elem_info_cont_btn.click()


# Could potentially refactor code
def fill_previous_vax_info(driver, dose_amount):
    
    # First Dose Form Fill
    if dose_amount >= 1:

        vax1 = mainScript.userDataDict['previous vaccines']['vaccines'][0]['brand']
        vax1_date = mainScript.userDataDict['previous vaccines']['vaccines'][0]['dateOfVaccine']
        vax1_location = mainScript.userDataDict['previous vaccines']['vaccines'][0]['location']
        vax1_options = {}

        vaccine_select1_xpath = "//select[@name='dose1Brand']"
        vaccine_select2_xpath = "//select[@name='dose2Brand']"

        vaccine_date1_xpath = "//input[@name='dose1Date']"
        vaccine_date2_xpath = "//input[@name='dose2Date']"
        
        vaccine_loc1_xpath = "//input[@name='dose1Location']"
        vaccine_loc2_xpath = "//input[@name='dose2Location']"

        elem_vax1 = Select(WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, vaccine_select1_xpath))))

        for option in elem_vax1.options:
            vax1_options[option.text] = option

        for key in vax1_options:
            if vax1 in key:
                elem_vax1.select_by_visible_text(key)

        elem_vax1_date = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, vaccine_date1_xpath)))
        elem_vax1_date.send_keys(vax1_date)


        elem_vax1_location = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, vaccine_loc1_xpath)))
        elem_vax1_location.send_keys(vax1_location)

    # Second Dose Form Fill
    if dose_amount >= 2:

        vax2 = mainScript.userDataDict['previous vaccines']['vaccines'][1]['brand']
        vax2_date = mainScript.userDataDict['previous vaccines']['vaccines'][1]['dateOfVaccine']
        vax2_location = mainScript.userDataDict['previous vaccines']['vaccines'][1]['location']
        vax2_options = {}

        elem_vax2 = Select(WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, vaccine_select2_xpath))))

        for option in elem_vax2.options:
            vax2_options[option.text] = option

        for key in vax2_options:
            if vax2 in key:
                elem_vax2.select_by_visible_text(key)

        elem_vax2_date = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, vaccine_date2_xpath)))
        elem_vax2_date.send_keys(vax2_date)

        elem_vax2_location = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, vaccine_loc2_xpath)))
        elem_vax2_location.send_keys(vax2_location)

# def get_booking_details(driver): 
#     details_xpath1 = "//div[@class='patientRegistrationstyles__Body-sc-13kcclq-15 fluShotSdmCompletionstyles__SectionBody-sc-1oep12q-1 idkCbA']"
#     details_xpath2 = "//div[@class='patientRegistrationstyles__Body-sc-13kcclq-15 fluShotSdmCompletionstyles__SectionBody-sc-1oep12q-1 idkCbA']"
#     elem_booking_details1 = WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located((By.XPATH, details_xpath1)))

#     elem_booking_details2 = WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located((By.XPATH, details_xpath2)))            
    
#     print(elem_booking_details1.text)
#     print(elem_booking_details2.text)

def get_booking_details(driver): 
    details_xpath1 = '//div[@class="patientRegistrationstyles__Body-sc-13kcclq-15 bookingDetailsstyles__Content-sc-6q2a18-4 iezHIn"]'

    elem_booking_details1 = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, details_xpath1)))

    print(elem_booking_details1.text)




def fill_personal_form(driver, dose_number):
    fill_previous_vax_info(driver, dose_number)
    input_personal_info(driver)
    get_booking_details(driver)
    driver.quit()
    # THIS BELOW SUBMITS FORM>>>> 
    #click_continue_btn(driver)
