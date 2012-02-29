# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from moneyed.classes import Money, RUB
from django_simptools.tests import AuthorizedViewTestCase
from payway.accounts.models import Account
from payway.webmoney.models import ResultResponsePayment


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


COMMON_FIXTURES = [
    "payway_accounts_auth.json",
    "payway_accounts_accounts.json",
    "payway_accounts_initial_data.json",
    "payway_webmoney_webmoney.json",
]

class WebmoneyViewTestCase(AuthorizedViewTestCase):
    fixtures = COMMON_FIXTURES

    def test_add_money(self):
        url = reverse("webmoney_add_money", kwargs={"invoice_uid": "1961380063"})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'LMI_')

class WebmoneyResultViewTestCase(TestCase):
    fixtures = COMMON_FIXTURES

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.payment_amount = Money('12.00', RUB)

        self.data = {
            u'LMI_PAYMENT_DESC': u'{0} payment for 1961380063 invoice'.format(self.user.username),
            u'LMI_MODE': u'1',
            u'LMI_PAYMENT_AMOUNT': u'{0}'.format(self.payment_amount.amount),
            u'LMI_LANG': u'ru-RU',
            u'LMI_PAYMENT_NO': u'1961380063',
            u'LMI_PAYER_PURSE': u'R172474141621',
            u'LMI_SYS_TRANS_DATE': u'20111219 15:20:35',
            u'LMI_HASH': u'D10F83D1EF3FBCC959DDAC59170A0B89',
            u'LMI_PAYER_WM': u'326319216579',
            u'LMI_PAYEE_PURSE': u'R834617269654',
            u'LMI_SYS_INVS_NO': u'798',
            u'LMI_DBLCHK': u'SMS',
            u'LMI_SYS_TRANS_NO': u'315',
            u'LMI_TELEPAT_PHONENUMBER': u'',
            u'LMI_PAYMER_NUMBER': u'',
            u'LMI_CAPITALLER_WMID': u'',
            u'LMI_PAYMER_EMAIL': u'',
            u'LMI_TELEPAT_ORDERID': u'',
        }

    def test_prerequest(self):
        prerequest_data = {
            u'LMI_PREREQUEST': u'1',
            u'LMI_PAYMENT_DESC': u'admin payment for 1961380063 invoice',
            u'LMI_MODE': u'1',
            u'LMI_PAYMENT_AMOUNT': u'1.00',
            u'LMI_LANG': u'ru-RU',
            u'LMI_PAYMENT_NO': u'1961380063',
            u'LMI_PAYER_PURSE': u'R172474141621',
            u'LMI_PAYER_WM': u'326319216579',
            u'LMI_PAYEE_PURSE': u'R834617269654',
            u'LMI_DBLCHK': u'SMS'
        }
        url = reverse('webmoney_result')
        response = self.client.post(url, prerequest_data)
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "YES")



    def test_result_response(self):
        success_payments_count = ResultResponsePayment.objects.count()
        account = Account.objects.filter(user=self.user)[0]
        balance_before = account.get_balance()

        url = reverse('webmoney_result')
        response = self.client.post(url, self.data)
        self.failUnlessEqual(response.status_code, 200)

        # payment response should be saved
        self.assertEquals(success_payments_count + 1, ResultResponsePayment.objects.count())

        # account balance should be increased
        self.assertEquals(balance_before + self.payment_amount, account.get_balance())

        self.assertContains(response, "OK")

    def test_process_payment_without_invoice(self):
        unknown_payment_no = u'1111'
        self.data['LMI_PAYMENT_NO'] = unknown_payment_no
        self.data['LMI_HASH'] = u'B9BE805ABE27425660139B3DC8AD71F6'

        zero_account = Account.objects.get(uid=0)
        invoices_count_before = zero_account.invoices.count()

        url = reverse('webmoney_result')
        response = self.client.post(url, self.data)
        self.failUnlessEqual(response.status_code, 200)

        # new invoice should be created
        self.assertEquals(invoices_count_before + 1, zero_account.invoices.count())

        # payment response should be saved
        self.assertIsNotNone(ResultResponsePayment.objects.get(LMI_PAYMENT_NO=unknown_payment_no))
        self.assert_mail_sent()

    def assert_mail_sent(self):
        from django.core.mail import outbox
        self.assertIsNotNone(outbox[0])

class WebmoneyFailAndSuccessViewTestCases(AuthorizedViewTestCase):
    fixtures = COMMON_FIXTURES

    def setUp(self):
        self.data = {
                    u'LMI_SYS_TRANS_DATE': u'20111220 16:02:57',
                    u'LMI_LANG': u'ru-RU',
                    u'LMI_PAYMENT_NO': u'14471981',
                    u'LMI_SYS_INVS_NO': u'308',
                    u'LMI_SYS_TRANS_NO': u'694'
                }
        self.client_login()

    def test_success_payment(self):
        url = reverse('webmoney_success')
        response = self.client.post(url, self.data)
        self.assertContainsPaymentNoAndDate(response)

    def test_fail_payment(self):
            url = reverse('webmoney_fail')
            response = self.client.post(url, self.data)
            self.assertContainsPaymentNoAndDate(response)

    def assertContainsPaymentNoAndDate(self, response):
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, self.data['LMI_PAYMENT_NO'])

