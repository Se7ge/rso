# -*- encoding: utf-8 -*-
from flask import render_template, abort, request, redirect, url_for, flash, session, current_app
from flask.views import MethodView

from jinja2 import TemplateNotFound
from wtforms import TextField, PasswordField, IntegerField
from flask_wtf import Form
from wtforms.validators import Required
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed
from flask.ext.principal import identity_loaded, Permission, RoleNeed, UserNeed, ActionNeed
from flask.ext.login import login_user, logout_user, login_required, current_user

from application.app import app, db, login_manager
from application.models import Config, OldExcel
from application.context_processors import general_menu
from .lib.utils import public_endpoint
from lib.user import UserAuth
from forms import LoginForm


ROWS_PER_PAGE = 20

login_manager.login_view = 'login'


@app.before_request
def check_valid_login():
    login_valid = current_user.is_authenticated()

    if (request.endpoint and
            'static' not in request.endpoint and
            not login_valid and
            not getattr(app.view_functions[request.endpoint], 'is_public', False)):
        return redirect(url_for('login', next=url_for(request.endpoint)))


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>/')
def index(page):
    organisations = OldExcel.query.filter(OldExcel.fmarkfordel == 0)
    if 'q' in request.args:
        query = request.args['q']
        organisations = organisations.filter(
            db.or_(
                OldExcel.fnamefull.like(u'%{0}%'.format(query)),
                OldExcel.fnumorg.like(u'{0}%'.format(query)),
                OldExcel.fogrn.like(u'{0}%'.format(query)),
                OldExcel.finn.like(u'{0}%'.format(query))))
    organisations = organisations.group_by(OldExcel.fnumorg).order_by(OldExcel.fnumorg)
    organisations = organisations.paginate(page, ROWS_PER_PAGE)
    return render_template('index.html', organisations=organisations)


@app.route('/edit/<int:fnum>/')
def edit(fnum):
    organisation = db.session.query(OldExcel).get(fnum)
    return render_template('edit.html', organisation=organisation)


@app.route('/login/', methods=['GET', 'POST'])
@public_endpoint
def login():
    # login form that uses Flask-WTF
    form = LoginForm()
    errors = list()
    # Validate form input
    if form.validate_on_submit():
        user = UserAuth.check_user(form.login.data.strip(), form.password.data.strip())
        if user:
            # Keep the user info in the session using Flask-Login
            login_user(user)
            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            return redirect(request.args.get('next') or url_for('index'))
        else:
            errors.append(u'Неверная пара логин/пароль')

    return render_template('user/login.html', form=form, errors=errors)


@app.route('/logout/')
def logout():
    # Remove the user information from the session
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(request.args.get('next') or '/')


@app.errorhandler(403)
def authorisation_failed(e):
    flash(u'У вас недостаточно привилегий для доступа к функционалу')
    return render_template('user/denied.html')


#########################################

@login_manager.user_loader
def load_user(user_id):
    # Return an instance of the User model
    return UserAuth.get_by_id(user_id)


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    if identity.id:
        identity.user = load_user(identity.id)