# coding: utf-8
from datetime import datetime
from application.database import db
from models import RO, ROStatus, Opf, Organisation, OrganisationPosrednik, OrganisationPrepareCase, ROAll

TABLE_PREFIX = 'rso'


class OrganisationCheckingHistory(db.Model):
    __tablename__ = 'organisation_checking_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_history_id = db.Column(db.Integer, db.ForeignKey('organisation_history.id', ondelete='CASCADE'), nullable=False)
    check_period_id = db.Column(db.Integer, db.ForeignKey('check_period.id', ondelete='CASCADE'), nullable=False)
    checking_date = db.Column(db.Date, nullable=False)
    checking_result = db.Column(db.Unicode(256), nullable=True)
    is_archive = db.Column(db.Boolean, default=False)

    db.UniqueConstraint('organisation_history_id', 'check_period_id', 'is_archive')

    period = db.relationship('CheckPeriod')


class OrganisationHistory(db.Model):
    __tablename__ = 'organisation_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id), nullable=False)
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
    posrednik2_id = db.Column(db.Integer, db.ForeignKey(OrganisationPosrednik.id), nullable=True, index=True)
    # posrednik2 = db.Column(db.UnicodeText, nullable=True)  # TODO: объеденить с posrednik и вынести в отд. табл.
    prepare_case_id = db.Column(db.Integer, db.ForeignKey(OrganisationPrepareCase.id), nullable=True, index=True)
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
    pered_sp = db.Column(db.Date)
    svid_begin_date = db.Column(db.Date)
    prekr_svid_date = db.Column(db.Date)
    zadolj_vznos = db.Column(db.UnicodeText, nullable=True)
    delo_org_arch = db.Column(db.UnicodeText, nullable=True)
    delo_org_vidano = db.Column(db.UnicodeText, nullable=True)
    vopros = db.Column(db.UnicodeText, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    resh_desc_kom = db.Column(db.UnicodeText, nullable=True)
    edit = db.Column(db.Unicode(64), nullable=True)  # TODO: to History OR FK to user_config??
    ro_all_id = db.Column(db.Integer, db.ForeignKey(ROAll.id))
    svid_date = db.Column(db.Date)
    idTimeStamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

    moderniz = db.Column(db.UnicodeText, nullable=True)

    organisation = db.relationship(Organisation)
    ro = db.relationship(RO)
    opf = db.relationship(Opf)
    ro_status = db.relationship(ROStatus)
    posrednik = db.relationship(OrganisationPosrednik, foreign_keys=[posrednik_id])
    posrednik2 = db.relationship(OrganisationPosrednik, foreign_keys=[posrednik2_id])
    prepare_case = db.relationship(OrganisationPrepareCase)
    check_period = db.relationship(
        'OrganisationCheckingHistory',
        primaryjoin='and_(OrganisationHistory.id==OrganisationCheckingHistory.organisation_history_id, '
                    'OrganisationCheckingHistory.is_archive==0)')
    check_period_archive = db.relationship(
        'OrganisationCheckingHistory',
        primaryjoin='and_(OrganisationHistory.id==OrganisationCheckingHistory.organisation_history_id, '
                    'OrganisationCheckingHistory.is_archive==1)')

    ro_all = db.relationship(ROAll)


class OrganisationWorkTypeHistory(db.Model):
    __tablename__ = 'organisation_work_type_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_history_id = db.Column(db.Integer, db.ForeignKey(OrganisationHistory.id, ondelete='CASCADE'), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('work_type_category.id'), index=True)
    work_type_id = db.Column(db.Integer, db.ForeignKey('work_type.id'), index=True)

    organisation_history = db.relationship(OrganisationHistory, backref=db.backref('work_types'), lazy=False)

    organisation_iskl_opasn = db.relationship(
        OrganisationHistory,
        primaryjoin="and_(OrganisationWorkTypeHistory.organisation_history_id==OrganisationHistory.id, "
                    "OrganisationWorkTypeHistory.category_id==1)",
        backref=db.backref('work_types_iskl_opasn'),
        innerjoin=True)

    organisation_vkl_opasn_iskl_atom = db.relationship(
        OrganisationHistory,
        primaryjoin="and_(OrganisationWorkTypeHistory.organisation_history_id==OrganisationHistory.id, "
                    "OrganisationWorkTypeHistory.category_id==2)",
        backref=db.backref('work_types_vkl_opasn_iskl_atom'),
        innerjoin=True)

    organisation_vkl_opasn_vkl_atom = db.relationship(
        OrganisationHistory,
        primaryjoin="and_(OrganisationWorkTypeHistory.organisation_history_id==OrganisationHistory.id, "
                    "OrganisationWorkTypeHistory.category_id==3)",
        backref=db.backref('work_types_vkl_opasn_vkl_atom'),
        innerjoin=True)


class OrganisationSvidDopuskaHistory(db.Model):
    __tablename__ = 'organisation_svid_dopuska_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_history_id = db.Column(db.Integer, db.ForeignKey(OrganisationHistory.id, ondelete='CASCADE'), index=True)
    name = db.Column(db.Unicode(128))
    is_archive = db.Column(db.Boolean, default=False)

    organisation_history = db.relationship(OrganisationHistory, backref=db.backref('svid_dopuska'), lazy=False)


class KSVHistory(db.Model):
    __tablename__ = 'organisation_ksv_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_history_id = db.Column(db.Integer, db.ForeignKey(OrganisationHistory.id, ondelete='CASCADE'), index=True)
    uved = db.Column(db.UnicodeText)
    otmetka_vruch = db.Column(db.UnicodeText)

    comment = db.Column(db.UnicodeText, nullable=False)
    control = db.Column(db.Date)
    status = db.Column(db.UnicodeText, nullable=False)
    narush = db.Column(db.UnicodeText, nullable=False)
    result_proverki = db.Column(db.UnicodeText, nullable=False)
    peredacha_dk = db.Column(db.Date)
    recommendation_dk = db.Column(db.UnicodeText, nullable=False)

    organisation = db.relationship(OrganisationHistory, backref=db.backref('ksv'))


class KKHistory(db.Model):
    __tablename__ = 'organisation_kk_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_history_id = db.Column(db.Integer, db.ForeignKey(OrganisationHistory.id, ondelete='CASCADE'), index=True)
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

    organisation = db.relationship(OrganisationHistory, backref=db.backref('kk'))


class DKHistory(db.Model):
    __tablename__ = 'organisation_dk_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_history_id = db.Column(db.Integer, db.ForeignKey(OrganisationHistory.id, ondelete='CASCADE'), index=True)
    date_pered = db.Column(db.Date)
    delo_org = db.Column(db.Unicode(64))
    date_zased = db.Column(db.Date)
    date_zased_arch = db.Column(db.UnicodeText)
    is_archive = db.Column(db.SmallInteger, server_default="0")
    uved = db.Column(db.UnicodeText)
    otm_vruch = db.Column(db.UnicodeText)
    protocol = db.Column(db.UnicodeText)
    otm_vruch2 = db.Column(db.UnicodeText)
    status = db.Column(db.Unicode(64), nullable=True)
    recommendation_dk = db.Column(db.UnicodeText, nullable=True)
    comment = db.Column(db.UnicodeText, nullable=True)
    control = db.Column(db.Date)

    organisation = db.relationship(OrganisationHistory, backref=db.backref('dk'))


class PDHistory(db.Model):
    __tablename__ = 'organisation_pd_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_history_id = db.Column(db.Integer, db.ForeignKey(OrganisationHistory.id, ondelete='CASCADE'), index=True)
    akt = db.Column(db.UnicodeText, nullable=True)
    comment = db.Column(db.UnicodeText, nullable=True)
    control = db.Column(db.Date)
    status = db.Column(db.UnicodeText, nullable=True)
    narush = db.Column(db.UnicodeText, nullable=True)
    result_proverki = db.Column(db.UnicodeText, nullable=True)
    peredacha_dk = db.Column(db.Date)
    recommendation_dk = db.Column(db.UnicodeText, nullable=True)

    organisation = db.relationship(OrganisationHistory, backref=db.backref('pd'))
