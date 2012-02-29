# -*- coding: UTF-8 -*-
from django import forms
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect
from django.utils.translation import ugettext_lazy as _
from django_simptools.models import RandomUIDAbstractModel
from payway.accounts.models import MAX_MONEY_PLACES, MAX_MONEY_DIGITS

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

MIN_MONEY_VALUE = 1.0


PAYMENT_SYSTEM_CHOICES = (
    ('webmoney_add_money', 'Webmoney WMR'),
    ('qiwi_add_money', 'Qiwi RUB'),
)


class AddMoneyForm(forms.Form):
    money_amount = forms.DecimalField(
        label=_('money amount'),
        min_value=MIN_MONEY_VALUE,
        max_digits=MAX_MONEY_DIGITS,
        decimal_places=MAX_MONEY_PLACES,
    )
    invoice_uid = forms.IntegerField(max_value=RandomUIDAbstractModel.MAX_UID, widget=forms.HiddenInput())

    payment_system = ChoiceField(
        label=_('payment system'),
        widget=RadioSelect,
        choices=PAYMENT_SYSTEM_CHOICES
    )
