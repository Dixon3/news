# -*- coding: utf-8 -*-


from flask.ext.wtf import Form
from wtforms import TextField, PasswordField , BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    username= TextField('user', validators = [Required()])
    password= PasswordField('pass', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)