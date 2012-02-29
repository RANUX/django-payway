# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from payway.utils.tests.base import BaseViewTestCase

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class AccountsListViewTestCase(BaseViewTestCase):
    _url = "{0}".format(reverse("accounts_list"))

    def setUp(self):
        self.create_new_user_with_account()

    def test_contains_account(self):
        response = self.client.get(self._url)
        self.assertContainsTextItems(response, [self.account.uid, self.account.get_balance().amount])

    def test_get(self):
        self.assert_url_available()