from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.conf import settings
import urllib2
import urllib
import datetime

class ViewTest(TestCase):

    def setUp(self):
        self.transactionId = '123344'
        self.transactionTime = datetime.datetime.now().strftime('%Y%m%dT%H:%M:%S')
        self.msisdn = '256776520831'
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
        
    def testUTLDataPost(self):
        data_structure = settings.UTL_BIRTH_DICT
        keys = dict([[v,k] for k,v in data_structure.items()])
        action = 'NEWBIRTH'
        post_data = {
            "NMNAT":"1",
            "NFNAT":"1",
            "NMOT":"test mother name",
            "NFAT":"test father name",
            "NSEX":"1",
            "NDATE":"11092012",
            "NNAME":"test child name",
            "NLNAME":"other child name",
            "PIN":"9045",
            "MSISDN":"256776520831",
            "ACTION":action,
            "SESSION":"1123",
        }
        result = urllib2.urlopen('http://www.mobilevrs.co.ug/ussd/notify.php?%s' % urllib.urlencode(post_data))
        self.assertEquals(result.getcode(), 200)
        
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
                                    ussdRequestString = '9045', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you for recording a new birth! You will  receive a confirmation message with the summary of the record and the registration number&action=end')
        
    def testDeathNotify(self):
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '', \
                                    response = True\
                                    )
        self.assertEquals(response.status_code, 200)
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '2', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter names of the Deceased:&action=request")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = 'my first dead guy', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = 'mbu 42', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Sex of the deceased:1. Male 2. Female&action=request')
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Date of death (ddmmyyyy):&action=request')
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '12072012', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Names of Declarant:&action=request")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = 'some woman', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Declarant's Phone Number:&action=request")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '256782998903', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Capacity: 1.Relative present at Death 2.Other Relative  3.Person present at death 4.House occupant at location 5.Person with knowledge 6. Person finding  body&action=request")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Summary deceased name: my first dead guy deacesed age: mbu 42 Deceased Sex: 1 declarant name: some woman declarant phone: 256782998903 declarant capacity: 1  Death Summary: &action=request")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '9045', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you for recording a new death. Please inform relatives to present themselves at the Registrars office to complete the process&action=end')
        
    def testResumeDeathNotify(self):
        response = self.sendRequest(transactionId = '123346',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '', \
                                    response = True\
                                    )
        self.assertEquals(response.status_code, 200)
        response = self.sendRequest(transactionId = '123346',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '2', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter names of the Deceased:&action=request")
        response = self.sendRequest(transactionId = '123346',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = 'my first dead guy', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = '123347',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '', \
                                    response = True\
                                    )
        response = self.sendRequest(transactionId = '123347',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '5', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
