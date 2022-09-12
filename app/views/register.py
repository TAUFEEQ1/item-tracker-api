from flask_wtf import FlaskForm
from wtforms import StringField,SelectField
from wtforms.validators import DataRequired,Length
from flask import request
from flask import jsonify
from app import db
from hashlib import sha256

from app.models import Depts,User

class RegisterForm(FlaskForm):
    class Meta:
        csrf = False
    first_name = StringField(validators=[DataRequired(),Length(min=3)])
    last_name = StringField(validators=[DataRequired(),Length(min=3)])
    phone_no = StringField(validators=[DataRequired(),Length(min=10,max=10)])
    username = StringField(validators=[DataRequired(),Length(min=3)])
    password = StringField(validators=[DataRequired(),Length(min=8)])
    dept = SelectField(choices=[Depts.LEVEL_1,Depts.LEVEL_2,Depts.LEVEL_3])

def register():
    form  = RegisterForm(data=request.form)
    if not form.validate():
        return jsonify(form.errors),422
    
    user = User()
    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    user.phone_no = form.phone_no.data
    user.username = form.username.data
    user.password = sha256(form.password.data.encode()).hexdigest()
    user.dept = form.dept.data
    
    db.session.add(user)
    db.session.commit()

    return "user registration successful",201
