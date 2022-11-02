from datetime import datetime as dt

# ELEM DATE FORMAT: 2022-10-11 00:00:00
# START DATE: 2022-10-06 00:00:00
# START DATE: 2022-10-08 00:00:00

elem_date_l = dt.strptime('2022-10-05', '%Y-%m-%d')
elem_date_h = dt.strptime('2022-10-11', '%Y-%m-%d')

s_d = dt.strptime('2022-10-06', '%Y-%m-%d')
e_d = dt.strptime('2022-10-12', '%Y-%m-%d')

# Date = date-time object
# Range = array of 2 DT objects

range = [elem_date_l, elem_date_h]

def check_date_within_range(date, date_range):

    date_lower_bound = date_range[0]
    date_higher_bound = date_range[1]

    if date_lower_bound <= date <= date_higher_bound:
        return True
    else: 
        return False
    
print(check_date_within_range(e_d, range))
