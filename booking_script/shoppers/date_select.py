from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_date_script(driver, appointment_date_time):
    # Storing the xpath using the date-time nested in the label
    timeslot_xpath = f'//input[@value="{appointment_date_time}"]//parent::label'

    # Time to wait for the element to appear on the page
    delay = 10

    # Selecting the timeslot
    elem_date_time = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, timeslot_xpath)))

    # Clicking the timeslot
    elem_date_time.click()

    # Storing the class name of the generated continue button
    btn_c_name = "ismKbC"

    # Storing modal button class name
    m_btn_c_name = "bZCKYm"

    # # Selecting the continue button element and clicking it
    WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.CLASS_NAME, btn_c_name))).click()

    # # Selecting the continue button on the modal and clicking it
    WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.CLASS_NAME, m_btn_c_name))).click()
