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


function('west bengal','kolkata', 45, 8)



