# -*- coding: utf-8 -*-
import json
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import override_settings
import requests

from .models import Invoice

logger = logging.getLogger(__name__)
PHANTOMJS_CONF = {
            'content': '',
            'renderType': 'pdf',
            'omitBackground': False,
            "renderSettings": {
                'emulateMedia': 'print',
                'pdfOptions': {
                    'format': 'A4',
                    'landscape': False,
                    'preferCSSPageSize': True,
                }
            },
            'requestSettings': {
                'waitInterval': 0
            }
        }


def generate_pdf(invoice: Invoice, domain_name=None, use_https=True):
    if not domain_name:
        domain_name = Site.objects.get(pk=settings.SITE_ID).domain
    context = {'object': invoice, 'invoice': invoice}
    request = HttpRequest()
    request.path = invoice.get_absolute_url()
    request.method = 'GET'
    request.META['SERVER_NAME'] = domain_name
    request.META['SERVER_PORT'] = use_https and 443 or 80
    request.META['HTTP_X_FORWARDED_PROTO'] = use_https and 'https' or 'http'
    with override_settings(ALLOWED_HOSTS=[domain_name]):
        content = render_to_string('invoices/detail.html', context=context, request=request)
    phantomjs_conf = PHANTOMJS_CONF.copy()
    phantomjs_conf['content'] = content
    try:
        payload = json.dumps(phantomjs_conf)
        logger.debug(payload)
        response = requests.post(settings.PHANTOMJSCLOUD_API_URL, payload)
        if not response.status_code == 200:
            logger.error(response.text)
            return None
        logger.debug(response.headers())
        return response.content
    except requests.exceptions.RequestException as exc:
        logger.error(exc)
        return None


