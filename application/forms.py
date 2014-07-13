# -*- coding: utf-8 -*-
from wtforms import StringField, BooleanField, PasswordField, RadioField, TextAreaField, FormField
from wtforms.validators import Required
from flask_wtf import Form
from wtforms_alchemy import model_form_factory, ModelFormField, ModelFieldList, SelectField
from application.models.models import Organisation, Opf, PD

from application.app import db, app

BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class OpfForm(ModelForm):
    class Meta:
        model = Opf


class PdForm(ModelForm):
    class Meta:
        model = PD


class OrganisationForm(ModelForm):
    class Meta:
        model = Organisation

    opf = SelectField(coerce=int)
    email = TextAreaField()
    pd = ModelFieldList(FormField(PdForm))


#----------------#

class LoginForm(Form):
    login = StringField(u'Логин')
    password = PasswordField(u'Пароль')