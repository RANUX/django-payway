# -*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django_simptools.models import RandomUIDAbstractModel
from payway.accounts.models import MAX_MONEY_DIGITS, MAX_MONEY_PLACES
from payway.orders.conf.settings import ORDER_MIN_SUM


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class OrderForm(forms.Form):

    uid = forms.IntegerField(
        label=_('order number'),
        min_value=0,
        max_value=RandomUIDAbstractModel.MAX_UID,
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )

    sum = forms.DecimalField(
        label=_('order sum'),
        max_digits=MAX_MONEY_DIGITS,
        decimal_places=MAX_MONEY_PLACES,
        min_value=ORDER_MIN_SUM,
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        required=True
    )

    account = forms.ChoiceField(
        label=_('account'),
        widget=forms.Select, required=False
    )

    description = forms.CharField(
        label=_('description'),
        widget=forms.Textarea(attrs={'readonly':'readonly'}),
        max_length=255,
    )

    merchant_uid = forms.IntegerField(widget=forms.HiddenInput())
    merchant_account = forms.IntegerField(
            label=_('merchant account'),
            widget=forms.TextInput(attrs={'readonly':'readonly'})
    )


    def __init__(self, accounts=None, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if accounts:
            self.set_account_field_choices(accounts)

    def set_account_field_choices(self, accounts):
        self.fields['account'].choices = [
            (a.uid, u'{0} {1} {2}'.format(a.currency, a.uid, a.get_balance())) for a in accounts
        ]

    def set_not_enough_money_error(self):
        self._errors['account'] = ErrorList([_(u'not enough money')])

