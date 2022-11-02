import time
from shoppers import vaccination_select as vax_select
from shoppers import location_select as loc_select
from shoppers import location_input as loc_input
from shoppers import fill_forms as form_fill

def book_appointment(driver):
    vax_select.select_vaccine_script(driver) 
 
    loc_input.location_input_script(driver, 10) 

    loc_select.select_location_script(driver) # TODO UPDATE USER DISTANCE PREF

    dose_number = vax_select.get_dose_number()

    form_fill.fill_personal_form(driver, dose_number) # TODO UPDATE DICT

    form_fill.fill_consent_form(driver) # TODO UPDATE DICT
