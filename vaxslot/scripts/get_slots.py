#
# import scrapy
# from scrapy.spiders import SitemapSpider
# import pandas as pd

import requests
import datetime
import sqlite3


def getStates():
    return requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states').json()

def getStateIDs():
    states = getStates()
    return [x['state_id'] for x in states['states']]

def getDistricts(stateID):
    return requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/'+str(stateID)).json()

def getDistrictIDs(stateID):
    districts = getDistricts(stateID)
    districtID = [x['district_id'] for x in districts['districts']]
    


def get_slot(districtID, age, weeks=8):
    currdate = datetime.datetime.now()
    enddate = currdate + datetime.timedelta(days=30)
    slots=[]
    for i in range(weeks):
        datestr = (currdate+datetime.timedelta(weeks=i)).strftime('%d-%m-%Y')
        slot7 = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(districtID)+'&date='+datestr).json()
        slot7_age = [ x for x in slot7['centers'] if sum((1 if y['min_age_limit']<=age else 0) for y in x['sessions'])>0]
        slot7_age_available = [x for x in slot7_age if sum(y['available_capacity'] for y in x['sessions'])>0]
        if len(slot7_age_available)>0:
            # print(slot7_age_available)
            slots+= slot7_age_available
            return (True, slots)
            # print('Slot Available')
    if len(slots)==0:
        # print('No slots Available')
        return (False, None)        
        
        
# [{'emailID':'adityaranjha786@gmail.com','state':'west bengal','district':'kolkata', 'age': 18},{....},{....}]

# {'andhra pradesh':{'kalimpondi': [usr1,usr2...], 'machu pichu': [usr3, usr4...]} }

#get_slots returns a list of centers
# each center is a dict of the format:

# {
#       "center_id": 1234,
#       "name": "District General Hostpital",
#       "name_l": "",
#       "address": "45 M G Road",
#       "address_l": "",
#       "state_name": "Maharashtra",
#       "state_name_l": "",
#       "district_name": "Satara",
#       "district_name_l": "",
#       "block_name": "Jaoli",
#       "block_name_l": "",
#       "pincode": "413608",
#       "lat": 28.7,
#       "long": 77.1,
#       "from": "09:00:00",
#       "to": "18:00:00",
#       "fee_type": "Free",
#       "vaccine_fees": [
#         {
#           "vaccine": "COVISHIELD",
#           "fee": "250"
#         }
#       ],
#       "sessions": [
#         {
#           "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#           "date": "31-05-2021",
#           "available_capacity": 50,
#           "min_age_limit": 18,
#           "vaccine": "COVISHIELD",
#           "slots": [ "FORENOON", "AFTERNOON"]
#         }
#       ]
#     }

# instead if i return 3 things:
# ek toh list of sessionID, available cap
# dusra a dictionary from sessionID to centerID
# teesra a centreID to center details ka pura dict


# ek datadase mein index by district, age, list of session ids and available capacities ->allsh
# ek database mein index by district, age, list of session ids that changed availability -> updsh
#  ek database mein index by district, age, list of session ids that werent available before but are now ->newsh
# ek database will take session id and give me all the centreID->centresh
# ek database will take centreID and give me center ke poore details.

def updateDB():
    # get states and districts possibly locally
    # look through the current database of (districtID,age) -> [list of centers with availability within next 12 weeks]
    # for every state,district,age, query the cowin thing and update to a local variable
    # go through the new db. if the session was there before and numbers same, dont do anything. if the numbers changes, save it to a changedDB. if it wasnt there before, save it to a newlyaddedDB.
    # finally update the on disk db to the new db.
    connslots = sqlite3.connect('slots.db')
    connupdates = sqlite3.connect('updates.db')
    connnews = sqlite3.connect('news.db')

    stateIDs = getStateIDs()
    districts = sum(getDistricts(x) for x in stateIDs)
    slots={}
    for districtID in districts:
        slots[districtID]=[]
        for age in {18,45}:
            slots[districtID].append(get_slot(districtID,age))



    pass

def notify():
    # go through the users in the (districtID,age)->list of users for every districtID and age
    #  for each districtID,age come up with 3 things - a> email in general likhna hai?, b> updates kya kya dene hai and c> newadditions kya kya batane hai
    # then for each districtID send (or don't) the respective email to all users from that category
    pass


def createEmail(updates,additions):
    # returns a parsed sexy ass email object ya whatever
    pass

def addUser(emailID, state, district, age):
    # create an email about ALL available stuff as additions, w some welcome bs
    # send email
    # save user to functional database
    # save user to permanent database
    pass

def deleteUser(emailID):
    # remove user from functional database
    # send bullshit liberal email
    pass


get_slot(710, 45, 8)



