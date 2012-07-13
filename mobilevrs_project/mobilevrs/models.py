from django.db import models
from ussd.models import Menu,Field
from ussd.models import ussd_pre_transition


skippy={

    }

def handle_skips(sender, **kwargs):
    screen = sender.last_screen()
    if screen and screen.slug=="birth_summary":
        #b_summary=Field.objects.get(slug="birth_summary")
        #b_summary.label=get_summary(sender)
        #b_summary.question=get_summary(sender)
        #b_summary.save()
        pass
ussd_pre_transition.connect(handle_skips, weak=False)
