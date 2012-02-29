# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from payway.orders.views.list import OrderListView
from payway.orders.views.payment import OrderPaymentView

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


urlpatterns = patterns('',
    url(r'^payment/$', login_required(csrf_exempt(OrderPaymentView.as_view())), name='orders_payment'),
    url(r'^list/$', login_required(OrderListView.as_view()), name='orders_list'),
    url(r'^test-order/$', TemplateView.as_view(template_name="orders/test_order.html"), name='orders_test_order'),
)