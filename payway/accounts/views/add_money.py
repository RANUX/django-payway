# -*- coding: UTF-8 -*-
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView
from moneyed.classes import Money
from payway.accounts.conf.settings import ADD_MONEY_INITIAL_SUM
from payway.accounts.forms.add_money import AddMoneyForm, PAYMENT_SYSTEM_CHOICES
from payway.accounts.models import Invoice, Account


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class AddMoneyView(TemplateView):
    template_name = 'accounts/add_money.html'

    def get(self, request, *args, **kwargs):

        account_uid = int(kwargs.get('account_uid', -1))
        invoice_uid = int(kwargs.get('invoice_uid', -1))
        account = get_object_or_404(Account, uid=account_uid)

        invoice, created = Invoice.objects.get_or_create(
            uid=invoice_uid,
            account=account,
            defaults={
                'account': account,
                'money_amount': Money(ADD_MONEY_INITIAL_SUM, account.currency)
            }
        )

        context = super(AddMoneyView, self).get_context_data(**kwargs)
        context['add_money_form'] = AddMoneyForm({
            'money_amount': invoice.money_amount_without_percent.amount,
            'payment_system': dict(PAYMENT_SYSTEM_CHOICES).keys()[0],
            'invoice_uid': invoice.uid
        })

        return self.render_to_response(context)

    def post(self, request):
        form = AddMoneyForm(request.POST or None)
        if form.is_valid():
            invoice = get_object_or_404(Invoice, uid=form.cleaned_data.get('invoice_uid'))
            new_money_amount = form.cleaned_data.get('money_amount')
            invoice.money_amount = Money(new_money_amount, invoice.money_amount.currency)
            invoice.save()
            return redirect(form.cleaned_data['payment_system'], invoice_uid=invoice.uid)

        return self.render_to_response({'add_money_form': form})
