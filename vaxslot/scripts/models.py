from vaxslot import db, districtname_to_id


class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    __table_args__ = {'extend_existing': True}
    email = db.Column(db.String(200), primary_key=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    district = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=True)

    def _repr_(self) -> str:
        return f"E-Mail - {self.email} Age - {self.age} State - {self.district}"


class Center(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(500))
    districtID = db.Column(db.Integer)
    def __init__(self, center,**kwargs):
        super(Center,self).__init__(**kwargs)
        self.id = center['center_id']
        self.name = center['name'] + ' ' + center.get('name_l','')
        self.address = center.get('address','') + center.get('address_l','')+ ', ' + center.get('block_name','') + center.get('block_name_l','')+ ', ' + center.get('district_name','') + center.get('district_name_l','')+ ', ' + center.get('state_name','') + center.get('state_name_l','')+ ' - ' + str(center.get('pincode',''))
        self.districtID = districtname_to_id[center['district_name']]

class sesh(db.Model):
    __table_args__ = {'extend_existing': True}
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
        super(sesh,self).__init__(**kwargs)
        self.id = session['session_id']
        self.date = session['date']
        self.currCap = session['available_capacity']
        self.age = session['min_age_limit']
        self.vaccine = session['vaccine']
        self.districtID = districtID
        self.centerID = centerID
        self.prevCap = 0
