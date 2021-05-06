import datetime

import requests

from vaxslot.scripts.get_slots import getDistricts, header
from vaxslot.scripts.models import sesh, Center


def test():
    alldists=[]
    for i in range(1,37):
        districts = getDistricts(i)
        for x in districts:
            alldists.append(x)
    file1 = open('districts.txt', 'w')
    alldists.sort(key=lambda x: int(x['district_id']))
    alldists = [str(x['district_id'])+': '+x['district_name']+'\n' for x in alldists]
    file1.writelines(alldists)
    print(len(alldists))
    file1.close()

def test27(districtID,weeks=1):
    currdate = datetime.datetime.now()
    enddate = currdate + datetime.timedelta(days=30)
    sessions18 = []
    sessions45 = []
    centers = []
    for i in range(weeks):
        datestr = (currdate + datetime.timedelta(weeks=i)).strftime('%d-%m-%Y')
        slot7 = requests.get(
            'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
                districtID) + '&date=' + datestr, headers=header).json()
        print(slot7)
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
        print('Slots Available')
        return (True, sessions18, sessions45, centers)

test27(27)