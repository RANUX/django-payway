# -*- coding: UTF-8 -*-
from django.conf import settings


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

WEBMONEY_PERCENT = getattr(settings, 'WEBMONEY_PERCENT', 4.0)