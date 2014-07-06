# coding: utf-8
from application.database import db


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

