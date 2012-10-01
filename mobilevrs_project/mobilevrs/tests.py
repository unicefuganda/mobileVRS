from django.test import TestCase
from django.test.client import Client
from django.conf import settings
import urllib2
import urllib
import datetime
import creator
import logging

logger = logging.getLogger(__name__)

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
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")

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
        logger.info("\n\n Testing Birth Notify....\n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
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
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter date of birth:\n1. Today\n2. Yesterday\nOther (Enter manually in the format ddmmyyyy) &action=request')
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
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select mother's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
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
        self.assertEquals(urllib2.unquote(response.content), "responseString=Select father's nationality:\n1. Uganda\n2. Kenya\n3. Tanzania\n4. Rwanda\n5. Burundi\n6. South Sudan\n7. DR Congo\nOthers (Type in the country manually)&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Pin to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '9045', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you for recording a new birth! You will  receive a confirmation message with the summary of the record and the registration number&action=end')

    def testBirthNotifyResume(self):
        logger.info("\n\nTesting Birth Resume Notify \n\n")
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Child's first name :&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = 'my first guy',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's other name(s):&action=request")
        response = self.sendRequest(transactionId = '34455',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request')
        response = self.sendRequest(transactionId = '34455',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '6',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter child's other name(s):&action=request")

    def testDeathNotify(self):
        logger.info("\n\nTesting Death Notify\n\n")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '', \
                                    response = True\
                                    )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
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
                                    ussdRequestString = '42', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Sex of the deceased:\n1. Male\n2. Female&action=request')
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
        self.assertEquals(urllib2.unquote(response.content), "responseString=Capacity:\n1.Relative present at Death\n2.Other Relative\n3.Person present at death\n4.House occupant at location\n5.Person with knowledge\n6. Person finding  body&action=request")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '1', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter Pin to confirm or \"0\" to cancel&action=request")
        response = self.sendRequest(transactionId = '123345',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '9045', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you for recording a new death. Please inform relatives to present themselves at the Registrars office to complete the process&action=end')

    def testResumeDeathNotify(self):
        logger.info("\n\nTesting Death Notify Resume\n\n")
        response = self.sendRequest(transactionId = '123346',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '', \
                                    response = True\
                                    )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
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
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '123347',\
                                    transactionTime = self.transactionTime, \
                                    msisdn = self.msisdn, \
                                    ussdServiceCode = self.msisdn, \
                                    ussdRequestString = '6', \
                                    response = True\
                                    )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")

    def testResumeDeathNotifyAccuracy(self):
        logger.info("\n\nTesting Death Notify Accuraccy\n\n")
        response = self.sendRequest(transactionId = '123346',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '',\
            response = True\
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '123346',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '2',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter names of the Deceased:&action=request")
        response = self.sendRequest(transactionId = '123346',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = 'Mr. Dead',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '6',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Age of the deceased:&action=request")
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '45',\
            response = True\
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Sex of the deceased:\n1. Male\n2. Female&action=request")
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1',\
            response = True\
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Date of death (ddmmyyyy):&action=request")
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '12122011',\
            response = True\
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Names of Declarant:&action=request")
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = 'Kenneth',\
            response = True\
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Declarant's Phone Number:&action=request")
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '63773737737',\
            response = True\
        )
        self.assertEqual(urllib2.unquote(response.content), "responseString=Capacity:\n1.Relative present at Death\n2.Other Relative\n3.Person present at death\n4.House occupant at location\n5.Person with knowledge\n6. Person finding  body&action=request")
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1',\
            response = False\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter Pin to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = '123347',\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '9045',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you for recording a new death. Please inform relatives to present themselves at the Registrars office to complete the process&action=end')

    def testUserManagementUserCreation(self):
        logger.info("\n\nTesting User Management User Creation\n\n")
        self.transactionId = '50012'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '5',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Create User\n2. Modify Pin\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's Surname:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString ="user register",\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's other names:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = 'Other names',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's sex:\n1. Male\n2. Female&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's Date of Birth (ddmmyyyy):&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '12121999',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter user's phone number:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '078942422424',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter User's parish or ward:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = 'kampala',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '9045',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Thank you creating a new user. You will receive a confirmation message.&action=end")

    def testModifyPin(self):
        logger.info("\n\nTesting User management modify Pin\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '5',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Create User\n2. Modify Pin\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '2',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter old PIN:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '9045',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Enter new PIN:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '2325',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=Re-enter new PIN:&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '2325',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=You will receive a message to confirm the change of your PIN. Protect your PIN. Keep it secret. Do not share it.&action=end")

    def testValidateViewRecord(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '4',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=View Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '9045',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you. You will receive a message with a summary of this record.&action=end')

    def testValidateValidateRecord(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '4',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '2',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1232',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Re-enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1232',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Validate Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '9045',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you for validating this record. You will receive a confirmation message.&action=end')

    def testDeleteValidateRecord(self):
        logger.info("\n\nTesting Validate View Record\n\n")
        self.transactionId = '534545'
        response = self.sendRequest()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. Notify Birth\n2. Notify Death\n3. Edit Record\n4. Validation\n5. User Management\n6. Resume Previous&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '4',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), "responseString=1. View Record\n2. Validate\n3. Delete\n#. Back&action=request")
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '3',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1232',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Re-enter reference number:&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '1232',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Delete Record\n\nEnter  PIN to confirm or "0" to cancel&action=request')
        response = self.sendRequest(transactionId = self.transactionId,\
            transactionTime = self.transactionTime,\
            msisdn = self.msisdn,\
            ussdServiceCode = self.msisdn,\
            ussdRequestString = '9045',\
            response = True\
        )
        self.assertEquals(urllib2.unquote(response.content), 'responseString=Thank you for updating the civil registry! You will receive a confirmation message.&action=end')