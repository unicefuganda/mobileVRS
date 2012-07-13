from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
import datetime
import urllib2

class ViewTest(TestCase):

    def setUp(self):
        self.transactionId = '123344'
        self.transactionTime = datetime.datetime.now().strftime('%Y%m%dT%H:%M:%S')
        self.msisdn = '256772698723'
        self.ussdServiceCode = '130'
        self.ussdRequestString = ''
        self.response = False
        
    def sendRequest(self, transactionId = None, transactionTime = None, msisdn = None, ussdServiceCode = None, ussdRequestString = None, response = None ):
        client = Client()
        transactionId = self.transactionId if transactionId == None else transactionId
        transactionTime = self.transactionTime if transactionTime == None else transactionTime
        msisdn = self.msisdn if msisdn == None else msisdn
        ussdServiceCode = self.ussdServiceCode if ussdServiceCode == None else ussdServiceCode
        ussdRequestString = self.ussdRequestString if ussdRequestString == None else ussdRequestString
        response = self.response if response == None else response
        
        return client.post('/ussd/', {'transactionId': transactionId,\
                                    'transactionTime': transactionTime,\
                                    'msisdn': msisdn,\
                                    'ussdServiceCode': ussdServiceCode,\
                                    'ussdRequestString': ussdRequestString,\
                                    'response': response
                                    })
        
    def testUSSDRequest(self):
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. User Management\n5. Resume Previous&action=request")
        
    def testBirthNotify(self):
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Child's first name :&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = 'my first guy', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's other name(s):&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = 'the other name', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter date of birth: 1. Today 2. Yesterday  Other (Enter manually in the format ddmmyyyy) &action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Select the sex of the child:\n 1. Male\n 2. Female&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter mother's names:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = 'the mother', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select mother's nationality:1. Uganda 2. Kenya 3. Tanzania 4. Rwanda Others (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter father's names:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = 'the father', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select father's nationality:1. Uganda 2. Kenya 3. Tanzania 4. Rwanda Others (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Summary child first name: my first guy child other name: the other name date of birth: 1 child sex 1 mother nationality: 1 father name: the father father nationality: 1  Enter Pin to comfirm or 0 to cancel &action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1234', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you for recording a new birth! You will  receive a confirmation message with the summary of the record and the registration number&action=end')
