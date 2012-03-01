# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from payway.accounts.models import ResponsePayment


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

TERMINATION_CODES = Choices(
    (0, 'SUCCESS',_('0 Success')),
    (13, 'SERVER_IS_BUSY', _('13 Server is busy, please repeat your request later')),
    (150, 'AUTHORIZATION_ERROR', _('150 Authorization error (wrong login/password)  ')),
    (210, 'BILL_NOT_FOUND', _('210 Bill not found')),
    (215, 'BILL_TXNID_EXISTS', _('215 Bill with this txn-id already exists')),
    (241, 'BILL_VERY_SMALL_SUM', _('241 Very small bill sum')),
    (242, 'BILL_MAXIMUM_SUM_EXCEEDED', _('242 Bill maximum sum exceeded')),
    (278, 'BILL_LIST_MAX_TIME_RANGE_EXCEEDED', _('278 Bill list maximum time range exceeded')),
    (298, 'NO_SUCH_AGENT', _('298 No such agent in the system')),
    (300, 'UNKNOWN_ERROR', _('300 Unknown error')),
    (330, 'ENCRYPTION_ERROR', _('330 Encryption error')),
    (370, 'MAXIMUM_REQUEST_OVERLIMIT', _('370 Maximum allowed concurrent requests overlimit'))
)


class Bill(ResponsePayment):


    STATUS = Choices(
        (50, 'MADE', _('50 Made')),
        (52, 'PROCESSING', _('52 Processing')),
        (60, 'PAYED', _('60 Paid')),
        (150, 'TERMINAL_ERROR', _('150 Cancelled (Terminal error)')),
        (151, 'MACHINE_ERROR', _('151 Cancelled (authorization error, declined, not enough money on account or something else)')),
        (160, 'CANCELLED', _('160 Cancelled')),
        (161, 'TIMEOUT', _('161 Cancelled (Timeout)')),
    )
    payment_system = _('Qiwi Wallet')
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS)
    user = models.CharField(_('User phone number'), max_length=10)
    date = models.CharField(_('Billing date'), max_length=20)
    lifetime = models.CharField(_('Bill lifetime'), max_length=20)

    class Meta:
        verbose_name = _('bill')
        verbose_name_plural = _('bills')
        db_table = 'payway_qiwi_bill'

