from celery.task import Task, task
from celery.registry import tasks

from poll.models import ResponseCategory, Poll, Response
from django.db import transaction
from django.db import IntegrityError

from django.test.client import Client
from mobilevrs.models import *


def submitt_to_utl(session,**kwargs):
   client=Client()
   if session.navigations.all()[0].response=='1':
       d=get_summary_dict(session,UTL_BIRTH_DICT,NEWBIRTH)
       res=client.get("http://www.mobilevrs.co.ug",d)
   elif session.navigations.all()[0].response=='2':
       d=get_summary_dict(session,UTL_DEATH_DICT,NEWDEATH)
       res=client.get("http://www.mobilevrs.co.ug",d)







