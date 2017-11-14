# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from oms_web import settings

group_name = 'TELLERCHDB'

set_dir = getattr(settings, 'VERSINO_{}_SOURCE'.format(group_name))

print(set_dir)