# -*- coding: UTF-8 -*-
from django.views.generic.base import TemplateView
from django_simptools.shortcuts import create_paginated_page
from payway.accounts.conf.settings import ACCOUNTS_PER_PAGE
from payway.accounts.models import Account

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

class AccountsListView(TemplateView):
    template_name = 'accounts/list.html'

    def get(self, request):
        accounts_page = create_paginated_page(
            query_set=Account.objects.filter(user=request.user).order_by('-id'),
            page_number=request.GET.get('page') or 1,
            objects_per_page=ACCOUNTS_PER_PAGE
        )
        return self.render_to_response({'accounts_page': accounts_page })