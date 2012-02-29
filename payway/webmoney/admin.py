# -*- coding: UTF-8 -*-
from django.contrib import admin
from payway.webmoney.models import Purse, ResultResponsePayment


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

admin.site.register(Purse)
admin.site.register(ResultResponsePayment)