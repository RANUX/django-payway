# -*- coding: UTF-8 -*-
from django.conf import settings

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


TRANSACTIONS_PER_PAGE = getattr(settings, 'TRANSACTIONS_PER_PAGE', 10)
INVOICES_PER_PAGE = getattr(settings, 'INVOICES_PER_PAGE', 5)
ACCOUNTS_PER_PAGE = getattr(settings, 'ACCOUNTS_PER_PAGE', 5)
ADD_MONEY_INITIAL_SUM = getattr(settings, 'ADD_MONEY_INITIAL_SUM', 10)