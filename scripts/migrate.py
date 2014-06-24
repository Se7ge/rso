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
    _migrate_opf()
    _migrate_ro()
    _migrate_work_type_categories()
    _migrate_work_types()
    _migrate_work_types_relations()
    _migrate_user_config()


def _migrate_actual_orgs():
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


def _migrate_history():
    pass


def migrate_org_data():
    _migrate_actual_orgs()


if __name__ == '__main__':
    with app.app_context():
        migrate_dicts()
        migrate_org_data()
