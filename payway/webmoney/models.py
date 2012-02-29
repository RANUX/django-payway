# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from moneyed.classes import CURRENCIES
from payway.accounts.models import ResponsePayment


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

CURRENCY_CHOICES = [(CURRENCIES['RUB'].code, CURRENCIES['RUB'].name)]

class Purse(models.Model):
    purse = models.CharField(_('purse'), max_length=13, unique=True)
    secret_key = models.CharField(_('secret key'), max_length=50)
    is_active = models.BooleanField(_('is active'), default=False)
    currency = models.CharField(_('currency'), max_length=3, choices=CURRENCY_CHOICES)

    def __unicode__(self):
        return '%s' % self.purse


class ResultResponsePayment(ResponsePayment):
    payment_system = _('Webmoney')

    PAYMENT_MODE = Choices((0, _('real')), (1, _('test')))

    LMI_MODE = models.PositiveSmallIntegerField(choices=PAYMENT_MODE)
    payee_purse =  models.ForeignKey(Purse, related_name='success_payments')

    LMI_SYS_INVS_NO = models.PositiveIntegerField()
    LMI_SYS_TRANS_NO = models.PositiveIntegerField()
    LMI_SYS_TRANS_DATE = models.DateTimeField()
    LMI_PAYMENT_NO = models.PositiveIntegerField()

    LMI_PAYER_PURSE = models.CharField(max_length=13)
    LMI_PAYER_WM = models.CharField(max_length=12)
    LMI_HASH = models.CharField(max_length=255)

    LMI_CAPITALLER_WMID = models.CharField(max_length=12, blank=True)
    LMI_WMCHECK_NUMBER = models.CharField(max_length=20, blank=True)
    LMI_PAYMER_NUMBER = models.CharField(max_length=30, blank=True)
    LMI_PAYMER_EMAIL = models.EmailField(blank=True)
    LMI_TELEPAT_PHONENUMBER = models.CharField(max_length=30, blank=True)
    LMI_TELEPAT_ORDERID = models.CharField(max_length=30, blank=True)
    LMI_PAYMENT_DESC = models.CharField(max_length=255, blank=True)
    LMI_LANG = models.CharField(max_length=10, blank=True)

    
