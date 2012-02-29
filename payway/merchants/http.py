# -*- coding: UTF-8 -*-
import logging
from model_utils import Choices
from simptools.wrappers.http import HttpClient, HttpRequest
from requests.exceptions import ConnectionError
from payway.merchants.models import Merchant

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'

RESPONSE_STATUS = Choices(
    ('OK', 'OK'),
)

class MerchantHttpRequest(HttpRequest):

    def __init__(self, merchant, order):
        self.merchant = merchant
        self.order = order

        if self.merchant.result_url_method == Merchant.URL_METHODS.GET:
            self.__set_GET()
        else:
            self.__set_POST()

    def __set_POST(self, *args, **kwargs):
        self.POST = self.__request()

    def __set_GET(self, *args, **kwargs):
        self.GET = self.__request()

    def __request(self):
        return {
            'url': self.merchant.result_url,
            'data': {
                'uid': self.order.uid,
                'is_paid': self.order.is_paid,
                'sum': self.order.sum.amount,
                'sum_currency': self.order.sum_currency,
                'description': self.order.description,
            }
        }

class MerchantHttpClient(HttpClient):

    @classmethod
    def notify(cls, merchant, order):
        result = ''
        try:
            request = MerchantHttpRequest(merchant, order)
            response = cls.execute(request)
            result = response.text
        except ConnectionError:
            logging.warn('Problems when connecting to merchant {0}'.format(merchant.result_url))
        return result
