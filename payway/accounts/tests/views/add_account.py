# -*- coding: UTF-8 -*-
from django.contrib.messages import constants
from django.core.urlresolvers import reverse
from payway.accounts.views.add_account import AddAccountView
from payway.utils.tests.base import BaseViewTestCase

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class AddAccountViewTests(BaseViewTestCase):

    def setUp(self):
        self.create_new_user_with_account()
        self._url = reverse("accounts_add_account", args=['RUB'])

    def test_get(self):
        accounts_count = self.user.accounts.count()
        self.assert_redirects(reverse('accounts_list'))
        self.assertEquals(accounts_count+1, self.user.accounts.count())

    def test_get_with_wrong_currency(self):
        url = reverse("accounts_add_account", args=['XXX'])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('accounts_list'))

        self.assert_has_message(
            response,
            message=AddAccountView.MESSAGES['WRONG_CURRENCY'],
            level=constants.WARNING
        )

