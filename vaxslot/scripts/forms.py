from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email

# give the user a list of districts to choose from
from vaxslot.scripts.db_imports_exports import stateToDistrict

state_choices = [(x,x) for x in stateToDistrict().keys()]


class Registration(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder":"E-Mail"})
    state = SelectField('State', choices=state_choices, validators=[DataRequired()], render_kw={"placeholder":"State"})
    district = SelectField('District', choices=[], validators=[DataRequired()], render_kw={"placeholder":"District"})
    age = StringField('Age', validators=[DataRequired()], render_kw={"placeholder":"Age"})
    number = StringField('Number', validators=[DataRequired(), Length(min=10, max=13)], render_kw={"placeholder":"Phone No."})
    submit = SubmitField('Submit')