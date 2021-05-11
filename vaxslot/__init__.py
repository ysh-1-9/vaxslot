import smtplib
import ssl

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rq import Queue

# from worker import conn
#
#


app = Flask(__name__)
app.config['SECRET_KEY'] = 'odsfb45hewrk37grawibn3gradlskj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
db = SQLAlchemy(app)

districtname_to_id={}
db_data = []
user_district={}

dist_start=0
dist_finish = 346            #max 757, min 1, 346 at 80%

port = 465  # For SSL
sender_email = "vaxslottest@gmail.com"
password = 'toHmip-myvgoq-tyhka2'

# Create a secure SSL context
context = ssl.create_default_context()
server  = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
server.login(sender_email, password)


from vaxslot.scripts import routes