# -*- coding: UTF-8 -*-
import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_admins
from django.utils.translation import ugettext_lazy as _
from moneyed.classes import Money
from payway.accounts.models import MAX_MONEY_DIGITS, MAX_MONEY_PLACES, Invoice, Account
from payway.webmoney.conf.settings import WEBMONEY_PERCENT
from payway.webmoney.models import ResultResponsePayment, Purse

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

PURSE_RE = re.compile(ur'^(?P<type>[ZREUYBGDC])(?P<number>\d{12})$')
WMID_RE = re.compile(ur'^\d{12}$')

class BasePaymentForm(forms.Form):
    LMI_PAYMENT_DESC = forms.CharField(label=_(u'description'), widget=forms.HiddenInput())
    LMI_PAYEE_PURSE = forms.RegexField(regex=PURSE_RE, widget=forms.HiddenInput(), required=True)
    LMI_PAYMENT_NO = forms.IntegerField(label=_(u'payment number'), widget=forms.HiddenInput(), required=True)

class RequestPaymentForm(BasePaymentForm):

    LMI_PAYMENT_AMOUNT = forms.DecimalField(
        max_digits=MAX_MONEY_DIGITS,
        decimal_places=MAX_MONEY_PLACES,
        label=u'{0} {1}% {2}'.format(_('sum with'), WEBMONEY_PERCENT, _('percent')),
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        required=True
    )
    LMI_SIM_MODE = forms.IntegerField(initial="0", widget=forms.HiddenInput())


class PrerequestResponsePaymentForm(BasePaymentForm):

    LMI_PREREQUEST = forms.BooleanField(label=_('prerequest flag'), required=False)
    LMI_PAYMENT_AMOUNT = forms.DecimalField(max_digits=MAX_MONEY_DIGITS, decimal_places=MAX_MONEY_PLACES, label=_(u'amount'))
    LMI_MODE = forms.IntegerField(label=_('test mode'), min_value=0, max_value=1)
    LMI_PAYER_WM = forms.RegexField(regex=WMID_RE)
    LMI_PAYER_PURSE = forms.RegexField(regex=PURSE_RE)
    LMI_LANG = forms.CharField(label=_(u'language'), required=False)


class ResultResponsePaymentForm(forms.ModelForm):

    class Meta:
        model = ResultResponsePayment
        exclude = ('payee_purse', 'money_amount', 'status', 'invoice')

    LMI_PAYEE_PURSE = forms.RegexField(regex=PURSE_RE, widget=forms.HiddenInput(), required=True)
    LMI_PAYMENT_NO = forms.IntegerField(label=_(u'payment number'), widget=forms.HiddenInput(), required=True)
    LMI_SYS_TRANS_DATE = forms.DateTimeField(input_formats=['%Y%m%d %H:%M:%S'])
    LMI_PAYER_WM = forms.RegexField(regex=WMID_RE)

    LMI_PAYMENT_AMOUNT = forms.DecimalField(
            max_digits=MAX_MONEY_DIGITS,
            decimal_places=MAX_MONEY_PLACES,
            label=_(u'amount'),
            widget=forms.TextInput(attrs={'readonly':'readonly'}),
            required=True
    )

    def save(self):
        payment = super(ResultResponsePaymentForm, self).save(commit=False)
        payee_purse = Purse.objects.get(purse=self.cleaned_data['LMI_PAYEE_PURSE'])
        money_amount = self.cleaned_data['LMI_PAYMENT_AMOUNT']

        invoice_uid = int(self.cleaned_data['LMI_PAYMENT_NO'])
        try:
            payment.invoice = Invoice.objects.get_or_create_invoice_with_other_money_amount(invoice_uid, money_amount)
            payment.invoice.account.add(payment.invoice.money_amount_without_percent)
        except ObjectDoesNotExist:
            #TODO: переделать на нормальное логирование
            mail_admins('Unprocessed payment without invoice!',
                                        'Payment NO is %s.' % self.cleaned_data['LMI_PAYMENT_NO'],
                                        fail_silently=True)
            payment.invoice = Invoice.objects.create(
                account=Account.objects.get(uid=0),
                money_amount=Money(money_amount, payee_purse.currency)
            )
        payment.money_amount = money_amount
        payment.payee_purse = payee_purse
        payment.is_OK = ResultResponsePayment.OK_STATUS.SUCCESS
        payment.save()
        return payment




