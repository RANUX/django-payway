# -*- coding: UTF-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django_simptools.shortcuts import create_paginated_page
from payway.accounts.conf.settings import INVOICES_PER_PAGE
from payway.accounts.models import Account

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class InvoicesListListView(TemplateView):
    template_name = 'accounts/invoices_list.html'


    def get(self, request, *args, **kwargs):
        account_uid = int(kwargs.get('account_uid', -1))
        account = get_object_or_404(Account, uid=account_uid)

        invoices_page = create_paginated_page(
            query_set=account.invoices.all().order_by('-created'),
            page_number=request.GET.get('page') or 1,
            objects_per_page=INVOICES_PER_PAGE
        )
        return self.render_to_response({'invoices_page': invoices_page})
