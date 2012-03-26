# -*- coding: UTF-8 -*-
import datetime
import logging
from suds.xsd import sxbasic
from suds.client import Client
from payway.qiwi.conf.settings import QIWI_ALARM, QIWI_CREATE, QIWI_SOAP_CLIENT_URL, QIWI_BILL_LIFETIME, QIWI_DATETIME_FORMAT
from payway.qiwi.conf.settings import QIWI_LOGIN, QIWI_PASSWORD, XML_SCHEMA_PATH


logger = logging.getLogger(__name__)

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

sxbasic.Import.bind('http://www.w3.org/2001/XMLSchema', XML_SCHEMA_PATH) # for suds


class QiwiSoapClientException(Exception):
    pass

class QiwiSoapClient(object):
    url = QIWI_SOAP_CLIENT_URL

    @classmethod
    def createBill(cls, login=QIWI_LOGIN, password=QIWI_PASSWORD, user='', amount='', comment='', txn='', lifetime=QIWI_BILL_LIFETIME, alarm=QIWI_ALARM, create=QIWI_CREATE):
        if len(user) > 10: raise QiwiSoapClientException("User phone number should be less than 10")
        client = Client(cls.url)

        response = client.service.createBill(
            login=login,
            password=password,
            user=user,
            amount=amount,
            comment=comment,
            txn=txn,
            lifetime=cls.hours_to_lifetime(lifetime),
            alarm=alarm,
            create=create)
        return response

    @classmethod
    def hours_to_lifetime(cls, days):
        now = datetime.datetime.now()
        now += datetime.timedelta(days=days)
        return now.strftime(QIWI_DATETIME_FORMAT)

    @classmethod
    def cancelBill(cls, login=QIWI_LOGIN, password=QIWI_PASSWORD, txn=''):
        client = Client(cls.url)
        response = client.service.cancelBill(
                    login=login,
                    password=password,
                    txn=txn,
        )
        return response

    @classmethod
    def checkBill(cls, login=QIWI_LOGIN, password=QIWI_PASSWORD, txn=''):
        client = Client(cls.url)
        response = client.service.checkBill(
                    login=login,
                    password=password,
                    txn=txn,
        )
        return response





