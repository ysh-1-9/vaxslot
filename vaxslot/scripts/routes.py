from flask import render_template, session, request, url_for, flash, redirect
from vaxslot import app
from vaxslot.scripts.forms import Registration
from vaxslot.scripts.models import Data

from vaxslot.scripts.common import cache

cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': 'misc/tmp'})
cache.set("flag", 0)


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
