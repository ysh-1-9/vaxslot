from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email

# give the user a list of districts to choose from

state_choices = [( 'Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), 
                ( 'Andhra Pradesh', 'Andhra Pradesh'), 
                ( 'Arunachal Pradesh', 'Arunachal Pradesh'), 
                ( 'Assam', 'Assam'), 
                ( 'Bihar', 'Bihar'), 
                ( 'Chandigarh', 'Chandigarh'), 
                ( 'Chattisgarh', 'Chhattisgarh'), 
                ( 'Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'), 
                ( 'Daman and Diu', 'Daman and Diu'), 
                ( 'Delhi', 'Delhi'), 
                ( 'Goa', 'Goa'), 
                ( 'Gujarat', 'Gujarat'), 
                ( 'Haryana', 'Haryana'), 
                ( 'Himachal Pradesh', 'Himachal Pradesh'), 
                ( 'Jammu and kashmir', 'Jammu and Kashmir'), 
                ( 'Jharkhand', 'Jharkhand'), 
                ( 'Karnataka', 'Karnataka'), 
                ( 'Kerala', 'Kerala'), 
                ( 'Ladakh', 'Ladakh'), 
                ( 'Lakshwadeep', 'Lakshadweep'), 
                ( 'Madhya Pradhesh', 'Madhya Pradesh'), 
                ( 'Maharashtra', 'Maharashtra'), 
                ( 'Manipur', 'Manipur'), 
                ( 'Meghalaya', 'Meghalaya'), 
                ( 'Mizoram', 'Mizoram'), 
                ( 'Nagaland', 'Nagaland'), 
                ( 'Odisha', 'Odisha'), 
                ( 'Puducherry', 'Puducherry'), 
                ( 'Punjab', 'Punjab'), 
                ( 'Rajasthan', 'Rajasthan'), 
                ( 'Sikkim', 'Sikkim'), 
                ( 'Tamil Nadu', 'Tamil Nadu'), 
                ( 'Telangana', 'Telangana'), 
                ( 'Tripura', 'Tripura'), 
                ( 'Uttar Pradesh', 'Uttar Pradesh'), 
                ( 'Uttarakhand', 'Uttarakhand'), 
                ( 'West Bengal', 'West Bengal')]


class Registration(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder":"E-Mail"})
    state = SelectField('State', choices=state_choices, validators=[DataRequired()], render_kw={"placeholder":"State"})
    district = SelectField('District', choices=[], validators=[DataRequired()], render_kw={"placeholder":"District"})
    age = StringField('Age', validators=[DataRequired()], render_kw={"placeholder":"Age"})
    number = StringField('Number', validators=[DataRequired(), Length(min=10, max=13)], render_kw={"placeholder":"Phone No."})
    submit = SubmitField('Submit')