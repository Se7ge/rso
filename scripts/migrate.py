# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname('..'))

from application.app import app, db
from application.models import *
from application.old_models import *

MAPPER = {
    'field': {'table': 'table', 'field': 'field'}
}


def _check_by_id(table, _id):
    obj = db.session.query(table).get(_id)
    return obj is not None


def _check_by_name(table, name):
    return db.session.query(table).filter(table.name == name).count() > 0


def _check_by_code(table, name):
    return db.session.query(table).filter(table.code == name).count() > 0


def _migrate_opf():
    data = OpfOLD.query.all()
    for opf in data:
        if not _check_by_id(Opf, opf.fnum):
            obj = Opf()
            obj.id = opf.fnum
            obj.short_name = opf.fshortname
            obj.long_name = opf.flongname
            obj.created = opf.fidTimeStamp
            db.session.add(obj)
            db.session.commit()


def _migrate_ro():
    data = (db.session.query(db.distinct(OldExcel.fro), OldExcel.fronametro, OldExcel.froshortnametro)
            .filter(db.and_(OldExcel.fronametro != '', OldExcel.froshortnametro != ''))
            .all())
    for old in data:
        fro, fronametro, froshortnametro = old
        if not _check_by_id(RO, fro):
            obj = RO()
            obj.id = fro
            obj.short_name = froshortnametro
            obj.name = fronametro
            db.session.add(obj)
            db.session.commit()


def _migrate_ro_status():
    data = db.session.query(db.distinct(OldExcel.frosost)).all()
    for old in data:
        frosost, = old
        check = db.session.query(ROStatus).filter(db.or_(ROStatus.name==u'{0}.'.format(frosost),
                                                         ROStatus.name==frosost.strip('.'))).count()
        if frosost and not check:
            obj = ROStatus()
            obj.short_name = frosost
            obj.name = frosost
            db.session.add(obj)
            db.session.commit()


def _migrate_posrednik():
    data = db.session.query(db.distinct(OldExcel.fposredn)).all()
    for old in data:
        fposredn, = old
        if fposredn:
            check = db.session.query(OrganisationPosrednik).filter(OrganisationPosrednik.name==fposredn).count()
            if fposredn and not check:
                obj = OrganisationPosrednik()
                obj.name = fposredn
                db.session.add(obj)
                db.session.commit()
    data = db.session.query(db.distinct(OldExcel.fposredn2)).all()
    for old in data:
        fposredn, = old
        if fposredn:
            check = db.session.query(OrganisationPosrednik).filter(OrganisationPosrednik.name==fposredn).count()
            if fposredn and not check:
                obj = OrganisationPosrednik()
                obj.name = fposredn
                db.session.add(obj)
                db.session.commit()


def _migrate_work_type_categories():
    data = (db.session.query(db.distinct(Trebovaniya.fkatobj))
            .filter(Trebovaniya.fkatobj != '')
            .all())
    for old in data:
        fkatobj, = old
        if not _check_by_code(WorkTypeCategory, fkatobj):
            obj = WorkTypeCategory()
            obj.code = fkatobj
            db.session.add(obj)
            db.session.commit()


def _migrate_work_types():
    data = (db.session.query(Trebovaniya.fnumvidrab, Trebovaniya.fnamevidrab, Trebovaniya.fro)
            .filter(Trebovaniya.fkatobj != '')
            .all())
    for old in data:
        fnumvidrab, fnamevidrab, fro = old
        obj = WorkType()
        obj.code = fnumvidrab
        obj.name = fnamevidrab
        obj.ro_id = fro
        db.session.add(obj)
        try:
            db.session.commit()
        except Exception, e:
            print e
            db.session.rollback()


def __get_work_type(code, ro_id):
    return WorkType.query.filter(db.and_(WorkType.code == code, WorkType.ro_id == ro_id)).first()


def __get_work_type_category(code):
    return WorkTypeCategory.query.filter(WorkTypeCategory.code == code).first()


def _migrate_work_types_relations():
    data = (db.session.query(Trebovaniya.fnum, Trebovaniya.fkatobj, Trebovaniya.fnumvidrab, Trebovaniya.fro, Trebovaniya.fblockrow)
            .filter(Trebovaniya.fkatobj != '')
            .all())
    for old in data:
        fnum, fkatobj, fnumvidrab, fro, fblockrow = old
        work_type = __get_work_type(fnumvidrab, fro)
        if not work_type:
            print 'Error find work_type ({0}, {1})'.format(fnumvidrab, fro)
            continue
        work_type_category = __get_work_type_category(fkatobj)
        if not work_type_category:
            print 'Error find work_type_category ({0})'.format(fkatobj)
            continue
        obj = WorkTypeRelations()
        obj.id = fnum
        obj.work_type_id = work_type.id
        obj.category_id = work_type_category.id
        db.session.add(obj)
        try:
            db.session.commit()
        except Exception, e:
            print e
            db.session.rollback()


def _migrate_user_config():
    data = ConfigOLD.query.all()
    for old in data:
        if not _check_by_id(UserConfig, old.fnum):
            obj = UserConfig()
            obj.id = old.fnum
            obj.versnew = old.fversnew
            obj.versold = old.fversold
            obj.comp = old.fcomp
            obj.user = old.fuser
            obj.userinout = old.fuserinout
            obj.numorgnew = old.fnumorgnew
            obj.dostup = old.fdostup
            obj.idTimeStamp = old.fidTimeStamp
            db.session.add(obj)
            db.session.commit()


def migrate_dicts():
    # _migrate_opf()
    # _migrate_ro()
    # _migrate_ro_status()
    # _migrate_work_type_categories()
    # _migrate_work_types()
    # _migrate_work_types_relations()
    # _migrate_user_config()
    _migrate_posrednik()
    pass


def __get_org_status(name):
    return db.session.query(ROStatus).filter(db.or_(ROStatus.name==u'{0}.'.format(name),
                                                    ROStatus.name==name.strip('.'))).first()


def __get_opf(name):
    return db.session.query(Opf).filter(Opf.name==name).first()


def __set_svid_dopuska(organisation_id, svid_dopuska, is_archive=False):
    svid_dopuska_list = svid_dopuska.split('\n')
    if isinstance(svid_dopuska_list, list):
        for svid in svid_dopuska_list:
            obj = OrganisationSvidDopuska()
            obj.name = svid
            obj.organisation_id = organisation_id
            obj.is_archive = is_archive
            db.session.add(obj)
            db.session.commit()


def __set_ksv(organisation_id, old):
    if (old.fuvedksv or
            old.fotmetkavruchksv or
            old.fksvkomment or
            old.fksvcontrol or
            old.fksvsostksv or
            old.fksvnarush or
            old.fksvresultproverki or
            old.fksvperedachadk or
            old.fksvrekomenddk):
        obj = KSV()
        obj.organisation_id = organisation_id
        obj.uved = old.fuvedksv
        obj.otmetka_vruch = old.fotmetkavruchksv
        obj.comment = old.fksvkomment
        obj.control = old.fksvcontrol
        obj.status = old.fksvsostksv
        obj.narush = old.fksvnarush
        obj.result_proverki = old.fksvresultproverki
        obj.peredacha_dk = old.fksvperedachadk
        obj.recommendation_dk = old.fksvrekomenddk
        db.session.add(obj)
        db.session.commit()


def __set_kk(organisation_id, old):
    if (old.fdateuvedkk or
            old.fuvedkk or
            old.fdateotpravkk or
            old.faktkk or
            old.fotmvruchkk or
            old.fsostkk or
            old.fkkbo or
            old.fkkkomment or
            old.fkkcontrol or
            old.fkkrekomenddk):
        obj = KK()
        obj.organisation_id = organisation_id
        obj.uved = old.fuvedkk
        obj.date_uved = old.fdateuvedkk
        obj.date_otprav = old.fdateotpravkk
        obj.akt = old.faktkk
        obj.otm_vruch = old.fotmvruchkk
        obj.status = old.fsostkk
        obj.bo = old.fkkbo
        obj.comment = old.fkkkomment
        obj.control = old.fkkcontrol
        obj.recommendation_dk = old.fkkrekomenddk
        db.session.add(obj)
        db.session.commit()


def __get_posrednik(posrednik):
    if not posrednik:
        return None
    p = OrganisationPosrednik.query.filter(OrganisationPosrednik.name == posrednik).first()
    if not p:
        p = OrganisationPosrednik()
        p.name = posrednik
        db.session.add(p)
        db.session.commit()
    return p


def __get_check_period(period):
    if not period:
        return None
    p = CheckPeriod.query.filter(CheckPeriod.name == period).first()
    if not p:
        p = CheckPeriod()
        p.name = period
        db.session.add(p)
        db.session.commit()
    return p


def __set_org_check_period(organisation_id, period, is_archive=False):
    svid_dopuska_list = svid_dopuska.split('\n')
    if isinstance(svid_dopuska_list, list):
        for svid in svid_dopuska_list:
            obj = OrganisationSvidDopuska()
            obj.name = svid
            obj.organisation_id = organisation_id
            obj.is_archive = is_archive
            db.session.add(obj)
            db.session.commit()


def __get_prepare_case(prepare_case):
    if not prepare_case:
        return None
    p = OrganisationPrepareCase.query.filter(OrganisationPrepareCase.name == prepare_case).first()
    if not p:
        p = OrganisationPrepareCase()
        p.name = prepare_case
        db.session.add(p)
        db.session.commit()
    return p


def _migrate_actual_orgs():
    data = OldExcel.query.filter(OldExcel.fmarkfordel == 0).order_by(OldExcel.fnumorg).all()
    for old in data:
        if not _check_by_id(Organisation, old.fnumorg):
            obj = Organisation()
            obj.id = old.fnumorg
            obj.ro_id = int(old.ro)
            obj.ro_status = __get_org_status(old.frostatus)
            obj.opf = __get_opf(old.fopforg)
            obj.name = old.fnamefull
            obj.inn = old.finn
            obj.ogrn = old.fogrn
            obj.address_place = old.addrplace
            obj.address_arenda = old.addrarenda
            obj.gendir = old.gendir
            obj.contact = old.fcontlico
            obj.site = old.fwwwsite
            obj.email = old.femail

            if old.fposredn:
                posrednik = __get_posrednik(old.fposredn)
                if posrednik:
                    obj.posrednik_id = posrednik.id

            if old.fpapkugot:
                prepare_case = __get_prepare_case(old.fpapkugot)
                if prepare_case:
                    obj.prepare_case_id = prepare_case.id

            obj.dolg_doc = old.fdolgdocum
            obj.narush = old.fnarush
            obj.sved_dop_iskl_partn = old.fnarush

            obj.idTimeStamp = old.fidTimeStamp
            db.session.add(obj)
            db.session.commit()

            __set_svid_dopuska(obj.id, old.fsviddopusk)
            __set_svid_dopuska(obj.id, old.fsviddopuskarch, True)
            __set_ksv(obj.id, old)
            __set_kk(obj.id, old)

            # TODO:
            __set_org_check_period()


def _migrate_history():
    pass


def migrate_org_data():
    _migrate_actual_orgs()
    _migrate_history()


if __name__ == '__main__':
    with app.app_context():
        migrate_dicts()
        # migrate_org_data()
