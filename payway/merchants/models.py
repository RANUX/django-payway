# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_simptools.models import RandomUIDAbstractModel
from model_utils import Choices


__author__ = 'Razzhivin Alexander'
__email__ = 'admin@httpbots.com'


class Merchant(RandomUIDAbstractModel):

    URL_METHODS = Choices(
        ('POST', 'POST'),
        ('GET',  'GET'),
    )

    user = models.ForeignKey(User, related_name='merchants', verbose_name=_('user'))
    name = models.CharField('Имя', max_length=255)
    secret_key = models.CharField(_('secret key'), max_length=50)

    result_url = models.URLField(_('result url'))
    result_url_method = models.CharField(_('result url method'), max_length=4, choices=URL_METHODS)

    success_url = models.URLField(_('success url'))
    fail_url = models.URLField(_('fail url'))

    class Meta:
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'
        db_table = 'payway_merchants'