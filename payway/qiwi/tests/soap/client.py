# -*- coding: UTF-8 -*-
from time import sleep
from django.test import TestCase
from payway.qiwi.conf.settings import QIWI_BILL_LIFETIME
from payway.qiwi.models import TERMINATION_CODES, Bill

from payway.qiwi.soap.client import QiwiSoapClient
from payway.qiwi.tests.mock_provider import MockQiwiProviderRunner, RECEIVED_DATA, BILLING_DATE



__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class QiwiSoapClientTestCase(TestCase):
    mock_qiwi_provider = None

    @classmethod
    def setUpClass(cls):
        cls.mock_qiwi_provider = MockQiwiProviderRunner()
        cls.mock_qiwi_provider.start()
        sleep(0.5)

    @property
    def bill_data(self):
        return {
            'user': '1111111111',
            'amount': 200.00,
            'comment': 'comment',
            'txn': '1234'
        }

    def test_createBill(self):
        self.assertEquals(TERMINATION_CODES.SUCCESS, self.createBill())
        self.assertDictContainsSubset(self.bill_data, RECEIVED_DATA['createBill'])


    def createBill(self):
        QiwiSoapClient.url = 'http://127.0.0.1:{0}/createBill?wsdl'.format(MockQiwiProviderRunner.PORT)
        return QiwiSoapClient.createBill(**self.bill_data)


    def test_cancelBill(self):

        QiwiSoapClient.url = 'http://127.0.0.1:{0}/cancelBill?wsdl'.format(MockQiwiProviderRunner.PORT)
        response = QiwiSoapClient.cancelBill(txn=self.bill_data['txn'])
        self.assertEquals(TERMINATION_CODES.SUCCESS, response)
        self.assertEquals(self.bill_data['txn'], RECEIVED_DATA['cancelBill']['txn'])

    def test_checkBill(self):
        self.createBill()
        QiwiSoapClient.url = 'http://127.0.0.1:{0}/checkBill?wsdl'.format(MockQiwiProviderRunner.PORT)
        response_expected = {
            'user': self.bill_data['user'],
            'amount': str(self.bill_data['amount']),
            'date': BILLING_DATE,
            'lifetime': QiwiSoapClient.hours_to_lifetime(QIWI_BILL_LIFETIME),
            'status': Bill.STATUS.MADE
        }
        response = QiwiSoapClient.checkBill(txn=self.bill_data['txn'])
        self.assertDictContainsSubset(response_expected, response)

    @classmethod
    def tearDownClass(cls):
        cls.mock_qiwi_provider.stop()