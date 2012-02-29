# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from payway.utils.tests.base import BaseViewTestCase


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class AddMoneyViewTests(BaseViewTestCase):

    def setUp(self):
        self.create_new_user_with_account()
        self._url = "{0}{1}/".format(reverse("accounts_add_money"), self.account.uid)

    def test_get(self):
        self.assert_url_available()


