import re
import time
import sys
sys.path.append('..')
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime as dt, date, timedelta
from shoppers import vaccination_select as vax_select, date_select
import main as mainScript



# Sample time range user is available for appointment
user_time_start = "09:00:00-04:00"
user_time_end = "8:00:00-04:00"

# Sample date range for a user
user_date_start = mainScript.userDataDict['search_preferences']['startDate']
user_date_end = mainScript.userDataDict['search_preferences']['endDate']

delay = 20

# Sample user input - represents 10km range
user_distance_range = 10

# Distance element class used to select the div containing the location
distance_c_name = "jENuth"

# Used to store the distance element object
dist_elem_list = []

# Filter for ints and floats - used to select distance value only from location elements
regex_float_filter = re.compile(r'[-+]?(?:\d*\.\d+|\d+)')

def select_location_script(driver):
    # Fetching all the divs that contain a distance element
    elem_dist = WebDriverWait(driver, delay + 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                                                             distance_c_name)))

    # Converting distance text to float and storing only objects within user specified distance to distance_elem_list
    for dist in elem_dist:

        temp_dist = float(regex_float_filter.search(dist.text).group(0))

        if temp_dist <= user_distance_range:
            dist_elem_list.append(dist) 

    # Selecting the initial location
    if len(dist_elem_list) > 0:
        dist_elem_list[0].click()
    
    # NOTE: Function below is not "Functional" yet :D
    check_available_dates(driver)


# <------------------------- Code below is in development and not functional yet! :) -------------------------->

# List of dates that the user can select
user_available_dates = []

user_match_date = ""
user_final_date_time = ""

# Retrieves all the available dates of the user
def get_user_available_dates(start_date, end_date):

    # Converting start and end date to datetime objects so its easier to use compare operations
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    end_date = dt.strptime(end_date, '%Y-%m-%d')

    # Difference between start and end date
    time_delta = end_date - start_date  

    # Stores all the dates the user is available for an appointment 
    available_dates = []

    # Going through the dates within the range and adding them to the available dates list
    for i in range(time_delta.days + 1):
        possible_date = start_date + timedelta(days=i)
        available_dates.append(possible_date)

    return available_dates


def check_available_dates(driver):

    is_date_time_match = False
    location_index = 0
    user_date_range = get_user_available_dates(user_date_start, user_date_end)

    # Convert end date to shoppers date format for comparison use
    end_date = dt.strptime(user_date_end, '%Y-%m-%d')

    # While there is no date time match and we're still searching within our location list
    while not is_date_time_match and location_index < (len(dist_elem_list)-1):

        # Flag to keep track of if a time-slot is found
        found_timeslot = False

        # Initial check to see if user date exists within the date header range at the currently selected location
        stay_within_dates = check_if_stay_within_date_header(end_date, driver)

        # When the location date header does not match the user dates we check if the next button is enabled at the current location.
        # If the next button is enabled, we click it and check the next header date until we either find a date match or the button is disabled.
        # If the button is disabled, we move onto the next location and repeat the process until the user date is within the location date header range.
        while not stay_within_dates:

            if check_if_next_btn_enabled(driver):
                go_next_week()
                stay_within_dates = check_if_stay_within_date_header(end_date, driver)

            else:

                go_next_location(location_index)
                location_index += 1     
                
        # Once our date is within the location header range, we check for a time slot. If we find an available slot, we break out of the loop and set 
        # our flag to true. If no timeslot is found, we'll head on over to the next location and repeat the date header range chceck and so on. 
        if stay_within_dates:
            found_timeslot = check_for_timeslot(driver)

            if found_timeslot:
                is_date_time_match = True
                break
            else:
                go_next_location(location_index) 
                location_index += 1   
                  

# NOTE TAKE A LOOK AT THIS IN THE FUTURE NEEDS MORE WORK ON THE DATE RANGE LOGIC FOR MATCHING
def check_if_stay_within_date_header(end_date, driver):

    # Targeted class name of the date header element
    calendar_header_c = 'kZWAKb'

    header_date_range = []

    # Fetching the header element containing the date range on the shoppers page
    elem_header = WebDriverWait(driver, delay + 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                                                               calendar_header_c)))
    
    # Extracting the date header strings (array of strings)
    date_header_list = elem_header[0].text.split(' - ')

    # Generating a header range 
    for elem in date_header_list:

        # Converting element to date time format so we can use comparison operators on them. Also removing the weekday name
        elem_datetime = dt.strptime(elem, '%a %b %d').strftime("%b %d")

        # Converting back to date time object for comparison
        elem_datetime = dt.strptime(elem_datetime, '%b %d')

        # Assigning a valid year to the date format
        elem_datetime = elem_datetime.replace(year=dt.now().year)

        # Adding the fetched date to the range list
        header_date_range.append(elem_datetime)

    # Check to see if user end date is within header - if true, stay within dates. If false, move next. 
    stay_within_dates = check_date_within_range(end_date, header_date_range)

    return stay_within_dates

# Look for a timeslot on the current page that fits the users requirements and selecting it if found
def check_for_timeslot(driver):

    found_timeslot = False

    # Getting the timeslots on the page
    timeslots = get_timeslots(driver)

    # Converting our start datetime and end datetime to a string that we can use to query similar datetime fields on page
    date_time_start = create_date_time_timezone_string(user_date_start, user_time_start)
    date_time_end = create_date_time_timezone_string(user_date_end, user_time_end)

    for t in timeslots:
        if date_time_start <= t.get_attribute("value") <= date_time_end:

            date_to_select = t.get_attribute("value")
            date_select.select_date_script(driver, date_to_select)

            found_timeslot = True

            break

    return found_timeslot

# Fetches the timeslots located within the current calendar
def get_timeslots(driver):

    timeslot_x = '//input[@name="startDateTime"]'

    timeslots = WebDriverWait(driver, delay).until(
        EC.presence_of_all_elements_located((By.XPATH, timeslot_x))
    )
    return timeslots

# Fetches the "Next 7 days button"
def get_next_week_btn(driver):
    next_week_btn_x = "//button[span[span[contains(text(), 'Next ')]]]"

    next_week_btn = WebDriverWait(driver, delay).until(
        EC.visibility_of_element_located((By.XPATH, next_week_btn_x)))

    return next_week_btn

# Selecting the "Next 7 Days" button
def go_next_week(driver):

    next_week_btn = get_next_week_btn(driver)

    next_week_btn.click()

# Creating a string to fit the format of the shoppers page
def create_date_time_timezone_string(u_date, u_time):

    return u_date + "T" + u_time

# Checks the next location if its avaialble in the list
def go_next_location(i):

    if i < (len(dist_elem_list)-1):

        dist_elem_list[i].click()



# Checks if the "Next 7 Days" button is enabled
def check_if_next_btn_enabled(driver):

    next_week_btn = get_next_week_btn(driver)

    if next_week_btn.is_enabled():
        return True
    else:

        return False



# Checking the current page to see if timeslots empty
def is_timeslots_empty(driver):

    # Swap to input radio - Class being targeted to scrape the element
    timeslot_c = 'ISUJv'

    try:
        time_elements = WebDriverWait(driver, delay).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, timeslot_c)))
    except NoSuchElementException:
        return True

    else:
        return False

# Checks to see if a particular date is within a range of dates
def check_date_within_range(date, date_range):

    date_lower_bound = date_range[0]
    date_higher_bound = date_range[1]

    if date_lower_bound <= date <= date_higher_bound:
        return True
    else: 
        return False