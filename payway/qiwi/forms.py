# -*- coding: UTF-8 -*-
import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from payway.accounts.models import MAX_MONEY_DIGITS, MAX_MONEY_PLACES
from payway.qiwi.conf.settings import QIWI_PERCENT


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

TNX_ID_RE = re.compile(ur'^\w{1,30}$')

class RequestPaymentForm(forms.Form):

    txn_id = forms.RegexField(regex=TNX_ID_RE, label=_(u'unique payment number'), widget=forms.HiddenInput())
    to = forms.IntegerField(
        label=_('10 digits phone number'),
        max_value=9999999999,
        widget=forms.TextInput(attrs={'maxlength':'10'})
    )
    summ = forms.DecimalField(
            max_digits=MAX_MONEY_DIGITS,
            decimal_places=MAX_MONEY_PLACES,
            label=u'{0} {1}% {2}'.format(_('sum with'), QIWI_PERCENT, _('percent')),
            widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    com = forms.CharField(label=_(u'description'), widget=forms.HiddenInput(), required=False)
    lifetime = forms.IntegerField(required=False, widget=forms.HiddenInput())
    check_agt = forms.BooleanField(required=False, widget=forms.HiddenInput())


    def __init__(self, *args, **kwargs):
        super(RequestPaymentForm, self).__init__(*args, **kwargs)
        # because 'from' is keyword
        self.fields['from'] = forms.IntegerField(label=_('from'), widget=forms.HiddenInput())