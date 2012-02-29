# -*- coding: UTF-8 -*-
from django.views.generic.base import TemplateView
from django_simptools.shortcuts import create_paginated_page
from payway.orders.conf.settings import ORDERS_PER_PAGE
from payway.orders.models import Order

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class OrderListView(TemplateView):
    template_name = 'orders/list.html'

    def get(self, request, *args, **kwargs):
        orders_page = create_paginated_page(
            query_set=Order.objects.filter(user=request.user).order_by("-id"),
            page_number=request.GET.get('page') or 1,
            objects_per_page=ORDERS_PER_PAGE
        )
        return self.render_to_response({'orders_page': orders_page})