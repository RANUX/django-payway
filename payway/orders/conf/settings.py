# -*- coding: UTF-8 -*-
from django.conf import settings

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


ORDERS_PER_PAGE = getattr(settings, 'ORDERS_PER_PAGE', 10)
ORDER_MIN_SUM = getattr(settings, 'ORDERS_ORDER_MIN_SUM', 5)