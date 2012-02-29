# -*- coding: UTF-8 -*-
from django.db import transaction
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from moneyed.classes import Money
from simptools.wrappers.http import HttpClient
from payway.accounts.models import Account
from payway.merchants.http import MerchantHttpRequest, RESPONSE_STATUS, MerchantHttpClient
from payway.merchants.models import Merchant
from payway.orders.forms import OrderForm
from payway.orders.models import Order

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

class OrderPaymentView(TemplateView):
    template_name = 'orders/payment.html'

    def get(self, request, *args, **kwargs):
        merchant = get_object_or_404(Merchant, uid=request.GET.get('merchant_uid'))
        order = Order.objects.get_or_None(
            merchant=merchant,
            uid=request.GET.get('uid') or -1
        )
        order_form = OrderForm(data=request.GET, accounts=self.get_accounts_list(request))
        return self.render_to_response({
            'order_form': order_form,
            'is_paid': order.is_paid if order else False,
            'success_url': merchant.success_url,
            'fail_url': merchant.fail_url,
        })

    @transaction.commit_on_success
    def post(self, request):
        accounts = self.get_accounts_list(request)
        order_form = OrderForm(data=request.POST, accounts=accounts)

        if order_form.is_valid():
            account = get_object_or_404(Account, user=request.user, uid=order_form.cleaned_data['account'])
            merchant = get_object_or_404(Merchant, uid=order_form.cleaned_data['merchant_uid'])
            merchant_account = get_object_or_404(Account, user=merchant.user, uid=order_form.cleaned_data['merchant_account'])

            order_sum = Money(order_form.cleaned_data['sum'], account.currency)
            order_uid = order_form.cleaned_data['uid']

            if order_sum <= account.get_balance():
                order, created = Order.objects.get_or_create(
                    uid=order_uid,
                    account=account,
                    merchant=merchant,
                    defaults={
                        'uid': order_uid,
                        'account': account,
                        'sum': order_sum,
                        'merchant': merchant,
                        'description': order_form.cleaned_data['description']
                    }
                )
                if not created:
                    order.sum = order_sum

                if not order.is_paid:
                    response = MerchantHttpClient.notify(merchant, order)
                    if RESPONSE_STATUS.OK not in response:
                        order.set_paid(False)
                        messages.error(request, _("Connection error. Merchant couldn't process order! Merchant response ") + response)
                    else:
                        account.transfer(order_sum, merchant_account)
                        order.set_paid(True)
                        messages.info(request, _("Order paid successfully"))

                    order.save()
                    order_form.set_account_field_choices(self.get_accounts_list(request))

                return self.render_to_response({
                    'order_form': order_form,
                    'is_paid': order.is_paid,
                    'success_url': merchant.success_url,
                    'fail_url': merchant.fail_url,
                })

            order_form.set_not_enough_money_error()

        return self.render_to_response({
            'order_form': order_form,
        })

    def get_accounts_list(self, request):
        return get_list_or_404(Account, user=request.user)

