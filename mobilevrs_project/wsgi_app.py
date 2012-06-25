# wsgi_app.py
import sys, os

filedir = os.path.dirname(__file__)
sys.path.append(os.path.join(filedir))

#print sys.path

os.environ["CELERY_LOADER"] = "django"
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import sys
print sys.path

from django.core.handlers.wsgi import WSGIHandler

import django.core.handlers.wsgi
class ForcePostHandler(WSGIHandler):
    """Workaround for: http://lists.unbit.it/pipermail/uwsgi/2011-February/001395.html
    """
    def get_response(self, request):
        request.POST # force reading of POST data
        return super(ForcePostHandler, self).get_response(request)

application = ForcePostHandler()

#application = WSGIHandler()
