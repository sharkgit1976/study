# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
import logging

logger = logging.getLogger('django')
logger.info('brilliance')
from oms_web import settings

# Create your views here.
class ChELK(View):
    def get(self, request):
        logger.info(request.GET)
        return render(request, 'elk.html')
