# -*- coding: utf-8 -*-

from application.app import db, app
with app.app_context():
    db.create_all()