# coding: utf-8
from database import db
from flask_login import UserMixin

TABLE_PREFIX = 'rso'


class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    versnew = db.Column(db.Integer, nullable=False)
    versold = db.Column(db.Integer, nullable=False)
    comp = db.Column(db.Unicode(32), nullable=False)
    user = db.Column(db.Unicode(32), nullable=False)
    userinout = db.Column(db.SmallInteger, nullable=False)
    numorgnew = db.Column(db.Integer)  #TODO: Organisation.id?
    dostup = db.Column(db.SmallInteger, nullable=False, server_default=u"'0'")
    idTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class ROStatus(db.Model):
    __tablename__ = 'ro_status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(32), unique=True)
    name_short = db.Column(db.Unicode(16))


class ROAll(db.Model):
    __tablename__ = 'ro_all'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(32), unique=True)


class Opf(db.Model):
    __tablename__ = 'opf'

    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.Unicode(24), nullable=False)
    long_name = db.Column(db.Unicode(128), nullable=False)
    created = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


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
    checking_result = db.Column(db.Unicode, nullable=False)
    is_archive = db.Column(db.SmallInteger, default="'0'")

    db.UniqueConstraint('organisation_id', 'check_period_id', 'is_archive')

    period = db.relationship('CheckPeriod')


class Organisation(db.Model):
    __tablename__ = 'organisation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fro = db.Column(db.Text, nullable=False)  # ?
    status_id = db.Column(db.Integer, db.ForeignKey(ROStatus.id), index=True, nullable=True)
    opf_id = db.Column(db.Integer, db.ForeignKey(Opf.id), index=True)
    name = db.Column(db.Unicode(256), nullable=False)
    inn = db.Column(db.Unicode(32), nullable=False)
    ogrn = db.Column(db.Unicode(32), nullable=False)
    address_place = db.Column(db.UnicodeText)
    address_arenda = db.Column(db.UnicodeText)
    address_post = db.Column(db.UnicodeText)
    gendir = db.Column(db.Unicode, nullable=False)
    contact = db.Column(db.UnicodeText, nullable=False)
    addr_site_post = db.Column(db.UnicodeText)
    site = db.Column(db.Unicode(128))
    email = db.Column(db.UnicodeText)
    posrednik = db.Column(db.UnicodeText, nullable=True)
    posrednik2 = db.Column(db.UnicodeText, nullable=True)  # TODO: объеденить с posrednik и вынести в отд. табл.
    papkugot = db.Column(db.UnicodeText, nullable=True)
    dolg_doc = db.Column(db.UnicodeText, nullable=True)
    specialist = db.Column(db.UnicodeText, nullable=True)
    narush = db.Column(db.UnicodeText, nullable=True)
    sved_dop_iskl_partn = db.Column(db.UnicodeText, nullable=True)
    iskl_chl_partn = db.Column(db.Date)
    osn_izm_chl_partn = db.Column(db.UnicodeText, nullable=False)
    sved_discipl_vozd = db.Column(db.UnicodeText, nullable=True)
    comments = db.Column(db.UnicodeText, nullable=True)
    osob_otmetki = db.Column(db.UnicodeText, nullable=True)
    jalobi = db.Column(db.Date)
    vid_zayavlen = db.Column(db.Unicode, nullable=True)
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
    deleted = db.Column(db.SmallInteger, server_default="'0'")
    resh_desc_kom = db.Column(db.Text, nullable=True)
    edit = db.Column(db.Unicode, nullable=True)  # TODO: to History?
    ro_all_id = db.Column(db.Integer, db.ForeignKey(ROAll.id))
    # fronametro = db.Column(db.Text) # см. ro_status.name
    # froshortnametro = db.Column(db.Text) # см. ro_status.short_name
    svid_date = db.Column(db.Date)
    idTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')

    moderniz = db.Column(db.UnicodeText, nullable=True)

    ro_status = db.relationship(ROStatus)
    check_period = db.relationship(
        'OrganisationChecking',
        primaryjoin='and_(Organisation.id==OrganisationChecking.organisation_id, '
                    'OrganisationChecking.is_archive==0)')
    check_period_archive = db.relationship(
        'OrganisationChecking',
        primaryjoin='and_(Organisation.id==OrganisationChecking.organisation_id, '
                    'OrganisationChecking.is_archive==1)')

    ro_all = db.relationship(ROAll)


class SvidDopuska(db.Model):
    __tablename__ = 'svid_dopuska'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id), index=True)
    name = db.Column(db.Unicode(64))

    organisation = db.relationship(Organisation, backref=db.backref('svid_dopuska'), lazy=False)


class KSV(db.Column):
    __tablename__ = 'organisation_ksv'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey(Organisation.id), index=True)
    uved_ksv = db.Column(db.UnicodeText)
    otmetka_vruch_ksv = db.Column(db.UnicodeText)

    comment = db.Column(db.UnicodeText, nullable=False)
    control = db.Column(db.Date)
    status = db.Column(db.UnicodeText, nullable=False)
    narush = db.Column(db.UnicodeText, nullable=False)
    resul_tproverki = db.Column(db.UnicodeText, nullable=False)
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
    is_archive = db.Column(db.SmallInteger, default="'0'")
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


class ConfigOLD(db.Model):
    __tablename__ = 'tconfig'

    fnum = db.Column(db.Integer, primary_key=True)
    fversnew = db.Column(db.Integer, nullable=False)
    fversold = db.Column(db.Integer, nullable=False)
    fcomp = db.Column(db.Text, nullable=False)
    fuser = db.Column(db.Text, nullable=False)
    fuserinout = db.Column(db.Integer, nullable=False)
    fnumorgnew = db.Column(db.Integer)
    fdostup = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    fidTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class OldExcel(db.Model):
    __tablename__ = 'toldexcel'

    fnum = db.Column(db.Integer, primary_key=True)
    fnumorg = db.Column(db.Integer, nullable=False)
    fro = db.Column(db.Text, nullable=False)
    frosost = db.Column(db.Text, nullable=False)
    fsviddopusk = db.Column(db.Text)
    fsviddopuskarch = db.Column(db.Text)
    fopforg = db.Column(db.Text, nullable=False)
    fnamefull = db.Column(db.Text, nullable=False)
    finn = db.Column(db.Text, nullable=False)
    fogrn = db.Column(db.Text, nullable=False)
    faddrplace = db.Column(db.Text, nullable=False)
    faddrarenda = db.Column(db.Text, nullable=False)
    faddrpost = db.Column(db.Text, nullable=False)
    fgendir = db.Column(db.Text, nullable=False)
    fcontlico = db.Column(db.Text, nullable=False)
    faddrsitepost = db.Column(db.Text, nullable=False)
    fwwwsite = db.Column(db.Text, nullable=False)
    femail = db.Column(db.Text, nullable=False)
    fposredn = db.Column(db.Text, nullable=False)
    fpapkugot = db.Column(db.Text, nullable=False)
    fdolgdocum = db.Column(db.Text, nullable=False)
    fvidrabbesop = db.Column(db.Text, nullable=False)
    fuvedksv = db.Column(db.Text, nullable=False)
    fotmetkavruchksv = db.Column(db.Text, nullable=False)
    fcpecialist = db.Column(db.Text, nullable=False)
    fperiodprov = db.Column(db.Text, nullable=False)
    fperiodprovarch = db.Column(db.Text, nullable=False)
    fdateprov = db.Column(db.Date)
    fdateprovarch = db.Column(db.Text, nullable=False)
    fdatelastprov = db.Column(db.Date)
    fdateuvedkk = db.Column(db.Date)
    fuvedkk = db.Column(db.Text, nullable=False)
    fdateotpravkk = db.Column(db.Date)
    faktkk = db.Column(db.Text, nullable=False)
    fotmvruchkk = db.Column(db.Text, nullable=False)
    fsostkk = db.Column(db.Text, nullable=False)
    fnarush = db.Column(db.Text, nullable=False)
    fresprovarch = db.Column(db.Text, nullable=False)
    fdatepereddk = db.Column(db.Date)
    fdeloorgdk = db.Column(db.Text, nullable=False)
    fdatezaseddk = db.Column(db.Date)
    fdatezaseddkarch = db.Column(db.Text, nullable=False)
    fuveddk = db.Column(db.Text, nullable=False)
    fotmvruchdk = db.Column(db.Text, nullable=False)
    fprotdk = db.Column(db.Text, nullable=False)
    fotmvruchdk2 = db.Column(db.Text, nullable=False)
    fsveddopisklpartn = db.Column(db.Text, nullable=False)
    fsveddisciplvozd = db.Column(db.Text, nullable=False)
    fsostdk = db.Column(db.Text, nullable=False)
    frekomenddk = db.Column(db.Text, nullable=False)
    fcomments = db.Column(db.Text, nullable=False)
    fosobotmetki = db.Column(db.Text, nullable=False)
    fjalobi = db.Column(db.Date)
    fvidzayavlen = db.Column(db.Text, nullable=False)
    fdatezayavlen = db.Column(db.Date)
    fvidrabisklopasn = db.Column(db.Text, nullable=False)
    fvidrabvklopasnisklatom = db.Column(db.Text, nullable=False)
    fvidrabvklopasnvklatom = db.Column(db.Text, nullable=False)
    fperedsp = db.Column(db.Date)
    fosnizmchlpartn = db.Column(db.Text, nullable=False)
    fbegindatesvid = db.Column(db.Date)
    fdatevidposlsvid = db.Column(db.Date)
    fprekrsvid = db.Column(db.Date)
    fisklchlpartn = db.Column(db.Date)
    fzadoljvznos = db.Column(db.Text, nullable=False)
    fdeloorgarch = db.Column(db.Text, nullable=False)
    fdeloorgvidano = db.Column(db.Text, nullable=False)
    fvopros = db.Column(db.Text, nullable=False)
    fperiodprovedprov = db.Column(db.Text, nullable=False)
    fdateproverki = db.Column(db.Date)
    fmarkfordel = db.Column(db.Integer, nullable=False)
    freshdesckom = db.Column(db.Text, nullable=False)
    fedit = db.Column(db.Text, nullable=False)
    froall = db.Column(db.Text, nullable=False)
    fopforglong = db.Column(db.Text)
    fvidrabisklopasnTemp = db.Column(db.Text)
    fronametro = db.Column(db.Text)
    froshortnametro = db.Column(db.Text)
    fvidrabvklopasnisklatomTemp = db.Column(db.Text)
    fvidrabvklopasnvklatomTemp = db.Column(db.Text)
    fsviddate = db.Column(db.Date)
    fposredn2 = db.Column(db.Text, nullable=False)
    fidposrednik = db.Column(db.Integer, nullable=False)
    fidTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    fpdaktpd = db.Column(db.Text, nullable=False)
    fpdkomment = db.Column(db.Text, nullable=False)
    fpdcontrol = db.Column(db.Date)
    fpdsostpd = db.Column(db.Text, nullable=False)
    fpdnarush = db.Column(db.Text, nullable=False)
    fpdresultproverki = db.Column(db.Text, nullable=False)
    fpdperedachadk = db.Column(db.Date)
    fpdrekomenddk = db.Column(db.Text, nullable=False)
    fksvkomment = db.Column(db.Text, nullable=False)
    fksvcontrol = db.Column(db.Date)
    fksvsostksv = db.Column(db.Text, nullable=False)
    fksvnarush = db.Column(db.Text, nullable=False)
    fksvresultproverki = db.Column(db.Text, nullable=False)
    fksvperedachadk = db.Column(db.Date)
    fksvrekomenddk = db.Column(db.Text, nullable=False)
    fkkbo = db.Column(db.Text, nullable=False)
    fkkkomment = db.Column(db.Text, nullable=False)
    fkkcontrol = db.Column(db.Date)
    fkkrekomenddk = db.Column(db.Text, nullable=False)
    fdkkomment = db.Column(db.Text, nullable=False)
    fdkcontrol = db.Column(db.Date)
    fmoderniz = db.Column(db.Text, nullable=False)


class OpfOLD(db.Model):
    __tablename__ = 'topf'

    fnum = db.Column(db.Integer, primary_key=True)
    flongname = db.Column(db.Text, nullable=False)
    fshortname = db.Column(db.Text, nullable=False)
    fidTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Postreestr(db.Model):
    __tablename__ = 'tpostreestr'

    fid = db.Column(db.Integer, primary_key=True)
    fnum = db.Column(db.Integer, nullable=False)
    fpoluchatel = db.Column(db.Text, nullable=False)
    fpoladdr = db.Column(db.Text, nullable=False)
    fspisdoc = db.Column(db.Text, nullable=False)
    fotpravitel = db.Column(db.Text, nullable=False)
    fotpravaddr = db.Column(db.Text, nullable=False)
    fotpravotdel = db.Column(db.Text, nullable=False)
    fotpravfio = db.Column(db.Text, nullable=False)
    fotpravdate = db.Column(db.Date)
    fpolprim = db.Column(db.Text, nullable=False)
    fpolfio = db.Column(db.Text, nullable=False)
    fpoldate = db.Column(db.Date)
    fidTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class SvidDopuskArchOld(db.Model):
    __tablename__ = 'tsviddopuskarch_old'

    fnum = db.Column(db.Integer, primary_key=True)
    fsviddopuskarch = db.Column(db.Text, nullable=False)
    fsviddate = db.Column(db.Date)
    fvidrabbesop = db.Column(db.Text, nullable=False)
    fnamefile = db.Column(db.Text, nullable=False)
    ffile = db.Column(db.BLOB, nullable=False)
    fvidrabisklopasn = db.Column(db.Text, nullable=False)
    fvidrabvklopasnisklatom = db.Column(db.Text, nullable=False)
    fvidrabvklopasnvklatom = db.Column(db.Text, nullable=False)
    fprekrsvid = db.Column(db.Date)
    fprekr = db.Column(db.Integer, nullable=False)
    fnumtoldexcel = db.Column(db.Integer, nullable=False)
    fmarkfordel = db.Column(db.Integer, nullable=False)
    fvidrabisklopasnTemp = db.Column(db.Text, nullable=False)
    fvidrabvklopasnisklatomTemp = db.Column(db.Text, nullable=False)
    fvidrabvklopasnvklatomTemp = db.Column(db.Text, nullable=False)
    fidTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Trebovaniya(db.Model):
    __tablename__ = 'ttrebovaniya'

    fnum = db.Column(db.Integer, primary_key=True)
    fkatobj = db.Column(db.Text, nullable=False)
    fnumvidrab = db.Column(db.Text, nullable=False)
    fnamevidrab = db.Column(db.Text, nullable=False)
    fro = db.Column(db.Integer, nullable=False)
    fblockrow = db.Column(db.Integer, nullable=False)
    fidTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class UsersLog(db.Model):
    __tablename__ = 'tuserslog'

    fnum = db.Column(db.Integer, primary_key=True)
    fdate = db.Column(db.Date, nullable=False)
    ftime = db.Column(db.Time, nullable=False)
    fuser = db.Column(db.Text, nullable=False)
    fcomp = db.Column(db.Text, nullable=False)
    ftypeoper = db.Column(db.Text, nullable=False)
    fidTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Zayavka(db.Model):
    __tablename__ = 'tzayavka'

    fid = db.Column(db.Integer, primary_key=True)
    fzayavka = db.Column(db.Text, nullable=False)
    fuser = db.Column(db.Text, nullable=False)
    fchek = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    fidTimeStamp = db.Column(db.DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


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
