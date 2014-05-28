# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
PROJECT_NAME = 'rso'

# DB connecting params
DB_DRIVER = 'mysql'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'db_user'
DB_PASSWORD = 'db_password'
DB_NAME = 'db_name'
DB_CONNECT_OPTIONS = ''

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

SYSTEM_USER = 'rso'

WTF_CSRF_ENABLED = True
SECRET_KEY = ''

BLUEPRINTS_DIR = 'blueprints'

BABEL_DEFAULT_LOCALE = 'ru_RU'

BEAKER_SESSION = {'session.type': 'file',
                  'session.data_dir': '/tmp/session/data',
                  'session.lock_dir': '/tmp/session/lock'}

TIME_ZONE = 'Europe/Moscow'


SEARCHD_CONNECTION = {
    'host': '127.0.0.1',
    'port': 9306,
}


try:
    from config_local import *
except ImportError:
    # no local config found
    pass

SQLALCHEMY_DATABASE_URI = '{0}://{1}:{2}@{3}:{4}/{5}{6}'.format(DB_DRIVER,
                                                       DB_USER,
                                                       DB_PASSWORD,
                                                       DB_HOST,
                                                       DB_PORT,
                                                       DB_NAME,
                                                       DB_CONNECT_OPTIONS)
