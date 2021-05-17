import datetime

import requests
import time
from vaxslot import db
from vaxslot.scripts.db_imports_exports import getStateIDs, getDistrictIDs, getStates, header
from vaxslot.scripts.get_slots import get_slot
from vaxslot.scripts.models import *

def test_get_slot(districtID,weeks=1):
    currdate = datetime.datetime.now()
    enddate = currdate + datetime.timedelta(days=30)
    sessions18 = []
    sessions45 = []
    centers = []
    for i in range(weeks):
        datestr = (currdate + datetime.timedelta(weeks=i)).strftime('%d-%m-%Y')
        slot7 = requests.get(
            'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
                districtID) + '&date=' + datestr, headers=header)
        try:
            slot7=slot7.json()
        except:
            print('Waiting......')
            time.sleep(300)
            slot7 = requests.get(
                'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
                    districtID) + '&date=' + datestr, headers=header).json()
        # print(slot7)
        # slot7_age = [x for x in slot7['centers'] if
        #              sum((1 if y['min_age_limit'] <= age else 0) for y in x['sessions']) > 0]
        # slot7_age_available = [x for x in slot7_age if sum(y['available_capacity'] for y in x['sessions']) > 0]
        for x in slot7['centers']:
            centers.append(Center(x))
            for y in x['sessions']:
                if y['min_age_limit'] == 18:
                    sessions18.append(sesh(y, districtID, x['center_id']))
                else:
                    sessions45.append(sesh(y, districtID, x['center_id']))

    if len(sessions18) + len(sessions45) == 0:
        print('No slots Available')
        return (False, sessions18, sessions45, centers)
    else:
        return (True, sessions18, sessions45, centers)



def updateDB(districtID, db_data):
    # updates the available sessions table in db
    # updates the centers table in db

    available,sessions18,sessions45,centers = get_slot(districtID)
    # size = len(centers)
    # sum+=size
    # print(str(districtID)+': '+str(size))
    # file1.write(str(districtID)+' '+str(size)+'\n')
    for x in sessions18:
        if x.id in db_data[districtID][0]:
            x.prevCap = db_data[districtID][0][x.id].currCap
    for x in sessions45:
        if x.id in db_data[districtID][1]:
            x.prevCap = db_data[districtID][1][x.id].currCap
    db_data[districtID][0] = {x.id: x for x in sessions18}
    db_data[districtID][1] = {x.id: x for x in sessions45}
    db_data[districtID][2] = {x.id: x for x in centers}
    return sessions18, sessions45, centers

