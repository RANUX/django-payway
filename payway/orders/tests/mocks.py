# -*- coding: UTF-8 -*-
from mock import Mock
from requests.exceptions import ConnectionError
from simptools.wrappers.http import HttpClient
from payway.merchants.http import MerchantHttpClient, RESPONSE_STATUS

__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


def mock_MerchantHttpClient_success_execute():

    class ResponseMock(object):
        text = RESPONSE_STATUS.OK
    MerchantHttpClient.execute = Mock(return_value=ResponseMock())

def mock_MerchantHttpClient_fail_execute():
    mock = Mock()
    mock.side_effect = ConnectionError()
    MerchantHttpClient.execute = mock

def set_back_MerchantHttpClient_execute():
    MerchantHttpClient.execute = HttpClient.execute

