# -*- coding: UTF-8 -*-
from decimal import Decimal
from simptools.decorators import catch_and_log_exception
import tornado
import tornado.options
import logging
from hashlib import md5
from payway.qiwi.soap.client import QiwiSoapClient
from tornadows import soaphandler, webservices, complextypes
from tornadows.soaphandler import webservice
from payway.accounts.models import Invoice
from payway.qiwi.models import TERMINATION_CODES, Bill
from conf.settings import QIWI_LOGIN, QIWI_PASSWORD
from payway.qiwi.conf.settings import QIWI_SOAP_SERVER_PORT, QIWI_SOAP_SERVER_CONF


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class UpdateBillService(object):

    @catch_and_log_exception(return_expression=TERMINATION_CODES.UNKNOWN_ERROR)
    def update_bill(self, login, password, txn, status):
        result = TERMINATION_CODES.UNKNOWN_ERROR
        if self.is_authenticated(login, password, txn):
            bill_data = self.check_bill(txn)
            invoice = Invoice.objects.get_or_create_invoice_with_other_money_amount(txn, bill_data['amount'])
            if invoice and bill_data:
                if Bill.STATUS.PAYED == bill_data['status']:
                    bill = Bill.objects.create(
                        invoice=invoice,
                        is_OK=True,
                        money_amount=Decimal(bill_data['amount']),
                        status=bill_data['status'],
                        user=bill_data['user'],
                        date=bill_data['date'],
                        lifetime=bill_data['lifetime']
                    )
                    bill.invoice.account.add(invoice.money_amount_without_percent)
                    result = TERMINATION_CODES.SUCCESS
                else:
                    Bill.objects.create(
                        invoice=invoice,
                        money_amount=Decimal(bill_data['amount']),
                        status=bill_data['status'],
                        user=bill_data['user'],
                        date=bill_data['date'],
                        lifetime=bill_data['lifetime']
                    )
                    result = TERMINATION_CODES.SUCCESS
        else:
            logging.info("Wrong login, password or txn")
        return result

    @classmethod
    def is_authenticated(cls, login, password, txn):
        return cls.check_login(login) and cls.check_password(password, txn)

    def check_bill(self, txn):
        return QiwiSoapClient.checkBill(txn=txn)

    @classmethod
    def check_login(cls, login):
        return login == QIWI_LOGIN

    @classmethod
    def check_password(cls, password, txn):
        secret_key = cls.getSecretKeyByTxn(txn)
        return secret_key == password

    @classmethod
    def getSecretKeyByTxn(cls, txn):
        return md5(
            "{0}{1}".format(txn, md5(QIWI_PASSWORD).hexdigest().upper())
        ).hexdigest().upper()



class updateBill(complextypes.ComplexType):
  login = str
  password = str
  txn = str
  status = int

class updateBillResponse(complextypes.ComplexType):
    updateBillResult = int


class UpdateBillSoapHandler(soaphandler.SoapHandler):

    @webservice(_params=updateBill, _returns=updateBillResponse)
    def updateBill(self, request):
        response = updateBillResponse()
        response.updateBillResult = TERMINATION_CODES.UNKNOWN_ERROR
        response.updateBillResult = UpdateBillService().update_bill(
            login=request.login,
            password=request.password,
            txn=request.txn,
            status=request.status
        )
        return response



def run_qiwi_soap_server():
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(QIWI_SOAP_SERVER_CONF)

    service = [('UpdateBillService', UpdateBillSoapHandler)]
    app = webservices.WebService(service)
    app.listen(QIWI_SOAP_SERVER_PORT)
    logging.info("Starting torando web server on port {0}".format(QIWI_SOAP_SERVER_PORT))
    tornado.ioloop.IOLoop.instance().start()

