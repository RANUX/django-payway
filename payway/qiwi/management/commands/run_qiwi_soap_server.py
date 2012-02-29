# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from payway.qiwi.soap.server import run_qiwi_soap_server


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        run_qiwi_soap_server()

