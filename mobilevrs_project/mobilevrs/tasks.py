from celery.task import Task, task
from celery.registry import tasks

from poll.models import ResponseCategory, Poll, Response
from django.db import transaction
from django.db import IntegrityError

from django.test.client import Client
from mobilevrs.models import *
from django.conf import settings
from mobilevrs.utils import get_summary_dict


def forward_to_utl(session,**kwargs):
   client = Client()
   if session.navigations.all()[0].response=='1':
       collected_data = get_summary_dict(session, settings.UTL_BIRTH_DICT, 'NEWBIRTH')
       response = client.post("http://www.mobilevrs.co.ug", collected_data)
   elif session.navigations.all()[0].response=='2':
       collected_data = get_summary_dict(session, settings.UTL_DEATH_DICT, 'NEWDEATH')
       response = client.post("http://www.mobilevrs.co.ug", collected_data)







