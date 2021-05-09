from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'odsfb45hewrk37grawibn3gradlskj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
db = SQLAlchemy(app)

districtname_to_id={}
db_data = []
user_district={}

dist_start=0
dist_finish = 346            #max 757, min 1, 346 at 80%

from vaxslot.scripts import routes