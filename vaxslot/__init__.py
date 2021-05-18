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


port = 465  # For SSL
sender_email = "vaxslot@gmail.com"
password = 'vozpoh-pocjUb-2kowwa'

# Create a secure SSL context
context = ssl.create_default_context()
try:
    server  = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
except:
    server = smtplib.SMTP_SSL("74.125.200.109", port, context=context)
server.login(sender_email, password)

from vaxslot.scripts import routes