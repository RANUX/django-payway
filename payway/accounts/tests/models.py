# -*- coding: UTF-8 -*-
import random
from django.contrib.auth.models import User
from django.test import TestCase
import moneyed
from moneyed.classes import Money
from nose.tools import eq_, raises
from payway.accounts.models import  Account, Transaction, Overdraft, Invoice, ResponsePayment
from simptools.money import round_down


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class BaseTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'user',
            'user@example.com',
            'abc123',
        )
        self.account = Account.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

class AccountTestCase(BaseTestCase):

    _200_RUB = Money(200, moneyed.RUB)
    _0_RUB = Money(0, moneyed.RUB)

    def test_add_money(self):

        self.assertEqual(self.account.transactions.count(), 0)
        self.assertEqual(self._0_RUB, self.account.get_balance())
        self.account.add(self._200_RUB)
        self.assertEqual(self.account.transactions.count(), 1)
        self.assertEqual(self.account.get_balance(), self._200_RUB)


    @raises(ValueError)
    def test_add_wrong_currency(self):
        self.account.add(Money(0, moneyed.USD))

    def test_pass_negative_money_in_add_withdraw_transfer(self):
        money = Money(random.randint(1, 100) * -1, moneyed.RUB)
        self.assertRaises(ValueError, self.account.add, money)
        self.assertRaises(ValueError, self.account.withdraw, money)
        self.assertRaises(ValueError, self.account.transfer, money, self.account)

    def test_float(self):
        money = Money(random.uniform(1, 100), moneyed.RUB)
        self.account.add(money)
        self.assertEquals(round_down(money), self.account.get_balance())

    def test_withdraw_integer(self):
        money = Money(random.randint(1, 100), moneyed.RUB)
        self.account.add(money)
        self.assertEqual(self.account.get_balance(), money)
        self.account.withdraw(money)
        self.assertEqual(self.account.get_balance(), self._0_RUB)

    def test_withdraw_money(self):
        money = self.random_money()
        self.account.add(money)

        balance = self.account.get_balance()
        self.assertTrue(isinstance(balance, Money))
        self.assertEqual(balance, money)

        self.add_and_withdraw_random_money()

        self.account.withdraw(money)
        balance = self.account.get_balance()
        self.assertTrue(isinstance(balance, Money))
        self.assertEqual(balance, self._0_RUB)

    def test_overdraft(self):
        money1 = self.random_money()
        self.account.add(money1)

        money2 = self.random_money(range=(101,200))
        self.assertRaises(Overdraft, self.account.withdraw, money2)
        self.account.withdraw(money2, True)
        self.assertEqual(self.account.get_balance(), money1 - money2)

    def test_transfer_money(self):
        money = self.random_money()
        account_balance = self.account.get_balance()
        self.account.add(money)

        other_account = Account.objects.create(user=self.user)
        self.account.transfer(money, other_account)

        self.assertEquals(account_balance, self.account.get_balance())
        self.assertEqual(other_account.get_balance(), money)

    def add_and_withdraw_random_money(self):
        balance = self.account.get_balance()
        money = self.random_money()
        self.account.add(money)

        expected_balance = balance + money
        self.assertTrue(isinstance(expected_balance, Money))
        self.assertEqual(expected_balance, self.account.get_balance())

        self.account.withdraw(money)


    def random_money(self, range=(1,100)):
        return Money('%.2f' % random.uniform(range[0], range[1]), moneyed.RUB)


class TransactionTestCase(BaseTestCase):

    def setUp(self):
        super(TransactionTestCase, self).setUp()

        self.money = Money(10.0001, moneyed.RUB)
        self.transaction = Transaction.objects.create(account=self.account,
                                       money_amount=self.money)

    def test_save_transaction_value_with_two_places_round_down(self):
        eq_(round_down(self.money), self.transaction.money_amount)


class InvoiceTestCase(BaseTestCase):

    def setUp(self):
        super(InvoiceTestCase, self).setUp()
        self.initial_money_amount = Money(amount=10.45, currency=moneyed.RUB)
        self.invoice = Invoice.objects.create(
            account=self.account,
            money_amount=self.initial_money_amount
        )

    def test_invoice_is_paid(self):
        response = ResponsePayment.objects.create(invoice=Invoice.objects.get(pk=self.invoice.pk),
                                                  is_OK=ResponsePayment.OK_STATUS.SUCCESS,
                                                  money_amount=self.invoice.money_amount.amount)

        self.assertIn(response, self.invoice.get_success_response_payments())
        self.assertEquals(self.invoice.money_amount.amount, response.money_amount)

    def test_update_money_amount_with_percent(self):
        PERCENT = 3.0
        EXPECTED_SUM = Money(10.76, self.invoice.money_amount.currency)

        self.assertEquals(self.invoice.money_amount, self.invoice.money_amount_without_percent)
        self.invoice.update_money_amount_with_percent(PERCENT)

        self.assertEquals(EXPECTED_SUM, self.invoice.money_amount)
        self.assertEquals(self.initial_money_amount, self.invoice.money_amount_without_percent)


