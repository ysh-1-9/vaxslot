#
# import scrapy
# from scrapy.spiders import SitemapSpider
# import pandas as pd

import requests
import datetime


def get_slot(state, district, age, weeks=8):
    currdate = datetime.datetime.now()
    enddate = currdate + datetime.timedelta(days=30)
    state = state.lower()
    states = {'states': [{'state_id': 1, 'state_name': 'Andaman and Nicobar Islands'}, {'state_id': 2, 'state_name': 'Andhra Pradesh'}, {'state_id': 3, 'state_name': 'Arunachal Pradesh'}, {'state_id': 4, 'state_name': 'Assam'}, {'state_id': 5, 'state_name': 'Bihar'}, {'state_id': 6, 'state_name': 'Chandigarh'}, {'state_id': 7, 'state_name': 'Chhattisgarh'}, {'state_id': 8, 'state_name': 'Dadra and Nagar Haveli'}, {'state_id': 37, 'state_name': 'Daman and Diu'}, {'state_id': 9, 'state_name': 'Delhi'}, {'state_id': 10, 'state_name': 'Goa'}, {'state_id': 11, 'state_name': 'Gujarat'}, {'state_id': 12, 'state_name': 'Haryana'}, {'state_id': 13, 'state_name': 'Himachal Pradesh'}, {'state_id': 14, 'state_name': 'Jammu and Kashmir'}, {'state_id': 15, 'state_name': 'Jharkhand'}, {'state_id': 16, 'state_name': 'Karnataka'}, {'state_id': 17, 'state_name': 'Kerala'}, {'state_id': 18, 'state_name': 'Ladakh'}, {'state_id': 19, 'state_name': 'Lakshadweep'}, {'state_id': 20, 'state_name': 'Madhya Pradesh'}, {'state_id': 21, 'state_name': 'Maharashtra'}, {'state_id': 22, 'state_name': 'Manipur'}, {'state_id': 23, 'state_name': 'Meghalaya'}, {'state_id': 24, 'state_name': 'Mizoram'}, {'state_id': 25, 'state_name': 'Nagaland'}, {'state_id': 26, 'state_name': 'Odisha'}, {'state_id': 27, 'state_name': 'Puducherry'}, {'state_id': 28, 'state_name': 'Punjab'}, {'state_id': 29, 'state_name': 'Rajasthan'}, {'state_id': 30, 'state_name': 'Sikkim'}, {'state_id': 31, 'state_name': 'Tamil Nadu'}, {'state_id': 32, 'state_name': 'Telangana'}, {'state_id': 33, 'state_name': 'Tripura'}, {'state_id': 34, 'state_name': 'Uttar Pradesh'}, {'state_id': 35, 'state_name': 'Uttarakhand'}, {'state_id': 36, 'state_name': 'West Bengal'}], 'ttl': 24}
    
    stateID = [x['state_id'] for x in states['states'] if x['state_name'].lower() ==state]
    if len(stateID)!=1:
        # print('Too many or too few matching states')
        return (False, None)
    else:
        stateID = stateID[0]


    districts = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/'+str(stateID)).json()

    districtID = [x['district_id'] for x in districts['districts'] if x['district_name'].lower() == district]
    if len(districtID)!=1:
        return (False, None)
        # print('Too many or too few matching districts')
        return
    else:
        districtID = districtID[0]

    distindex = 1+districtID-districts['districts'][0]['district_id']
    slots=[]
    for i in range(weeks):
        datestr = (currdate+datetime.timedelta(weeks=i)).strftime('%d-%m-%Y')
        slot7 = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(districtID)+'&date='+datestr).json()
        slot7_age = [ x for x in slot7['centers'] if sum((1 if y['min_age_limit']<=age else 0) for y in x['sessions'])>0]
        slot7_age_available = [x for x in slot7_age if sum(y['available_capacity'] for y in x['sessions'])>0]
        if len(slot7_age_available)>0:
            # print(slot7_age_available)
            slots.append(slot7_age_available)
            return (True, slots)
            # print('Slot Available')
    if len(slots)==0:
        return (False, None)



# get_slot('west bengal','kolkata', 45, 8)



