# -*- coding: UTF-8 -*-
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from payway.accounts.models import CURRENCY_CHOICES

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class AddAccountView(TemplateView):
    template_name = 'accounts/list.html'

    MESSAGES =  {
        'WRONG_CURRENCY':  _('Currency not allowed!'),
    }

    def get(self, request, *args, **kwargs):
        currency = kwargs.get('currency')
        if currency not in dict(CURRENCY_CHOICES).keys():
            messages.warning(request, self.MESSAGES['WRONG_CURRENCY'])
        else:
            request.user.accounts.create(user=request.user, currency=currency)
        return redirect('accounts_list')
