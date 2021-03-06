# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify
from flask.ext.principal import Principal
from flask.ext.babel import Babel
from flask.ext.login import LoginManager, current_user
from flask_beaker import BeakerSession
import pytz
from database import db
from autoload import load_blueprints
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
from models.models import *
from models.history import *

babel = Babel(app)


login_manager = LoginManager(app)
Principal(app)

BeakerSession(app)


@babel.timezoneselector
def get_timezone():
    return pytz.timezone(app.config['TIME_ZONE'])

#Register blueprints
blueprints_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', app.config['BLUEPRINTS_DIR']))
load_blueprints(app, apps_path=blueprints_path)

# Import all views
from views import *