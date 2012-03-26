#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
from optparse import OptionParser
from django.core.management import setup_environ
from payway_demo import settings

settings.QIWI_LOGIN = '1111'
settings.QIWI_PASSWORD = '1234'

setup_environ(settings)


from django_nose import NoseTestSuiteRunner

def runtests(*test_args, **kwargs):
    if not test_args:
        test_args = ['payway']

    test_runner = NoseTestSuiteRunner(**kwargs)
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--verbosity', dest='verbosity', action='store', default=1, type=int)
    parser.add_options(NoseTestSuiteRunner.options)
    (options, args) = parser.parse_args()

    runtests(*args, **options.__dict__)