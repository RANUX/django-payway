# -*- coding: UTF-8 -*-
from model_utils import Choices
from model_utils.models import  TimeStampedModel, InheritanceCastModel
from moneyed import CURRENCIES
import moneyed
from django.db import models
from django.contrib.auth.models import User
from django_simptools.managers import ChainableQuerySetManager
from django_simptools.money.models import fields
from django_simptools.models import RandomUIDAbstractModel
from django.utils.translation import ugettext_lazy as _
from moneyed.classes import Money, get_currency
from payway.accounts.querysets import TransactionQuerySet, InvoiceQuerySet
from simptools.money import round_down


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

MAX_MONEY_PLACES = 2
MAX_MONEY_DIGITS = 20



class Overdraft(Exception):
    pass


CURRENCY_CHOICES = (
    (CURRENCIES['RUB'].code, CURRENCIES['RUB'].name),
    (CURRENCIES['USD'].code, CURRENCIES['USD'].name)
)


class Account(RandomUIDAbstractModel):
    user = models.ForeignKey(User, related_name='accounts', verbose_name=_('user'))
    currency_code = models.CharField(_('currency code'), max_length=3, choices=CURRENCY_CHOICES, default=moneyed.RUB)

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')
        permissions = (('can_view_account_report', 'Can view account report'),)
        db_table = 'payway_accounts'

    @property
    def currency(self):
        currency = None
        if self.currency_code:
            currency = get_currency(self.currency_code)
        return currency

    def __unicode__(self):
        return u"{0} {1}".format(self.uid, self.currency)

    def get_balance(self):
        sum = Transaction.objects.filter(account=self, money_amount_currency=self.currency).sum_values()
        return round_down(Money(sum, self.currency))

    def withdraw(self, money, allow_overdraft=False):
        self.assert_correct_currency(money)

        if money < Money(0, self.currency):
            raise ValueError("You can't withdraw a negative amount")

        if not allow_overdraft and (self.get_balance() - money) < Money(0, self.currency):
            raise Overdraft

        return Transaction.objects.create(
            account=self,
            money_amount=money * '-1.0',
        )

    def add(self, money):
        self.assert_correct_currency(money)

        if money < Money(0, self.currency):
            raise ValueError("You can't add a negative money amount")

        return Transaction.objects.create(
            account=self,
            money_amount=money,
        )

    def transfer(self, money, to_account):
        self.assert_correct_currency(money)

        if money < Money(0, self.currency):
            raise ValueError("You can't transfer a negative money amount")

        self.withdraw(money)

        return Transaction.objects.create(
            account=to_account,
            money_amount=money,
        )

    def assert_correct_currency(self, money):
        if money.currency != self.currency:
            raise ValueError("You can't add money with %s currency. Current currency %s" % (money.currency, self.currency))

class Transaction(TimeStampedModel):
    account = models.ForeignKey(Account, related_name='transactions', verbose_name=_('account'))
    money_amount = fields.MoneyField(_('money amount'), max_digits=MAX_MONEY_DIGITS, decimal_places=MAX_MONEY_PLACES)
    objects = ChainableQuerySetManager(TransactionQuerySet)

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
        db_table = 'payway_transactions'

    def __unicode__(self):
        return 'Transaction #%d (%s)' % (self.id, self.money_amount)

    def save(self, *args, **kwargs):
        self.money_amount = round_down(self.money_amount)
        super(Transaction, self).save(*args, **kwargs)

class Invoice(RandomUIDAbstractModel, TimeStampedModel):

    account = models.ForeignKey(Account, related_name='invoices', verbose_name=_('account'))
    money_amount = fields.MoneyField(_('money amount'), max_digits=MAX_MONEY_DIGITS, decimal_places=MAX_MONEY_PLACES) # for transmit
    money_amount_without_percent = fields.MoneyField(_('money amount without percent'), max_digits=MAX_MONEY_DIGITS, decimal_places=MAX_MONEY_PLACES) # befor transmit
    objects = ChainableQuerySetManager(InvoiceQuerySet)

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        db_table = 'payway_invoices'

    def __init__(self, *args, **kwargs):
        money_amount = kwargs.get('money_amount') or None
        if money_amount:
            kwargs.setdefault('money_amount_without_percent', money_amount)
        super(Invoice, self).__init__(*args, **kwargs)

    def get_success_response_payments(self):
        return self.accounts_responsepayment_related.filter(is_OK=ResponsePayment.OK_STATUS.SUCCESS)

    def __unicode__(self):
        return u'{0}'.format(self.uid)

    def update_money_amount_with_percent(self, percent=0.0):
        self.money_amount_without_percent = self.money_amount
        self.money_amount += round_down(percent % self.money_amount)
        self.save()



class AbstractPayment(TimeStampedModel):
    money_amount = models.DecimalField(max_digits=MAX_MONEY_DIGITS, decimal_places=MAX_MONEY_PLACES, default=0)
    invoice = models.ForeignKey(Invoice, related_name="%(app_label)s_%(class)s_related", verbose_name=_('invoice'))
    payment_system = ''

    class Meta:
        abstract = True


class ResponsePayment(InheritanceCastModel, AbstractPayment):
    """
    Parent response model
    """
    OK_STATUS = Choices((True, 'SUCCESS', _('success')), (False, 'FAIL', _('fail')))

    is_OK = models.BooleanField(choices=OK_STATUS, default=OK_STATUS.FAIL)

    class Meta:
        db_table = 'payway_response_payments'

    def __unicode__(self):
        return u'id:{0} is_ok:{2}'.format(self.id, self.money_amount, self.is_OK)

