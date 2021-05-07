from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email

# give the user a list of districts to choose from

state_choices = [( 'andaman and nicobar islands', 'Andaman and Nicobar Islands'), 
                ( 'andhra pradesh', 'Andhra Pradesh'), 
                ( 'arunachal pradesh', 'Arunachal Pradesh'), 
                ( 'assam', 'Assam'), 
                ( 'bihar', 'Bihar'), 
                ( 'chandigarh', 'Chandigarh'), 
                ( 'chattisgarh', 'Chhattisgarh'), 
                ( 'dadra and nagar haveli', 'Dadra and Nagar Haveli'), 
                ( 'daman and diu', 'Daman and Diu'), 
                ( 'delhi', 'Delhi'), 
                ( 'goa', 'Goa'), 
                ( 'gujarat', 'Gujarat'), 
                ( 'haryana', 'Haryana'), 
                ( 'himachal', 'Himachal Pradesh'), 
                ( 'jammu and kashmir', 'Jammu and Kashmir'), 
                ( 'jharkhand', 'Jharkhand'), 
                ( 'karnataka', 'Karnataka'), 
                ( 'kerala', 'Kerala'), 
                ( 'ladakh', 'Ladakh'), 
                ( 'lakshwadeep', 'Lakshadweep'), 
                ( 'madhya pradhesh', 'Madhya Pradesh'), 
                ( 'maharashtra', 'Maharashtra'), 
                ( 'manipur', 'Manipur'), 
                ( 'meghalaya', 'Meghalaya'), 
                ( 'mizoram', 'Mizoram'), 
                ( 'nagaland', 'Nagaland'), 
                ( 'odisha', 'Odisha'), 
                ( 'puducherry', 'Puducherry'), 
                ( 'punjab', 'Punjab'), 
                ( 'rajasthan', 'Rajasthan'), 
                ( 'sikkim', 'Sikkim'), 
                ( 'tamil nadu', 'Tamil Nadu'), 
                ( 'telangana', 'Telangana'), 
                ( 'tripura', 'Tripura'), 
                ( 'uttar pradesh', 'Uttar Pradesh'), 
                ( 'uttarakhand', 'Uttarakhand'), 
                ( 'west bengal', 'West Bengal')]


class Registration(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()], render_kw={"placeholder":"E-Mail"})
    state = SelectField('state', choices=state_choices, validators=[DataRequired()], render_kw={"placeholder":"State"})
    district = SelectField('district', choices=[], validators=[DataRequired()], render_kw={"placeholder":"District"})
    age = IntegerField('age', validators=[DataRequired()], render_kw={"placeholder":"Age"})
    number = StringField('number', validators=[DataRequired(), Length(min=10, max=13)], render_kw={"placeholder":"Phone No."})
    submit = SubmitField('Submit')