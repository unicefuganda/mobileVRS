from celery.task import Task, task
from celery.registry import tasks

from poll.models import ResponseCategory, Poll, Response
from django.db import transaction
from django.db import IntegrityError

from django.test.client import Client
from mobilevrs.models import *
from django.conf import settings
from mobilevrs.utils import get_summary_dict, get_session_data_turples
import urllib2, urllib


def forward_to_utl(session,**kwargs):
    print 'forwarding...'
    if session.navigations.order_by('date')[0].response=='1':
        collected_data = get_summary_dict(session, settings.UTL_BIRTH_DICT, 'NEWBIRTH')
        result = urllib2.urlopen('http://www.mobilevrs.co.ug/ussd/notify.php?%s' % urllib.urlencode(collected_data))
        return result
    elif session.navigations.order_by('date')[0].response=='2':
        collected_data = get_summary_dict(session, settings.UTL_DEATH_DICT, 'NEWDEATH')
        result = urllib2.urlopen('http://www.mobilevrs.co.ug/ussd/notify.php?%s' % urllib.urlencode(collected_data))
        return result







