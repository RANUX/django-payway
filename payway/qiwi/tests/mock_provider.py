# -*- coding: UTF-8 -*-
import os
import sys
from threading import Thread
import tornado
from tornadows import soaphandler, webservices, complextypes
from tornadows.soaphandler import webservice
from django.core.management import setup_environ

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

sys.path.append(PROJECT_DIR)

try:
    from payway_pps.conf.dev import settings
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find settings module in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

setup_environ(settings)

from payway.qiwi.models import Bill
from payway.qiwi.conf.settings import QIWI_LOGIN, QIWI_PASSWORD


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

class createBill(complextypes.ComplexType):
    login = str
    password = str
    user = str
    amount = str
    comment = str
    txn = str
    lifetime = str
    alarm = int
    create = bool

class createBillResponse(complextypes.ComplexType):
    createBillResult = int

RECEIVED_DATA = {}
BILLING_DATE = '10.01.2012 13:00:00'

class MockCreateBillService(soaphandler.SoapHandler):

    @webservice(_params=createBill, _returns=createBillResponse)
    def createBill(self, request):
        login = request.login
        password = request.password
        user = request.user
        amount = request.amount
        comment = request.comment
        txn = request.txn
        lifetime = request.lifetime
        alarm = request.alarm
        create = request.create

        response = createBillResponse()
        response.createBillResult = 0

        if not all([login==QIWI_LOGIN, password==QIWI_PASSWORD]):
            response.createBillResult = 150
        if len(user) != 10:
            response.createBillResult = 150
        try:
            amount = float(amount)
        except:
            response.createBillResult = 150

        if amount > 15000:
            response.createBillResult = 242

        if alarm not in [0, 1, 2]:
            response.createBillResult = 150

        if create not in [True, False]:
            response.createBillResult = 150

        RECEIVED_DATA['createBill'] = {
                'user': user,
                'amount': amount,
                'comment': comment,
                'txn': txn,
                'lifetime': lifetime,
                'alarm': alarm,
                'create':create,
                'date': BILLING_DATE
        }

        return response

class cancelBill(complextypes.ComplexType):
    login = str
    password = str
    txn = str

class cancelBillResponse(complextypes.ComplexType):
    cancelBillResult = int

class MockCancelBillService(soaphandler.SoapHandler):

    @webservice(_params=cancelBill, _returns=cancelBillResponse)
    def cancelBill(self, request):
        login = request.login
        password = request.password
        txn = request.txn

        response = cancelBillResponse()
        response.cancelBillResult = 0

        if not all([login==QIWI_LOGIN, password==QIWI_PASSWORD]):
                    response.cancelBillResult = 150

        RECEIVED_DATA['cancelBill'] = {
                        'txn': txn
        }
        return response

class checkBill(complextypes.ComplexType):
    login = str
    password = str
    txn = str


class checkBillResponse(complextypes.ComplexType):
    user = str
    amount = str
    date = str
    lifetime = str
    status = int

class MockCheckBillService(soaphandler.SoapHandler):

    @webservice(_params=checkBill, _returns=checkBillResponse)
    def checkBill(self, request):
        login = request.login
        password = request.password

        if not all([login==QIWI_LOGIN, password==QIWI_PASSWORD]):
            raise Exception("incorrect login or password")

        response = checkBillResponse()
        response.user = RECEIVED_DATA['createBill']['user']
        response.amount = RECEIVED_DATA['createBill']['amount']
        response.date = BILLING_DATE
        response.lifetime = RECEIVED_DATA['createBill']['lifetime']
        response.status = Bill.STATUS.MADE
        return response

class MockQiwiProviderRunner(Thread):
    PORT = 18888

    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.services = [
            ('createBill', MockCreateBillService),
            ('cancelBill', MockCancelBillService),
            ('checkBill', MockCheckBillService),
        ]

    def run(self):
        app = webservices.WebService(self.services)
        app.listen(self.PORT)
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        tornado.ioloop.IOLoop.instance().stop()
        self.join()

if __name__ == '__main__':
    MockQiwiProviderRunner().run()