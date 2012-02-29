# -*- coding: UTF-8 -*-
from django_simptools.tests import AuthorizedViewTestCase
from django.core.urlresolvers import reverse


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

COMMON_FIXTURES = [
    "payway_accounts_auth.json",
    "payway_accounts_accounts.json",
    "qiwi.json",
    ]

class QiwiViewTestCase(AuthorizedViewTestCase):
    fixtures = COMMON_FIXTURES

    def test_add_money(self):
        url = reverse("qiwi_add_money", kwargs={"invoice_uid": "1961380063"})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        request_params_names = ['txn_id', 'from', 'to', 'summ', 'com', 'lifetime', 'check_agt']
        self.assertContainsTextItems(response, request_params_names)