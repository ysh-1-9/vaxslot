import sys
sys.path.insert(0, 'scripts')

from flask import Flask, render_template, session, request, url_for, flash, redirect
from forms import Registration
from flask_sqlalchemy import SQLAlchemy

from common import cache
from get_slots import get_slot

app = Flask(__name__)

cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': 'misc/tmp'})
cache.set("flag", 0)

app.config['SECRET_KEY'] = 'odsfb45hewrk37grawibn3gradlskj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
db = SQLAlchemy(app)

DEBUG = True
PORT = 8080


class Data(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), primary_key=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=True)

    def _repr_(self) -> str:
        return f"E-Mail - {self.email} Age - {self.age} State - {self.district}"


@app.route('/main.html', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    
    form = Registration()
    flag = cache.get("flag")
    if form.validate_on_submit():
        st = form.state.data
        dist = form.district.data
        age = form.age.data

        print(st, dist, age)
        if(get_slot(st, dist, age)[0]):
            flash("You have been succesfully registered.\nSlots are available now.\nVisit the CoWin Portal to register.", 'success')
        else:
            flash("You have been succesfully registered.")
        if(flag):
            flashes = session.pop("_flashes", None)
            flag = 0
        else:
            flag = 1
    cache.set("flag", flag)

    data = Data()
    if(request.method=='POST'):
        data.email = form.email.data
        data.state = form.state.data
        data.district = form.district.data
        data.number = form.number.data
        data.age = form.age.data
        db.session.add(data)
        db.session.commit()
        print("Details have been added.")
    
    return render_template('main.html', form=form, flag=flag)

if __name__ == "__main__":
    app.run(debug = DEBUG, port = PORT)

