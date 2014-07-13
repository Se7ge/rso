# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname('..'))
from application.app import app
from application.models.history import *
from application.models.old import *
from application.models.models import *
from scripts.migrate import __get_org_status, __get_opf, __get_posrednik, __get_prepare_case
from scripts.migrate import __get_ro_all, __get_check_period, __get_res_prov


def __set_svid_dopuska(organisation_id, svid_dopuska, is_archive=False):
    svid_dopuska_list = svid_dopuska.split('\n')
    if isinstance(svid_dopuska_list, list):
        for svid in svid_dopuska_list:
            obj = OrganisationSvidDopuskaHistory()
            obj.name = svid.strip()
            obj.organisation_history_id = organisation_id
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
        obj = KSVHistory()
        obj.organisation_history_id = organisation_id
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
        obj = KKHistory()
        obj.organisation_history_id = organisation_id
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
        obj = DKHistory()
        obj.organisation_history_id = organisation_id
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
        obj = PDHistory()
        obj.organisation_history_id = organisation_id
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


def __set_org_checking(organisation_id, old):
    old_period_prov = old.fperiodprov.strip()
    if old_period_prov:
        per = __get_check_period(old_period_prov)
        obj = OrganisationCheckingHistory()
        obj.organisation_history_id = organisation_id
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
                    obj = OrganisationCheckingHistory()
                    per_arch = __get_check_period(old_period_prov_arch)
                    obj.organisation_history_id = organisation_id
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
            obj = OrganisationWorkTypeHistory()
            obj.organisation_history_id = organisation_id
            obj.work_type_id = work_type.work_type_id
            obj.category_id = work_type.category_id
            db.session.add(obj)
            db.session.commit()


def __migrate_organisation_history(old):
    if old.fnumorg:
        obj = OrganisationHistory()
        obj.organisation_id = old.fnumorg
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
        db.session.add(obj)
        db.session.commit()

        __set_svid_dopuska(obj.id, old.fsviddopusk)
        __set_svid_dopuska(obj.id, old.fsviddopuskarch, True)
        __set_ksv(obj.id, old)
        __set_kk(obj.id, old)
        __set_dk(obj.id, old)
        __set_pd(obj.id, old)

        __set_work_types(obj.id, old.fvidrabisklopasn)
        __set_work_types(obj.id, old.fvidrabvklopasnisklatom)
        __set_work_types(obj.id, old.fvidrabvklopasnvklatom)

        __set_org_checking(obj.id, old)


def migrate_history():
    data = OldExcel.query.filter(OldExcel.fmarkfordel == 1).order_by(OldExcel.fnumorg).all()
    for old in data:
        __migrate_organisation_history(old)


if __name__ == '__main__':
    with app.app_context():
        migrate_history()