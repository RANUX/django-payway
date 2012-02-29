# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from payway.utils.tests.base import BaseViewTestCase

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class AccountStatementViewTestCase(BaseViewTestCase):

    def setUp(self):
        self.create_new_user_with_account()
        self._url = "{0}".format(reverse("accounts_statement", args=[self.account.uid]))

    def test_get(self):
        self.assert_url_available()

    def test_contains_account(self):
        response = self.client.get(self._url)
        transaction = self.account.transactions.all()[0]
        self.assertContainsTextItems(response, [transaction.id, transaction.money_amount.amount])