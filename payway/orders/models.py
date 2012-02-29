# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_simptools.money.models import fields
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django_simptools.managers import ChainableQuerySetManager
from django_simptools.querysets import ExtendedQuerySet
from payway.accounts.models import MAX_MONEY_DIGITS, MAX_MONEY_PLACES, Account
from payway.merchants.models import Merchant

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class Order(TimeStampedModel):
    PAYMENT_STATUS = Choices(
        (False, 'NOT_PAID', _('not paid')),
        (True,  'PAID', _('paid')),
    )
    user = models.ForeignKey(User, related_name='orders', verbose_name=_('user'))
    merchant = models.ForeignKey(Merchant, related_name='orders', verbose_name=_('merchant'))
    uid = models.PositiveIntegerField(unique=False, editable=False)
    sum = fields.MoneyField(_('sum'), max_digits=MAX_MONEY_DIGITS, decimal_places=MAX_MONEY_PLACES)
    account = models.ForeignKey(Account, related_name='orders', verbose_name=_('account'))
    description = models.CharField(_('description'), max_length=255, blank=True)
    is_paid = models.BooleanField(_('payment status'), default=False, choices=PAYMENT_STATUS)
    objects = ChainableQuerySetManager(ExtendedQuerySet)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        db_table = 'payway_orders'

    def __init__(self, *args, **kwargs):
        account = kwargs.get('account') or None
        if account:
            kwargs.setdefault('user', account.user)
        super(Order, self).__init__(*args, **kwargs)

    def set_paid(self, is_paid=False):
        self.is_paid = is_paid

    def __unicode__(self):
        return 'Order {0}'.format(self.uid)

