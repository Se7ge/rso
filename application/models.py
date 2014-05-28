# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, Text, Time
from sqlalchemy.dialects.mysql.base import LONGBLOB
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Tconfig(Base):
    __tablename__ = 'tconfig'

    fnum = Column(Integer, primary_key=True)
    fversnew = Column(Integer, nullable=False)
    fversold = Column(Integer, nullable=False)
    fcomp = Column(Text, nullable=False)
    fuser = Column(Text, nullable=False)
    fuserinout = Column(Integer, nullable=False)
    fnumorgnew = Column(Integer)
    fdostup = Column(Integer, nullable=False, server_default=u"'0'")
    fidTimeStamp = Column(DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Toldexcel(Base):
    __tablename__ = 'toldexcel'

    fnum = Column(Integer, primary_key=True)
    fnumorg = Column(Integer, nullable=False)
    fro = Column(Text, nullable=False)
    frosost = Column(Text, nullable=False)
    fsviddopusk = Column(Text)
    fsviddopuskarch = Column(Text)
    fopforg = Column(Text, nullable=False)
    fnamefull = Column(Text, nullable=False)
    finn = Column(Text, nullable=False)
    fogrn = Column(Text, nullable=False)
    faddrplace = Column(Text, nullable=False)
    faddrarenda = Column(Text, nullable=False)
    faddrpost = Column(Text, nullable=False)
    fgendir = Column(Text, nullable=False)
    fcontlico = Column(Text, nullable=False)
    faddrsitepost = Column(Text, nullable=False)
    fwwwsite = Column(Text, nullable=False)
    femail = Column(Text, nullable=False)
    fposredn = Column(Text, nullable=False)
    fpapkugot = Column(Text, nullable=False)
    fdolgdocum = Column(Text, nullable=False)
    fvidrabbesop = Column(Text, nullable=False)
    fuvedksv = Column(Text, nullable=False)
    fotmetkavruchksv = Column(Text, nullable=False)
    fcpecialist = Column(Text, nullable=False)
    fperiodprov = Column(Text, nullable=False)
    fperiodprovarch = Column(Text, nullable=False)
    fdateprov = Column(Date)
    fdateprovarch = Column(Text, nullable=False)
    fdatelastprov = Column(Date)
    fdateuvedkk = Column(Date)
    fuvedkk = Column(Text, nullable=False)
    fdateotpravkk = Column(Date)
    faktkk = Column(Text, nullable=False)
    fotmvruchkk = Column(Text, nullable=False)
    fsostkk = Column(Text, nullable=False)
    fnarush = Column(Text, nullable=False)
    fresprovarch = Column(Text, nullable=False)
    fdatepereddk = Column(Date)
    fdeloorgdk = Column(Text, nullable=False)
    fdatezaseddk = Column(Date)
    fdatezaseddkarch = Column(Text, nullable=False)
    fuveddk = Column(Text, nullable=False)
    fotmvruchdk = Column(Text, nullable=False)
    fprotdk = Column(Text, nullable=False)
    fotmvruchdk2 = Column(Text, nullable=False)
    fsveddopisklpartn = Column(Text, nullable=False)
    fsveddisciplvozd = Column(Text, nullable=False)
    fsostdk = Column(Text, nullable=False)
    frekomenddk = Column(Text, nullable=False)
    fcomments = Column(Text, nullable=False)
    fosobotmetki = Column(Text, nullable=False)
    fjalobi = Column(Date)
    fvidzayavlen = Column(Text, nullable=False)
    fdatezayavlen = Column(Date)
    fvidrabisklopasn = Column(Text, nullable=False)
    fvidrabvklopasnisklatom = Column(Text, nullable=False)
    fvidrabvklopasnvklatom = Column(Text, nullable=False)
    fperedsp = Column(Date)
    fosnizmchlpartn = Column(Text, nullable=False)
    fbegindatesvid = Column(Date)
    fdatevidposlsvid = Column(Date)
    fprekrsvid = Column(Date)
    fisklchlpartn = Column(Date)
    fzadoljvznos = Column(Text, nullable=False)
    fdeloorgarch = Column(Text, nullable=False)
    fdeloorgvidano = Column(Text, nullable=False)
    fvopros = Column(Text, nullable=False)
    fperiodprovedprov = Column(Text, nullable=False)
    fdateproverki = Column(Date)
    fmarkfordel = Column(Integer, nullable=False)
    freshdesckom = Column(Text, nullable=False)
    fedit = Column(Text, nullable=False)
    froall = Column(Text, nullable=False)
    fopforglong = Column(Text)
    fvidrabisklopasnTemp = Column(Text)
    fronametro = Column(Text)
    froshortnametro = Column(Text)
    fvidrabvklopasnisklatomTemp = Column(Text)
    fvidrabvklopasnvklatomTemp = Column(Text)
    fsviddate = Column(Date)
    fposredn2 = Column(Text, nullable=False)
    fidposrednik = Column(Integer, nullable=False)
    fidTimeStamp = Column(DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    fpdaktpd = Column(Text, nullable=False)
    fpdkomment = Column(Text, nullable=False)
    fpdcontrol = Column(Date)
    fpdsostpd = Column(Text, nullable=False)
    fpdnarush = Column(Text, nullable=False)
    fpdresultproverki = Column(Text, nullable=False)
    fpdperedachadk = Column(Date)
    fpdrekomenddk = Column(Text, nullable=False)
    fksvkomment = Column(Text, nullable=False)
    fksvcontrol = Column(Date)
    fksvsostksv = Column(Text, nullable=False)
    fksvnarush = Column(Text, nullable=False)
    fksvresultproverki = Column(Text, nullable=False)
    fksvperedachadk = Column(Date)
    fksvrekomenddk = Column(Text, nullable=False)
    fkkbo = Column(Text, nullable=False)
    fkkkomment = Column(Text, nullable=False)
    fkkcontrol = Column(Date)
    fkkrekomenddk = Column(Text, nullable=False)
    fdkkomment = Column(Text, nullable=False)
    fdkcontrol = Column(Date)
    fmoderniz = Column(Text, nullable=False)


class Topf(Base):
    __tablename__ = 'topf'

    fnum = Column(Integer, primary_key=True)
    flongname = Column(Text, nullable=False)
    fshortname = Column(Text, nullable=False)
    fidTimeStamp = Column(DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Tpostreestr(Base):
    __tablename__ = 'tpostreestr'

    fid = Column(Integer, primary_key=True)
    fnum = Column(Integer, nullable=False)
    fpoluchatel = Column(Text, nullable=False)
    fpoladdr = Column(Text, nullable=False)
    fspisdoc = Column(Text, nullable=False)
    fotpravitel = Column(Text, nullable=False)
    fotpravaddr = Column(Text, nullable=False)
    fotpravotdel = Column(Text, nullable=False)
    fotpravfio = Column(Text, nullable=False)
    fotpravdate = Column(Date)
    fpolprim = Column(Text, nullable=False)
    fpolfio = Column(Text, nullable=False)
    fpoldate = Column(Date)
    fidTimeStamp = Column(DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class TsviddopuskarchOld(Base):
    __tablename__ = 'tsviddopuskarch_old'

    fnum = Column(Integer, primary_key=True)
    fsviddopuskarch = Column(Text, nullable=False)
    fsviddate = Column(Date)
    fvidrabbesop = Column(Text, nullable=False)
    fnamefile = Column(Text, nullable=False)
    ffile = Column(LONGBLOB, nullable=False)
    fvidrabisklopasn = Column(Text, nullable=False)
    fvidrabvklopasnisklatom = Column(Text, nullable=False)
    fvidrabvklopasnvklatom = Column(Text, nullable=False)
    fprekrsvid = Column(Date)
    fprekr = Column(Integer, nullable=False)
    fnumtoldexcel = Column(Integer, nullable=False)
    fmarkfordel = Column(Integer, nullable=False)
    fvidrabisklopasnTemp = Column(Text, nullable=False)
    fvidrabvklopasnisklatomTemp = Column(Text, nullable=False)
    fvidrabvklopasnvklatomTemp = Column(Text, nullable=False)
    fidTimeStamp = Column(DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Ttrebovaniya(Base):
    __tablename__ = 'ttrebovaniya'

    fnum = Column(Integer, primary_key=True)
    fkatobj = Column(Text, nullable=False)
    fnumvidrab = Column(Text, nullable=False)
    fnamevidrab = Column(Text, nullable=False)
    fro = Column(Integer, nullable=False)
    fblockrow = Column(Integer, nullable=False)
    fidTimeStamp = Column(DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Tuserslog(Base):
    __tablename__ = 'tuserslog'

    fnum = Column(Integer, primary_key=True)
    fdate = Column(Date, nullable=False)
    ftime = Column(Time, nullable=False)
    fuser = Column(Text, nullable=False)
    fcomp = Column(Text, nullable=False)
    ftypeoper = Column(Text, nullable=False)
    fidTimeStamp = Column(DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Tzayavka(Base):
    __tablename__ = 'tzayavka'

    fid = Column(Integer, primary_key=True)
    fzayavka = Column(Text, nullable=False)
    fuser = Column(Text, nullable=False)
    fchek = Column(Integer, nullable=False, server_default=u"'0'")
    fidTimeStamp = Column(DateTime, nullable=False, server_default=u'CURRENT_TIMESTAMP')