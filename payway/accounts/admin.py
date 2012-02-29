# -*- coding: UTF-8 -*-
from django.contrib import admin
from payway.accounts.models import Account, Transaction, Invoice

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'uid',
        'currency_code',
        'user',
    )

class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'uid',
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction)
admin.site.register(Invoice, InvoiceAdmin)