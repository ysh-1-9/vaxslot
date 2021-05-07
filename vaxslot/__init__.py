from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'odsfb45hewrk37grawibn3gradlskj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
db = SQLAlchemy(app)

districtname_to_id={}
db_data = []

def initialize():
    from vaxslot.scripts.get_slots import getDistrictIDs
    from vaxslot.scripts.models import sesh,Center
    centerdict = []  # list of center dicts, indexed by center.id
    seshlist18 = []  # list of session dicts, age18, indexed by sesh.id
    seshlist45 = []  # list of session dicts, age45, indexed by sesh.id
    districtIDs = getDistrictIDs()
    for x in range(800):
        db_data.append([])
        seshlist18.append({})
        seshlist45.append({})
        centerdict.append({})
    with open('districts_names.txt') as f:
        lines = f.read().splitlines()
    for x in lines:
        y = x.split(': ')
        districtname_to_id[y[1]]=int(y[0])

    centers = Center.query.all()
    for x in centers:
        centerdict[x.districtID][x.id] = x

    seshes = sesh.query.all()
    for x in seshes:
        if x.age==18:
            seshlist18[x.districtID][x.id] = x
        else:
            seshlist45[x.districtID][x.id] = x

    for x in districtIDs:
        db_data[x] = [seshlist18[x],seshlist45[x],centerdict[x]]


from vaxslot.scripts import routes