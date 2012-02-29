# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from moneyed.classes import Money
from payway.merchants.models import Merchant
from payway.orders.models import Order
from payway.orders.tests import mocks
from payway.utils.tests.base import BaseViewTestCase

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class OrderPaymentViewTestCase(BaseViewTestCase):
    fixtures = [
        "payway_accounts_auth.json",
        "payway_accounts_accounts.json",
        "payway_merchants_merchants.json",
        "payway_orders_orders.json",
    ]

    def setUp(self):
        self.create_new_user_with_account()
        self.order = Order(
            uid=1234,
            sum=Money(10, self.account.currency),
            description=u"Тестовый товар",
        )
        self.merchant = Merchant.objects.get(uid=972855239)
        self.merchant_account = self.merchant.user.accounts.get(uid=1111132330)
        self.GET = self.POST = {
            'uid': self.order.uid,
            'sum': self.order.sum.amount,
            'merchant_uid': self.merchant.uid,
            'merchant_account': self.merchant_account.uid,
            'description': self.order.description,
        }
        self.POST.setdefault('account', self.account.uid)

    def test_get(self):
        response = self.client.get(reverse('orders_payment'), self.GET)
        self.failUnlessEqual(response.status_code, 200)
        self.assertContainsTextItems(response, self.GET.values() + ['Pay order'])

    def test_order_exists(self):
        self.GET['uid'] = 1
        response = self.client.get(reverse('orders_payment'), self.GET)
        self.failUnlessEqual(response.status_code, 200)
        self.assertContainsTextItems(response, self.GET.values() + ['Order is paid'])

    def test_success_order_payment(self):
        mocks.mock_MerchantHttpClient_success_execute()

        initial_balance = self.account.get_balance()
        merchant_init_balance = self.merchant_account.get_balance()

        response = self.client.post(reverse('orders_payment'), self.POST)

        self.failUnlessEqual(response.status_code, 200)
        self.assertContainsTextItems(response, self.POST.values() + [dict(Order.PAYMENT_STATUS).get(Order.PAYMENT_STATUS.PAID)])
        self.assertTrue(Order.objects.get(uid=self.order.uid).is_paid)
        self.assert_balance_decreased(initial_balance)

        # merchant balance should be increased
        self.assertEquals(merchant_init_balance + self.order.sum, self.merchant_account.get_balance())

        # test if already paid
        initial_balance = self.account.get_balance()
        response = self.client.post(reverse('orders_payment'), self.POST)

        self.assertContainsTextItems(response, self.POST.values() + [dict(Order.PAYMENT_STATUS).get(Order.PAYMENT_STATUS.PAID)])
        self.assert_balance_should_be_same(initial_balance)

        mocks.set_back_MerchantHttpClient_execute()

    def test_fail_order_payment(self):
        initial_balance = self.account.get_balance()

        response = self.client.post(reverse('orders_payment'), self.POST)

        self.failUnlessEqual(response.status_code, 200)
        self.assertContainsTextItems(response, self.POST.values())
        self.assertFalse(Order.objects.get(uid=self.order.uid).is_paid)
        self.assert_balance_should_be_same(initial_balance)

    def assert_balance_decreased(self, initial_balance):
        self.assertEquals(initial_balance - self.order.sum, self.account.get_balance())

    def assert_balance_should_be_same(self, initial_balance):
        self.assertEquals(initial_balance, self.account.get_balance())
