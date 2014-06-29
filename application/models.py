# coding: utf-8
from datetime import datetime
from database import db
from flask_login import UserMixin

TABLE_PREFIX = 'rso'


class UserConfig(db.Model):
    __tablename__ = 'user_config'

    id = db.Column(db.Integer, primary_key=True)
    versnew = db.Column(db.Integer, nullable=False)
    versold = db.Column(db.Integer, nullable=False)
    comp = db.Column(db.Unicode(32), nullable=False)
    user = db.Column(db.Unicode(32), nullable=False)
    userinout = db.Column(db.SmallInteger, nullable=False)
    numorgnew = db.Column(db.Integer)  #TODO: Organisation.id?
    dostup = db.Column(db.SmallInteger, nullable=False, server_default="0")
    idTimeStamp = db.Column(db.DateTime, nullable=False, default=datetime.now())


class WorkTypeCategory(db.Model):
    __tablename__ = 'work_type_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Unicode(32), nullable=False)
    name = db.Column(db.Unicode(32), nullable=True)


class WorkType(db.Model):
    __tablename__ = 'work_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Unicode(32), nullable=False)
    name = db.Column(db.Unicode(256), nullable=False)
    ro_id = db.Column(db.Integer, db.ForeignKey('ro.id'), index=True)

    __table_args__ = (db.UniqueConstraint('code', 'ro_id', name='uix_ro_code'), )
    ro = db.relationship('RO')


class WorkTypeRelations(db.Model):
    __tablename__ = 'work_type_relations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('work_type_category.id'), index=True)
    work_type_id = db.Column(db.Integer, db.ForeignKey('work_type.id'), index=True)


class ROStatus(db.Model):
    __tablename__ = 'ro_status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(32), unique=True)


class ROAll(db.Model):
    __tablename__ = 'ro_all'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(32), unique=True)


class RO(db.Model):
    __tablename__ = 'ro'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(32), unique=True, index=True)
    short_name = db.Column(db.Unicode(4), unique=True, index=True)


class Opf(db.Model):
    __tablename__ = 'opf'

    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.Unicode(24), nullable=False)
    long_name = db.Column(db.Unicode(128), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())


class CheckPeriod(db.Model):
    __tablename__ = 'check_period'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(32))


class OrganisationChecking(db.Model):
    __tablename__ = 'organisation_checking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    check_period_id = db.Column(db.Integer, db.ForeignKey('check_period.id'), nullable=False)
    checking_date = db.Column(db.Date, nullable=False)
    checking_result = db.Column(db.Unicode(256), nullable=False)
    is_archive = db.Column(db.SmallInteger, server_default="0")

    db.UniqueConstraint('organisation_id', 'check_period_id', 'is_archive')

    period = db.relationship('CheckPeriod')


class Organisation(db.Model):
    __tablename__ = 'organisation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ro_id = db.Column(db.Integer, db.ForeignKey(RO.id), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(ROStatus.id), index=True, nullable=True)
    opf_id = db.Column(db.Integer, db.ForeignKey(Opf.id), index=True)
    name = db.Column(db.Unicode(256), nullable=False)
    inn = db.Column(db.Unicode(32), nullable=False)
    ogrn = db.Column(db.Unicode(32), nullable=False)
    address_place = db.Column(db.UnicodeText)
    address_arenda = db.Column(db.UnicodeText)
    address_post = db.Column(db.UnicodeText)
    gendir = db.Column(db.Unicode(128), nullable=False)
    contact = db.Column(db.UnicodeText, nullable=False)
    addr_site_post = db.Column(db.UnicodeText)
    site = db.Column(db.Unicode(128))
    email = db.Column(db.Unicode(128))
    posrednik_id = db.Column(db.Integer, db.ForeignKey(OrganisationPosrednik.id), nullable=True, index=True)
    # posrednik2 = db.Column(db.UnicodeText, nullable=True)  # TODO: объеденить с posrednik и вынести в отд. табл.
    prepare_case_id = db.Column(db.Integer, db.ForeignKey(OrganisationPrepareCase), nullable=True, index=True)
    dolg_doc = db.Column(db.UnicodeText, nullable=True)
    specialist = db.Column(db.Unicode(256), nullable=True)
    narush = db.Column(db.UnicodeText, nullable=True)
    sved_dop_iskl_partn = db.Column(db.UnicodeText, nullable=True)
    iskl_chl_partn = db.Column(db.Date)
    osn_izm_chl_partn = db.Column(db.UnicodeText, nullable=False)
    sved_discipl_vozd = db.Column(db.UnicodeText, nullable=True)
    comments = db.Column(db.UnicodeText, nullable=True)
    osob_otmetki = db.Column(db.UnicodeText, nullable=True)
    jalobi = db.Column(db.Date)
    vid_zayavlen = db.Column(db.Unicode(256), nullable=True)
    date_zayavlen = db.Column(db.Date)
    vid_rab_besop = db.Column(db.UnicodeText, nullable=True)
    vid_rab_iskl_opasn = db.Column(db.UnicodeText, nullable=True)
    vid_rab_vkl_opasn_iskl_atom = db.Column(db.UnicodeText, nullable=True)
    vid_rab_vkl_opasn_vkl_atom = db.Column(db.UnicodeText, nullable=True)
    pered_sp = db.Column(db.Date)
    svid_begin_date = db.Column(db.Date)
    # vid_posl_svid_date = db.Column(db.Date)
    prekr_svid_date = db.Column(db.Date)
    zadolj_vznos = db.Column(db.UnicodeText, nullable=True)
    delo_org_arch = db.Column(db.UnicodeText, nullable=True)
    delo_org_vidano = db.Column(db.UnicodeText, nullable=True)
    vopros = db.Column(db.UnicodeText, nullable=True)
    deleted = db.Column(db.SmallInteger, server_default="0")
    resh_desc_kom = db.Column(db.Text, nullable=True)
    edit = db.Column(db.Unicode(64), nullable=True)  # TODO: to History OR FK to user_config??
    ro_all_id = db.Column(db.Integer, db.ForeignKey(ROAll.id))
    # fronametro = db.Column(db.Text) # см. ro_status.name
    # froshortnametro = db.Column(db.Text) # см. ro_status.short_name
    svid_date = db.Column(db.Date)
    idTimeStamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

    moderniz = db.Column(db.UnicodeText, nullable=True)

    ro = db.relationship(RO)
    opf = db.relationship(Opf)
    ro_status = db.relationship(ROStatus)
    posrednik = db.relationship(OrganisationPosrednik)
    prepare_case = db.relationship(OrganisationPrepareCase)
    check_period = db.relationship(
        'OrganisationChecking',
        primaryjoin='and_(Organisation.id==OrganisationChecking.organisation_id, '
                    'OrganisationChecking.is_archive==0)')
    check_period_archive = db.relationship(
        'OrganisationChecking',
        primaryjoin='and_(Organisation.id==OrganisationChecking.organisation_id, '
                    'OrganisationChecking.is_archive==1)')

    ro_all = db.relationship(ROAll)


class OrganisationPosrednik(db.Model):
    __tablename__ = 'organisation_posrednik'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))


class OrganisationPrepareCase(db.Model):
    __tablename__ = 'organisation_prepare_case'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(256))


class OrganisationSvidDopuska(db.Model):
    __tablename__ = 'organisation_svid_dopuska'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id), index=True)
    name = db.Column(db.Unicode(128))
    is_archive = db.Column(db.Boolean, default=False)

    organisation = db.relationship(Organisation, backref=db.backref('svid_dopuska'), lazy=False)


class KSV(db.Column):
    __tablename__ = 'organisation_ksv'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id), index=True)
    uved = db.Column(db.UnicodeText)
    otmetka_vruch = db.Column(db.UnicodeText)

    comment = db.Column(db.UnicodeText, nullable=False)
    control = db.Column(db.Date)
    status = db.Column(db.UnicodeText, nullable=False)
    narush = db.Column(db.UnicodeText, nullable=False)
    result_proverki = db.Column(db.UnicodeText, nullable=False)
    peredacha_dk = db.Column(db.Date)
    recommendation_dk = db.Column(db.UnicodeText, nullable=False)

    organisation = db.relationship(Organisation, backref=db.backref('ksv'))


class KK(db.Column):
    __tablename__ = 'organisation_kk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id), index=True)
    date_uved = db.Column(db.Date)
    uved = db.Column(db.UnicodeText)
    date_otprav = db.Column(db.Date)
    akt = db.Column(db.UnicodeText)
    otm_vruch = db.Column(db.UnicodeText)
    status = db.Column(db.UnicodeText)
    bo = db.Column(db.Text, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    control = db.Column(db.Date)
    recommendation_dk = db.Column(db.Text, nullable=True)

    organisation = db.relationship(Organisation, backref=db.backref('kk'))


class DK(db.Column):
    __tablename__ = 'organisation_dk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id), index=True)
    date_pered = db.Column(db.Date)
    delo_org = db.Column(db.Unicode)
    date_zased = db.Column(db.Date)
    is_archive = db.Column(db.SmallInteger, server_default="0")
    uved = db.Column(db.Unicode)
    otm_vruch = db.Column(db.Unicode)
    protocol = db.Column(db.Unicode)
    otm_vruch2 = db.Column(db.Unicode)
    status = db.Column(db.Unicode, nullable=True)
    recommendation_dk = db.Column(db.UnicodeText, nullable=True)
    comment = db.Column(db.UnicodeText, nullable=True)
    control = db.Column(db.Date)

    organisation = db.relationship(Organisation, backref=db.backref('dk'))


class PD(db.Column):
    __tablename__ = 'organisation_pd'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id), index=True)
    akt = db.Column(db.UnicodeText, nullable=True)
    comment = db.Column(db.UnicodeText, nullable=True)
    control = db.Column(db.Date)
    status = db.Column(db.UnicodeText, nullable=True)
    narush = db.Column(db.UnicodeText, nullable=True)
    result_proverki = db.Column(db.UnicodeText, nullable=True)
    peredacha_dk = db.Column(db.Date)
    recommendation_dk = db.Column(db.UnicodeText, nullable=True)

    organisation = db.relationship(Organisation, backref=db.backref('pd'))


####################

class Roles(db.Model):
    __tablename__ = '%s_roles' % TABLE_PREFIX

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.Unicode(80), unique=True)
    description = db.Column(db.Unicode(255))


class Users(db.Model, UserMixin):
    __tablename__ = '%s_users' % TABLE_PREFIX

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship(Roles,
                            secondary='%s_users_roles' % TABLE_PREFIX,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, login, password):
        self.login = login
        self.password = password


class UsersRoles(db.Model):
    __tablename__ = '%s_users_roles' % TABLE_PREFIX

    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(Roles.id), primary_key=True)
