# -*- coding: UTF-8 -*-
from payway.webmoney.conf.settings import WEBMONEY_PERCENT

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView, View
from payway.accounts.models import Invoice
from payway.webmoney.forms import RequestPaymentForm, PrerequestResponsePaymentForm, ResultResponsePaymentForm
from payway.webmoney.models import Purse

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class WebmoneyView(TemplateView):
    template_name = 'webmoney/add_money_request.html'

    def get(self, request, *args, **kwargs):
        context = super(WebmoneyView, self).get_context_data(**kwargs)
        invoice_uid = int(kwargs.get('invoice_uid', 0))
        invoice = get_object_or_404(Invoice, uid=invoice_uid)
        invoice.update_money_amount_with_percent(WEBMONEY_PERCENT)

        try:
            context['request_form'] = RequestPaymentForm(initial={'LMI_PAYMENT_AMOUNT': invoice.money_amount.amount,
                                                                  'LMI_PAYMENT_NO': invoice.uid,
                                                                  'LMI_PAYMENT_DESC': render_to_string(
                                                                                  'webmoney/payment_description.txt',
                                                                                  {'invoice_uid': invoice.uid,
                                                                                   'user': request.user}
                                                                              ).strip()[:255],
                                                                  'LMI_PAYEE_PURSE': Purse.objects.filter(is_active=True, currency=invoice.money_amount.currency)[0]
            })
        except IndexError:
            raise Http404("WebMoney purse number doesn't exists")
        return self.render_to_response(context)

class WebmoneyResultView(View):

    def post(self, request, *args, **kwargs):
        form = PrerequestResponsePaymentForm(request.POST)
        if form.is_valid() and form.cleaned_data['LMI_PREREQUEST']:
            invoice_uid = int(form.cleaned_data['LMI_PAYMENT_NO'])
            try:
                Invoice.objects.get(uid=invoice_uid)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest("Invoice with number %s not found." % invoice_uid)
            return HttpResponse("YES")

        form = ResultResponsePaymentForm(request.POST)
        if form.is_valid():
            purse = Purse.objects.get(purse=form.cleaned_data['LMI_PAYEE_PURSE'])

            key = u"{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(
                purse.purse,
                form.cleaned_data['LMI_PAYMENT_AMOUNT'],
                form.cleaned_data['LMI_PAYMENT_NO'],
                form.cleaned_data['LMI_MODE'],
                form.cleaned_data['LMI_SYS_INVS_NO'],
                form.cleaned_data['LMI_SYS_TRANS_NO'],
                form.cleaned_data['LMI_SYS_TRANS_DATE'].strftime('%Y%m%d %H:%M:%S'),
                purse.secret_key,
                form.cleaned_data['LMI_PAYER_PURSE'],
                form.cleaned_data['LMI_PAYER_WM']
            )
            generated_hash = md5(key).hexdigest().upper()
            if generated_hash == form.cleaned_data['LMI_HASH']:
                form.save()
            else:
                #TODO: log to somewhere
                return HttpResponseBadRequest("Incorrect hash")
            return HttpResponse("OK")

        return HttpResponseBadRequest("Unknown error!")


class WebmoneySuccessView(TemplateView):
    template_name = 'webmoney/success.html'

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context(request))

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context(request))

    def get_context(self, request):
        context = super(WebmoneySuccessView, self).get_context_data()
        request_data = request.GET or request.POST
        context['LMI_PAYMENT_NO'] = request_data.get('LMI_PAYMENT_NO')
        return context

class WebmoneyFailView(WebmoneySuccessView):
    template_name = 'webmoney/fail.html'