#
# import scrapy
# from scrapy.spiders import SitemapSpider
# import pandas as pd

import requests
import datetime

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
            slots.append(slot7_age_available)
            return (True, slots)
            # print('Slot Available')
    if len(slots)==0:
        # print('No slots Available')
        return (False, None)        
        
        
# [{'emailID':'adityaranjha786@gmail.com','state':'west bengal','district':'kolkata', 'age': 18},{....},{....}]

# {'andhra pradesh':{'kalimpondi': [usr1,usr2...], 'machu pichu': [usr3, usr4...]} }

def updateDB():
    # get states and districts possibly locally
    # look through the current database of (districtID,age) -> [list of centers with availability within next 12 weeks]
    # for every state,district,age, query the cowin thing and update to a local variable
    # go through the new db. if the session was there before and numbers same, dont do anything. if the numbers changes, save it to a changedDB. if it wasnt there before, save it to a newlyaddedDB.
    # finally update the on disk db to the new db.
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


# get_slot('west bengal','kolkata', 45, 8)



