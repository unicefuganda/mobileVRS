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
        b_summary=Field.objects.get(slug="birth_summary")
        b_summary.label=get_summary(sender)
        b_summary.question=get_summary(sender)
        b_summary.save()

ussd_pre_transition.connect(handle_skips, weak=False)
