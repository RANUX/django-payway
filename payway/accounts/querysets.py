# -*- coding: UTF-8 -*-
import logging
from django.db.models.aggregates import Sum
from django_simptools.querysets import ExtendedQuerySet
from moneyed.classes import Money

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class TransactionQuerySet(ExtendedQuerySet):

    def sum_values(self):
        return self.aggregate(Sum('money_amount'))['money_amount__sum'] or 0.0

class InvoiceQuerySet(ExtendedQuerySet):

    def get_or_create_invoice_with_other_money_amount(self, txn, money_amount):
        invoice = self.get(uid=txn)
        if invoice:
            money_amount = Money(money_amount, invoice.money_amount.currency)
            if invoice.money_amount != money_amount:
                self.__log_different_amount(invoice, invoice.money_amount, money_amount)
                invoice = self.create(
                    account=invoice.account,
                    money_amount=money_amount,
                    money_amount_without_percent=invoice.money_amount_without_percent
                )
        return invoice

    def __log_different_amount(self, invoice, should_be, given):
        if should_be != given:
            logging.warning(u"Got different money amount for {0} invoice. Amount should be {1} but was {2}".format(
                invoice,
                should_be,
                given
            ))