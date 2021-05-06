import datetime

import requests

from vaxslot import db
from vaxslot.scripts.get_slots import getStateIDs, getDistrictIDs, get_slot, getStates, header
from vaxslot.scripts.models import *

def test_get_slot(districtID,weeks=8):
    currdate = datetime.datetime.now()
    enddate = currdate + datetime.timedelta(days=30)
    sessions18 = {}
    sessions45 = {}
    centers = []
    for i in range(weeks):
        datestr = (currdate + datetime.timedelta(weeks=i)).strftime('%d-%m-%Y')
        slot7 = requests.get(
            'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
                districtID) + '&date=' + datestr, headers=header).json()
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
        return (False, None, None, None)
    else:
        return (True, sessions18, sessions45, centers)



def updateDB():
    # updates the available sessions table in db
    # updates the centers table in db

    stateIDs = getStateIDs()
    districts = sum(getDistrictIDs(x) for x in stateIDs)
    slots = {}
    prevavails18 = sesh.query.filter_by(age=18)
    prevavails45 = sesh.query.filter_by(age=45)
    old18sessions = {x.id:x for x in prevavails18}
    old45sessions = {x.id:x for x in prevavails45}
    finalsessions18 = []
    finalsessions45 = []
    finalcenters =[]
    for districtID in districts:
        available,sessions18,sessions45,centers = test_get_slot(districtID)
        for x in sessions18:
            x.prevCap = old18sessions.get(x.id,x).prevCap
        for x in sessions45:
            x.prevCap = old45sessions.get(x.id,x).prevCap
        finalsessions18+=sessions18
        finalsessions45+=sessions45
        finalcenters+=centers

    sesh.query.delete()
    db.session.add_all(finalsessions18)
    db.session.add_all(finalsessions45)
    db.session.add_all(finalcenters)
    db.session.commit()

updateDB()