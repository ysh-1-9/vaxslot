
import time


import requests
import datetime


from vaxslot.scripts.db_imports_exports import header
from vaxslot.scripts.models import Center, sesh


def get_slot(districtID, weeks=1):                         #all sessions with available space
    currdate = datetime.datetime.now()
    enddate = currdate + datetime.timedelta(days=30)
    sessions18 = []
    sessions45=[]
    centers=[]
    for i in range(weeks):
        datestr = (currdate + datetime.timedelta(weeks=i)).strftime('%d-%m-%Y')
        slot7 = requests.get(
            'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
                districtID) + '&date=' + datestr,headers=header)
        try:
            slot7=slot7.json()
        except:
            print('Sleeping......')
            time.sleep(300)
            print('Awake')
            while(True):
                try:
                    slot7 = requests.get(
                        'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
                            districtID) + '&date=' + datestr, headers=header).json()
                    break
                except:
                    time.sleep(15)
        # slot7_age = [x for x in slot7['centers'] if
        #              sum((1 if y['min_age_limit'] <= age else 0) for y in x['sessions']) > 0]
        # slot7_age_available = [x for x in slot7_age if sum(y['available_capacity'] for y in x['sessions']) > 0]
        # centerdict={}
        for x in slot7['centers']:
            # if x['center_id'] in centerdict:
            #     print('Duplicate centers at district ',districtID,' with ID', x['center_id'])
            #     exit()
            # else:
            #     centerdict[x['center_id']] = x
            centers.append(Center(x))
            for y in x['sessions']:
                if y['available_capacity']>0:
                    if y['min_age_limit']==18:
                        sessions18.append(sesh(y, districtID, x['center_id']))
                    else:
                        sessions45.append(sesh(y, districtID, x['center_id']))

    if len(sessions18) + len(sessions45) == 0:
        # print('No slots Available')
        return (False, sessions18,sessions45,centers)
    else:
        return(True,sessions18,sessions45,centers)

    # [{'emailID':'adityaranjha786@gmail.com','state':'west bengal','district':'kolkata', 'age': 18},{....},{....}]


# {'andhra pradesh':{'kalimpondi': [usr1,usr2...], 'machu pichu': [usr3, usr4...]} }

# get_slots returns a boolean, 2 lists of session objects and a list of Center objects
# each center from cowin API is a dict of the format:

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

# ek db will have session objects - done
# ek database will take centreID and give me center ke poore details.  - done




def notify(districtID,sessions,users,centers):
    # go through the users in the (districtID,age)->list of users for every districtID and age
    #  for each districtID,age come up with 3 things - a> email in general likhna hai?, b> updates kya kya dene hai and c> newadditions kya kya batane hai
    # then for each districtID send (or don't) the respective email to all users from that category
    additions=[]
    updates=[]
    for x in sessions:
        if x.prevCap==0:                  #can get rid of createEmail and do what it does here only for better speed
            additions.append(x)
        else:
            updates.append(x)
    s = createEmail(updates,additions,centers)
    #send s



    pass


def createEmail(updates, additions, centerdeets):
    s =""
    for x in updates:
        if x.centerID in centerdeets:
             s +=  "<tr>" + "<td>" + x.currCap + "</td>" + "<td>" + x.date + "</td>" + "<td>" + x.age + "</td>" + """<td width = "15%">""" + centerdeets[x.centerID].name + "</td>" + """<td width = "45%">""" + centerdeets[x.centerID].address+ "</td>" + "</tr>" 

        
    for x in additions:
        if x.centerID in centerdeets:
            s +=  "<tr>" + "<td>" + x.currCap + "</td>" + "<td>" + x.date + "</td>" + "<td>" + x.age + "</td>" + """<td width = "15%">""" + centerdeets[x.centerID].name + "</td>" + """<td width = "45%">""" + centerdeets[x.centerID].address+ "</td>" + "</tr>" 

        
    return s



