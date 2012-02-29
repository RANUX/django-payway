# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import CookieStorage
from django_simptools.tests import AuthorizedViewTestCase
from moneyed.classes import Money


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'



class BaseViewTestCase(AuthorizedViewTestCase):

    _url = ''

    def create_new_user_with_account(self):
        password = 'abc123'
        self.user = User.objects.create_user(
            'user',
            'user@example.com',
            password,
        )
        self.account = self.user.accounts.create(user=self.user, currency='RUB')
        self.account.add(Money(20, self.account.currency))
        self.client_login(username=self.user.username, password=password)

    def assert_url_available(self):
        response = self.client.get(self._url)
        self.failUnlessEqual(response.status_code, 200)

    def assert_redirects(self, expected_url):
        response = self.client.get(self._url)
        self.assertRedirects(response, expected_url)

    def assert_has_message(self, response, message, level):
        messages_list = CookieStorage(response)._decode(response.cookies['messages'].value)
        self.assertIn(Message(level, message), messages_list)