# -*- coding: UTF-8 -*-

from django.test import TestCase
from simptools.wrappers.http import HttpClient
from payway.merchants.models import Merchant
from payway.merchants.tests.http.mocks import *

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'



class MerchantHttpClientTestCase(TestCase):
    fixtures = [
        "payway_merchants_merchants.json",
        "payway_orders_orders.json",
    ]

    def setUp(self):
        self.merchant = Merchant.objects.get(uid=972855239)
        self.order = self.merchant.orders.all()[0]

    def tearDown(self):
        set_back_MerchantHttpClient_execute()

    def test_success_notify(self):
        mock_MerchantHttpClient_success_execute()
        response = MerchantHttpClient.notify(self.merchant, self.order)
        self.assertIn(RESPONSE_STATUS.OK, response)

    def test_connection_error(self):
        self.merchant.result_url = 'http://wrong12343434.com'
        mock_MerchantHttpClient_fail_execute()
        response = MerchantHttpClient.notify(self.merchant, self.order)
        self.assertEquals('', response)