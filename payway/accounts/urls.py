# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from payway.accounts.views.add_account import AddAccountView
from payway.accounts.views.add_money import AddMoneyView
from payway.accounts.views.invoices_list import InvoicesListListView
from payway.accounts.views.list import AccountsListView
from payway.accounts.views.statement import AccountStatementView


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


urlpatterns = patterns('',
    url(r'^add-money/(?P<account_uid>\d+)/(?P<invoice_uid>\d+)$', login_required(AddMoneyView.as_view()), name='accounts_add_money'),
    url(r'^add-money/(?P<account_uid>\d+)/$', login_required(AddMoneyView.as_view()), name='accounts_add_money'),
    url(r'^add-money/$', login_required(AddMoneyView.as_view()), name='accounts_add_money'),
    url(r'^add-account/currency/(?P<currency>\w{3})$', login_required(AddAccountView.as_view()), name='accounts_add_account'),
    url(r'^list/$', login_required(AccountsListView.as_view()), name='accounts_list'),
    url(r'^statement/(?P<account_uid>\d+)/$', login_required(AccountStatementView.as_view()), name='accounts_statement'),
    url(r'^invoices/(?P<account_uid>\d+)/$', login_required(InvoicesListListView.as_view()), name='accounts_invoices'),
)