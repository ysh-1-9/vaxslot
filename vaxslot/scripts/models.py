from vaxslot import db

class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), primary_key=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=True)

    def _repr_(self) -> str:
        return f"E-Mail - {self.email} Age - {self.age} State - {self.district}"


class Center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(500))

    def __init__(self, center,**kwargs):
        super(Center,self).__init__(**kwargs)
        self.id = center['center_id']
        self.name = center['name'] + ' ' + center['name_l']
        self.address = center['address'] + center['address_l'] + center['block_name'] + center['block_name_l'] + center[
            'district_name'] + center['district_name_l'] + center['state_name'] + center['state_name_l'] + center[
                           'pincode']

class sesh(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    districtID = db.Column(db.Integer)
    age = db.Column(db.Integer)             #bool karke can save space until 18- starts
    centerID = db.Column(db.Integer)
    prevCap = db.Column(db.Integer)
    currCap = db.Column(db.Integer)
    date = db.Column(db.String(20))
    vaccine = db.Column(db.String(20))      #bool karke can save space until india gets richer / Bill Gates gets cancelled
    # abhi not saving slot time details, can add later.

    def __init__(self,session, districtID, centerID,**kwargs):
        super(session,self).__init__(**kwargs)
        self.id = session['session_id']
        self.date = session['date']
        self.currCap = session['available_capacity']
        self.age = session['min_age_limit']
        self.vaccine = session['vaccine']
        self.districtID = districtID
        self.centerID = centerID
        self.prevCap = 0
