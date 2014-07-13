# -*- encoding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, current_app
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed
from flask.ext.principal import identity_loaded
from flask.ext.login import login_user, logout_user, current_user

from application.app import app, db, login_manager
from application.models.models import Organisation, Opf, RO, ROStatus, OrganisationPosrednik
from application.lib.utils import public_endpoint
from lib.user import UserAuth
from forms import LoginForm, OrganisationForm


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
    organisations = Organisation.query.filter(Organisation.deleted == False)
    if 'q' in request.args:
        query = request.args['q']
        filter_or = []
        try:
            int_query = int(query)
        except ValueError:
            pass
        else:
            if int_query > 0:
                filter_or.append(Organisation.id == int_query)
        filter_or.append(Organisation.name.like(u'%{0}%'.format(query)))
        filter_or.append(Organisation.ogrn.like(u'%{0}%'.format(query)))
        filter_or.append(Organisation.inn.like(u'%{0}%'.format(query)))
        organisations = organisations.filter(db.or_(*filter_or))
    ro_filter = request.args.getlist("ro")
    if ro_filter:
        organisations = organisations.filter(Organisation.ro_id.in_(ro_filter))
    if 'ro_status' in request.args and request.args['ro_status']:
        organisations = organisations.filter(Organisation.status_id == request.args['ro_status'])
    if 'opf' in request.args and request.args['opf']:
        organisations = organisations.filter(Organisation.opf_id == request.args['opf'])
    if 'posrednik' in request.args and request.args['posrednik']:
        organisations = organisations.filter(db.or_(Organisation.posrednik_id == request.args['posrednik'],
                                                    Organisation.posrednik2_id == request.args['posrednik']))
    organisations = organisations.order_by(Organisation.id)
    organisations = organisations.paginate(page, ROWS_PER_PAGE)
    return render_template('index.html',
                           organisations=organisations,
                           opf=db.session.query(Opf).all(),
                           ro=db.session.query(RO).all(),
                           ro_status=db.session.query(ROStatus).all(),
                           posrednik=db.session.query(OrganisationPosrednik).all())


@app.route('/edit/<int:id>/')
def edit(id):
    organisation = db.session.query(Organisation).get(id)

    form_organisation = OrganisationForm(request.form, organisation)
    form_organisation.populate_obj(organisation)

    form_organisation.opf.choices = [(item.id, item.name) for item in Opf.query.all()]
    form_organisation.opf.data = organisation.opf_id

    return render_template('edit.html', organisation=organisation, form=form_organisation)


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