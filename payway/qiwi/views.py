# -*- coding: UTF-8 -*-
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView
from payway.accounts.models import Invoice
from payway.qiwi.conf.settings import QIWI_BILL_LIFETIME, QIWI_CHECK_AGT, QIWI_PERCENT
from payway.qiwi.forms import RequestPaymentForm
from payway.qiwi.conf.settings import QIWI_LOGIN

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class QiwiView(TemplateView):
    template_name = 'qiwi/add_money_request.html'

    def get(self, request, *args, **kwargs):
        context = super(QiwiView, self).get_context_data(**kwargs)
        invoice_uid = int(kwargs.get('invoice_uid', 0))
        invoice = get_object_or_404(Invoice, uid=invoice_uid)
        invoice.update_money_amount_with_percent(QIWI_PERCENT)

        context['request_form'] = RequestPaymentForm(initial={
            'txn_id': invoice.uid,
            'from': QIWI_LOGIN,
            'summ': invoice.money_amount.amount,
            'com': render_to_string(
                'qiwi/payment_description.txt', {
                    'invoice_uid': invoice.uid,
                    'user': request.user
                }).strip()[:255],
            'lifetime': QIWI_BILL_LIFETIME,
            'check_agt': QIWI_CHECK_AGT
            })

        return self.render_to_response(context)
