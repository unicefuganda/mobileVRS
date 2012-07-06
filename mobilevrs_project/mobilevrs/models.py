from django.db import models
from ussd.models import Menu,Field
from ussd.models import ussd_pre_transition

from rapidsms_xforms.models import XForm, XFormSubmission, XFormSubmissionValue, XFormField


skippy={

    }

summary_dict={
    'mother_nationality':'mother nationality:',
    'mother_name':'mother name:',
    'father_nationality':'father nationality:',
    'death_sex':'Deceased Sex:',
    'death_age':'deacesed age:',
    'death_reporter':'declarant name:',
    'death_birth':'date of death',
    'death_reporter_phone':'declarant phone:',
    'death_reporter_capacity':'declarant capacity:',
    'death_name':'deceased name:',
    'father_name':'father name:',
    'child_first_name':'child first name:',
    'other_name':'child other name:',
    'birth_date':'date of birth:',
    'child_sex':'child sex'

}







UTL_BIRTH_DICT={
"NFNAT":"father_nationality",
"NMNAT":"mother_nationality",
"NFAT":"father_name",
"PIN":"PIN",
"NMOT":"mother_name",
"NSEX":"child_sex",
"NDATE":"birth_date",
"NLNAME":"other_name",
"NNAME":"child_first_name",
"MSISDN":"MSISDN",
"ACTION":"ACTION",
"SESSION":"SESSION",
}




UTL_DEATH_DICT={
    'ACTION':'NEWDEATH',
    'SESSION':'SESSION',
    "MSISDN":"MSISDN",
    'PIN':'PIN',
    'DLNAME':'death_sex',
    'DAGE':'death_age',
    'DDNAME':'death_reporter',
    'DDATE':'death_birth',
    'DDFON':'death_reporter_phone',
    'DDCAP':'death_reporter_capacity',
    'DLNAME':'death_name',

}
def dictinvert(dict):
    inv = {}
    for k, v in dict.iteritems():
        inv[v]=k
    return inv



def get_summary_dict(session,dictto,action):
    results=dictto
    pin=''
    keys=dictinvert(dictto)
    for nav in session.navigations.all():
        val=summary_dict.get(nav.screen.downcast().slug,None)
        if val in ["death_summary","birth_summary"]:
            pin=nav.screen.downcast().slug
        if val:
            results[keys.get(nav.screen.downcast().slug)]=nav.response
    results['SESSION']=1123
    results['MSISDN']=session.connection.identity
    results['PIN']=pin
    results['ACTION']=action
    return results


def get_summary(session):
    summary=""
    for nav in session.navigations.all():
        val=summary_dict.get(nav.screen.downcast().slug,None)
        if val:
            summary=summary+" "+val+nav.response
    return summary
def handle_skips(sender, **kwargs):
    screen = sender.last_screen()
    if screen and screen.slug=="birth_summary":
        #b_summary=Field.objects.get(slug="birth_summary")
        #b_summary.label=get_summary(sender)
        #b_summary.question=get_summary(sender)
        #b_summary.save()
        pass
ussd_pre_transition.connect(handle_skips, weak=False)
