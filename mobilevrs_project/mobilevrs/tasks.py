from celery.task import Task, task
from celery.registry import tasks

from poll.models import ResponseCategory, Poll, Response
from django.db import transaction
from django.db import IntegrityError




@task
def submitt_to_utl(pk,**kwargs):

   pass




