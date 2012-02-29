# -*- coding: UTF-8 -*-
from django.conf import settings


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

QIWI_LOGIN = getattr(settings, 'QIWI_LOGIN')
QIWI_PASSWORD = getattr(settings, 'QIWI_PASSWORD')
QIWI_SOAP_SERVER_PORT = getattr(settings, 'QIWI_SOAP_SERVER_PORT', 9090)
QIWI_SOAP_SERVER_CONF = getattr(settings, 'QIWI_SOAP_SERVER_CONF', 'qiwi_server.conf')
QIWI_CREATE  = getattr(settings, 'QIWI_CREATE', False)
QIWI_ALARM  = getattr(settings, 'QIWI_ALARM', 0)
QIWI_BILL_LIFETIME = getattr(settings, 'QIWI_BILL_LIFETIME', 24)  # hours
QIWI_DATETIME_FORMAT = getattr(settings, 'QIWI_DATETIME_FORMAT', '%d.%m.%Y %H:%M:%S')
QIWI_SOAP_CLIENT_URL = getattr(settings, 'QIWI_SOAP_CLIENT_URL', 'https://ishop.qiwi.ru/services/ishop?wsdl')
QIWI_CHECK_AGT = getattr(settings, 'QIWI_CHECK_AGT', False)
QIWI_PERCENT = getattr(settings, 'QIWI_PERCENT', 4.0)