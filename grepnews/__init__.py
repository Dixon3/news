from flask import Flask

import os
from flask.ext.login import LoginManager
import users
#from config import basedir

grepnews = Flask(__name__)

grepnews.config.from_object('config')
lm = LoginManager()
lm.init_app(grepnews)
lm.login_view = 'login'

@lm.user_loader
def load_user(userid):
    print userid
    user=users.User(userid,'')
    return user


from grepnews import views