import requests
import json
from vaxslot import db_data, districtname_to_id
from vaxslot.scripts.models import sesh, Center, User
import os
import sys

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def initialize():

    centerdict = []  # list of center dicts, indexed by center.id
    seshlist18 = []  # list of session dicts, age18, indexed by sesh.id
    seshlist45 = []  # list of session dicts, age45, indexed by sesh.id
    userlist18 = []  # list of user lists, age18
    userlist45 = []  # list of user lists, age45
    districtIDs = getDistrictIDs()
    for x in range(800):
        db_data.append([])
        seshlist18.append({})
        seshlist45.append({})
        centerdict.append({})
        userlist18.append([])
        userlist45.append([])
    with open(os.path.join(sys.path[0],'vaxslot/scripts/districts_names.txt')) as f:
        lines = f.read().splitlines()
    for x in lines:
        y = x.split(': ')
        districtname_to_id[y[1]] = int(y[0])

    centers = Center.query.all()
    for x in centers:
        centerdict[x.districtID][x.id] = x

    seshes = sesh.query.all()
    for x in seshes:
        if x.age == 18:
            seshlist18[x.districtID][x.id] = x
        else:
            seshlist45[x.districtID][x.id] = x

    users = User.query.all()
    for x in users:
        if x.age >= 45:
            userlist45[x.districtID].append(x)  # THIS WON'T RUN UNLESS USER CLASS KA PROTOTYPE IS CHANGED
        else:
            userlist45[x.districtID].append(x)

    for x in districtIDs:
        db_data[x] = [seshlist18[x], seshlist45[x], centerdict[x], userlist18[x], userlist45[x]]


def getStates():
    return requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states',headers=header ).json()


def getStateIDs():
    states = getStates()
    return [x['state_id'] for x in states['states']]


def getDistricts(stateID):
    return requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + str(stateID),headers=header).json()['districts']


def getDistrictIDs(start=0,finish=757):          #start inclusive, finish excluded, 0 indexed
    with open(os.path.join(sys.path[0],'vaxslot/scripts/districts.txt'), "r") as f:
        lines = f.read().splitlines()
    lines = [int(x) for x in lines]
    lines = lines[start:finish]
    return lines

#this returns a dict indexed by state_names and for each state name, there's a list of 2 tuples.
# {'Andaman and Nicobar Islands': [['Nicobar', 3], ['North and Middle Andaman', 1], ['South Andaman', 2]], 'Andhra Pradesh': [['Anantapur', 9],...]...}
# def stateToDistrict():

#     # states = getStates()['states']
#     # dic = {}
#     # for x in states:
#     #     districts_as_dicts = getDistricts(x['state_id'])
#     #     districts_as_lists =  []
#     #     for y in districts_as_dicts:
#     #         districts_as_lists.append([y['district_name'],y['district_id']])
#     #     dic[x['state_name']]=districts_as_lists
#     # print(dic)
#     # with open('district_data.json', 'w') as f:
#     #     json.dump(dic, f)
#     # return dic
#     with open('district_data.json') as f:
#         dic = json.load(f)
#         # print(dic)
#         return dic

# stateToDistrict()