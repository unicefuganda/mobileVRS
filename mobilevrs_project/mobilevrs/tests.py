from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
import datetime
import urllib

class ViewTest(TestCase):

    def setUp(self):
        self.transactionId = '123344'
        self.transactionTime = datetime.datetime.now().strftime('%Y%m%dT%H:%M:%S')
        self.msisdn = '256772698723'
        self.ussdServiceCode = '130'
        self.ussdRequestString = ''
        self.response = False
        
    def testUSSDRequest(self):
        client = Client()
        response = client.post('/ussd/', {'transactionId': self.transactionId,\
                                    'transactionTime': self.transactionTime,\
                                    'msisdn': self.msisdn,\
                                    'ussdServiceCode': self.ussdServiceCode,\
                                    'ussdRequestString': self.ussdRequestString,\
                                    'response':self.response
                                    })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'responseString=1.%20Notify%20Birth%0A2.%20Notify%20Death%0A3.%20Edit%20Record%0A4.%20User%20Management&action=request')
