# -*- coding: UTF-8 -*-
from django.test import TestCase
from payway.webmoney.forms import RequestPaymentForm


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class PaymentRequestFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'LMI_PAYEE_PURSE': 'Z123412341234',
            'LMI_PAYMENT_AMOUNT': '999999.99',
            'LMI_PAYMENT_DESC': 'test payment',
            'LMI_PAYMENT_NO': '2147483647',
            'LMI_SIM_MODE': '0',
        }

    def test_valid_payment_request_form(self):
        form = RequestPaymentForm(data=self.valid_data)
        self.failUnless(form.is_valid())





