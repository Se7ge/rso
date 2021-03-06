# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname('..'))

from application.app import app
from application.models.old import *
from application.models.models import *


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
            obj.name = opf.fshortname
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
            obj.name = svid.strip()
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


def __set_dk(organisation_id, old):
    if (old.fdatepereddk or
            old.fdeloorgdk or
            old.fdatezaseddk or
            old.fdatezaseddkarch or
            old.fuveddk or
            old.fotmvruchdk or
            old.fprotdk or
            old.fotmvruchdk2 or
            old.fsostdk or
            old.frekomenddk or
            old.fdkkomment or
            old.fdkcontrol):
        obj = DK()
        obj.organisation_id = organisation_id
        obj.date_pered = old.fdatepereddk
        obj.delo_org = old.fdeloorgdk
        obj.date_zased = old.fdatezaseddk
        obj.date_zased_arch = old.fdatezaseddkarch
        obj.uved = old.fuveddk
        obj.otm_vruch = old.fotmvruchdk
        obj.protocol = old.fprotdk
        obj.otm_vruch2 = old.fotmvruchdk2
        obj.status = old.fsostdk
        obj.recommendation_dk = old.frekomenddk
        obj.comment = old.fdkkomment
        obj.control = old.fdkcontrol
        db.session.add(obj)
        db.session.commit()


def __set_pd(organisation_id, old):
    if (old.fpdaktpd or
            old.fpdkomment or
            old.fpdcontrol or
            old.fpdsostpd or
            old.fpdnarush or
            old.fpdresultproverki or
            old.fpdperedachadk or
            old.fpdrekomenddk):
        obj = PD()
        obj.organisation_id = organisation_id
        obj.akt = old.fpdaktpd
        obj.comment = old.fpdkomment
        obj.control = old.fpdcontrol
        obj.status = old.fpdsostpd
        obj.narush = old.fpdnarush
        obj.result_proverki = old.fpdresultproverki
        obj.peredacha_dk = old.fpdperedachadk
        obj.recommendation_dk = old.fpdrekomenddk
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


def __get_res_prov(results, dateprov):
    for res_prov in results:
        if res_prov.find(dateprov) > -1:
            return res_prov.replace(dateprov, u'').strip()
    return None


def __set_org_checking(organisation_id, old):
    old_period_prov = old.fperiodprov.strip()
    if old_period_prov:
        per = __get_check_period(old_period_prov)
        obj = OrganisationChecking()
        obj.organisation_id = organisation_id
        obj.check_period_id = per.id
        obj.checking_date = old.fdateprov
        db.session.add(obj)
        try:
            db.session.commit()
        except Exception, e:
            print e
            db.session.rollback()

    if old.fperiodprovarch:
        check_period_list = old.fperiodprovarch.split('\n')
        check_dates_list = old.fdateprovarch.split('\n')
        check_res_list = old.fresprovarch.split('\n')

        if check_period_list:
            for k, v in enumerate(check_period_list):
                old_period_prov_arch = v.strip()
                if old_period_prov_arch and old_period_prov != old_period_prov_arch:
                    obj = OrganisationChecking()
                    per_arch = __get_check_period(old_period_prov_arch)
                    obj.organisation_id = organisation_id
                    obj.check_period_id = per_arch.id
                    obj.is_archive = True
                    try:
                        prov_date = check_dates_list[k].strip()
                    except IndexError:
                        print 'no {0} index in check_dates_list'.format(k)
                    else:
                        try:
                            checking_date = datetime.strptime(prov_date, '%d.%m.%Y')
                        except ValueError, e:
                            print e
                        else:
                            obj.checking_date = checking_date
                            res_prov = __get_res_prov(check_res_list, prov_date)
                            if res_prov:
                                obj.checking_result = res_prov
                            db.session.add(obj)
                            try:
                                db.session.commit()
                            except Exception, e:
                                print e
                                db.session.rollback()


def __set_work_types(organisation_id, work_types):
    if not work_types:
        return None
    work_types_list = work_types.split(',')
    if isinstance(work_types_list, list):
        for work_type_id in work_types_list:
            work_type = WorkTypeRelations.query.get(int(work_type_id))
            obj = OrganisationWorkType()
            obj.organisation_id = organisation_id
            obj.work_type_id = work_type.work_type_id
            obj.category_id = work_type.category_id
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


def __get_ro_all(ro_all):
    if not ro_all:
        return None
    p = ROAll.query.filter(ROAll.name == ro_all).first()
    if not p:
        p = ROAll()
        p.name = ro_all
        db.session.add(p)
        db.session.commit()
    return p


def __migrate_organisation(old):
    if old.fnumorg and not _check_by_id(Organisation, old.fnumorg):
        obj = Organisation()
        obj.id = old.fnumorg
        print obj.id
        obj.ro_id = int(old.fro)
        obj.ro_status = __get_org_status(old.frosost)
        obj.opf = __get_opf(old.fopforg)
        obj.name = old.fnamefull
        obj.inn = old.finn
        obj.ogrn = old.fogrn
        obj.address_place = old.faddrplace
        obj.address_arenda = old.faddrarenda
        obj.gendir = old.fgendir
        obj.contact = old.fcontlico
        obj.site = old.fwwwsite
        obj.email = old.femail

        if old.fposredn:
            posrednik = __get_posrednik(old.fposredn)
            if posrednik:
                obj.posrednik_id = posrednik.id

        if old.fposredn2:
            posrednik2 = __get_posrednik(old.fposredn2)
            if posrednik2:
                obj.posrednik2_id = posrednik2.id

        if old.fpapkugot:
            prepare_case = __get_prepare_case(old.fpapkugot)
            if prepare_case:
                obj.prepare_case_id = prepare_case.id

        obj.dolg_doc = old.fdolgdocum
        obj.narush = old.fnarush
        obj.sved_dop_iskl_partn = old.fnarush
        obj.comments = old.fcomments
        obj.osob_otmetki = old.fosobotmetki
        obj.jalobi = old.fjalobi
        obj.vid_zayavlen = old.fvidzayavlen
        obj.date_zayavlen = old.fdatezayavlen
        obj.pered_sp = old.fperedsp
        obj.osn_izm_chl_partn = old.fosnizmchlpartn
        obj.svid_begin_date = old.fbegindatesvid
        obj.svid_date = old.fsviddate
        obj.prekr_svid_date = old.fprekrsvid
        obj.iskl_chl_partn = old.fisklchlpartn
        obj.zadolj_vznos = old.fzadoljvznos
        obj.delo_org_arch = old.fdeloorgarch
        obj.delo_org_vidano = old.fdeloorgvidano
        obj.vopros = old.fvopros
        obj.deleted = old.fmarkfordel
        obj.resh_desc_kom = old.freshdesckom
        obj.edit = old.fedit
        obj.deleted = bool(old.fmarkfordel)

        if old.froall:
            ro_all = __get_ro_all(old.froall)
            if ro_all:
                obj.ro_all_id = ro_all.id

        obj.idTimeStamp = old.fidTimeStamp

        try:
            db.session.add(obj)
            db.session.commit()
        except Exception, e:
            print e
            db.session.rollback()
        else:
            organisation_id = obj.id
            if old.fsviddopusk:
                __set_svid_dopuska(organisation_id, old.fsviddopusk)
            if old.fsviddopuskarch:
                __set_svid_dopuska(organisation_id, old.fsviddopuskarch, True)
            __set_ksv(organisation_id, old)
            __set_kk(organisation_id, old)
            __set_dk(organisation_id, old)
            __set_pd(organisation_id, old)

            __set_work_types(organisation_id, old.fvidrabisklopasn)
            __set_work_types(organisation_id, old.fvidrabvklopasnisklatom)
            __set_work_types(organisation_id, old.fvidrabvklopasnvklatom)

            __set_org_checking(organisation_id, old)


def __link_posrednik(old):
    obj = db.session.query(Organisation).get(old.fnumorg)
    if not obj:
        return None
    if old.fposredn:
        posrednik = __get_posrednik(old.fposredn)
        if posrednik:
            obj.posrednik_id = posrednik.id

    if old.fposredn2:
        posrednik2 = __get_posrednik(old.fposredn2)
        if posrednik2:
            obj.posrednik2_id = posrednik2.id

    try:
        db.session.add(obj)
        db.session.commit()
    except Exception, e:
        print e
        db.session.rollback()


def _migrate_actual_orgs():
    data = OldExcel.query.filter(OldExcel.fmarkfordel == 0).order_by(OldExcel.fnumorg).all()
    for old in data:
        __migrate_organisation(old)
        __link_posrednik(old)  # TMP


def _migrate_deleted_orgs():
    stmt = db.session.query(db.distinct(OldExcel.fnumorg)).filter(OldExcel.fmarkfordel == 0).subquery()
    data = OldExcel.query.filter(db.not_(OldExcel.fnumorg.in_(stmt))).order_by(OldExcel.fnumorg).all()
    for old in data:
        __migrate_organisation(old)
        __link_posrednik(old)  # TMP


def migrate_org_data():
    _migrate_actual_orgs()
    _migrate_deleted_orgs()


if __name__ == '__main__':
    with app.app_context():
        migrate_dicts()
        migrate_org_data()
