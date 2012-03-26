# -*- coding: UTF-8 -*-
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.unittest.case import skip
from mock import Mock
import suds
from payway.accounts.models import Invoice, Account
from payway.qiwi.conf.settings import QIWI_SOAP_SERVER_PORT, QIWI_BILL_LIFETIME
from payway.qiwi.models import TERMINATION_CODES, Bill
from payway.qiwi.soap.client import QiwiSoapClient
from payway.qiwi.soap.server import UpdateBillService
from payway.qiwi.conf.settings import QIWI_LOGIN


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

COMMON_FIXTURES = [
    "payway_accounts_auth.json",
    "payway_accounts_accounts.json",
]


class UpdateBillServiceTestCase(TestCase):
    fixtures = COMMON_FIXTURES
    server_process = None

    def setUp(self):
        self.user = User.objects.get(username="admin")

        self.account = Account.objects.filter(user=self.user)[0]
        self.balance_before = self.account.get_balance()

        self.bills_count = Bill.objects.count()
        self.invoice = Invoice.objects.get(pk=1)

    @skip("to run this test run: bin/manage.py run_qiwi_soap_server")
    def test_service_is_starting(self):
        url = 'http://127.0.0.1:{0}/UpdateBillService?wsdl'.format(QIWI_SOAP_SERVER_PORT)
        client = suds.client.Client(url,cache=None) # if server be late
        result = client.service.updateBill(login=QIWI_LOGIN, password='E54A03A622273FA4EC345D43AAB6F5AE', txn='1111', status=60)
        self.assertEquals(TERMINATION_CODES.UNKNOWN_ERROR, result)

    def test_update_payed_bill(self):

        result = self.update_bill()
        self.assertEquals(TERMINATION_CODES.SUCCESS, result)

        self.assert_bill_should_be_saved()
        self.assert_balance_should_be_increased()

        # try once more
        result = self.update_bill()
        self.assertEquals(TERMINATION_CODES.SUCCESS, result)

    def test_update_payed_bill_with_other_money_amount(self):
        amount = Decimal('100.00')
        result = self.update_bill(amount=amount)
        self.assertEquals(TERMINATION_CODES.SUCCESS, result)
        self.assert_bill_should_be_saved()
        self.assert_balance_should_be_increased()

        # wrong amount should be saved in bill
        self.assertEquals(amount, Bill.objects.all().order_by('-id')[0].money_amount)

    def test_update_bill_with_nonexistent_invoice(self):
        amount = '100.00'
        result = self.update_bill(amount=amount, txn='12345')
        self.assertEquals(TERMINATION_CODES.UNKNOWN_ERROR, result)


    def test_update_cancelled_bill(self):

        result = self.update_bill(status=Bill.STATUS.CANCELLED)
        self.assertEquals(TERMINATION_CODES.SUCCESS, result)

        self.assert_bill_should_be_saved()

        last_bill = Bill.objects.all().order_by('-pk')[0]

        self.assertEquals(Bill.STATUS.CANCELLED, last_bill.status)
        self.assertFalse(last_bill.is_OK)

        # balance should be same
        self.assertEquals(self.balance_before, self.account.get_balance())

    def test_invoice_doesnt_exists(self):
        result = self.update_bill(txn=1234, status=Bill.STATUS.PAYED)
        self.assertEquals(TERMINATION_CODES.UNKNOWN_ERROR, result)

    def update_bill(self, login=QIWI_LOGIN, password='F29C5B73B3D6126A8AB7F6F42058E06C', txn=None, status=Bill.STATUS.PAYED, amount=None):
        service = UpdateBillService()
        check_bill_mock = Mock()
        BILLING_DATE='10.01.2012 13:00:00'
        check_bill_mock.return_value = {
            'user': '1234567890',
            'amount': amount if amount else self.invoice.money_amount.amount,
            'date': BILLING_DATE,
            'lifetime': QiwiSoapClient.hours_to_lifetime(QIWI_BILL_LIFETIME),
            'status': status
        }
        service.check_bill = check_bill_mock

        return service.update_bill(
            login=login,
            password=password,
            txn=txn if txn else self.invoice.uid,
            status=status
        )

    def assert_bill_should_be_saved(self):
        self.assertEquals(self.bills_count + 1, Bill.objects.count())

    def assert_balance_should_be_increased(self):
        self.assertEquals(self.balance_before + self.invoice.money_amount_without_percent, self.account.get_balance())
