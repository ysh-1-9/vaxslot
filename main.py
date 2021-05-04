#
# import scrapy
# from scrapy.spiders import SitemapSpider

import requests
# import pandas as pd
import datetime


def function(state, district, age, weeks):
    currdate = datetime.datetime.now()
    enddate = currdate + datetime.timedelta(days=30)
    state = state.lower()
    states = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states').json()
    # print(states['states'][0])

    stateID = [x['state_id'] for x in states['states'] if x['state_name'].lower() ==state]
    if len(stateID)!=1:
        print('Too many or too few matching states')
        return
    else:
        stateID = stateID[0]

    districts = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/'+str(stateID)).json()

    districtID = [x['district_id'] for x in districts['districts'] if x['district_name'].lower() == district]
    if len(districtID)!=1:
        print('Too many or too few matching districts')
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
            print(slot7_age_available)
            slots.append(slot7_age_available)
            print('Slot Available')
    if len(slots)==0:
        print('No slots Available')



function('west bengal','kolkata', 45, 8)



