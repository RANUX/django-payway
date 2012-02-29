# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from payway.qiwi.views import QiwiView


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

urlpatterns = patterns('',
    url(r'add-money/(?P<invoice_uid>\d+)/$', login_required(QiwiView.as_view()), name='qiwi_add_money'),
#    url(r'result/$', csrf_exempt(WebmoneyResultView.as_view()), name='webmoney_result'), TODO: доделать
#    url(r'success/$', login_required(csrf_exempt(WebmoneySuccessView.as_view())), name='webmoney_success'),
#    url(r'fail/$', login_required(csrf_exempt(WebmoneyFailView.as_view())), name='webmoney_fail'),
)