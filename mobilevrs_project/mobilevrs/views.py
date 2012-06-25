from ussd.forms import YoForm
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib
from ussd.models import *
from django.conf import settings

def advance_progress(session,input):
    '''
        Navigate down the tree, based on the number the user has input.
        '''
    if input.rsplit("_")[0] == getattr(settings,"BACK_KEY","#"):
        return StubScreen(text=session.back(), terminal=False)
    screen = session.last_screen()
    if not screen:
        screen = session.get_initial_screen()
        session.navigations.create(session=session, screen=screen, text=str(screen.downcast()))
        return screen.downcast()

    nav = session.navigations.latest('date')
    nav.response = input
    nav.save()

    #check for back navigation

    try:
        ussd_pre_transition.send(sender=session, screen=screen, input=input.rsplit("_")[0], session=session)
        #handle equatel
        next = screen.downcast().accept_input(input.rsplit("_")[0], session)
        if not next:
            # this is actually an improperly configured USSD menu, but
            # we're relaxing constraints and not blowing up in the
            # case of a leaf node without any successor screen
            next = StubScreen()
        session.navigations.create(session=session, screen=next, text=str(next.downcast()))
        if next.downcast().is_terminal():
            session.complete()
        return next.downcast()
    except BackNavigation:
        return StubScreen(text=session.back(), terminal=False)
    except TransitionException as e:
        next = e.screen
        session.navigations.create(session=session, screen=next, text=str(next.downcast()))
        if next.downcast().is_terminal():
            session.complete()
        return next.downcast()


def ussd_menu(req, input_form=YoForm, output_template='ussd/yo.txt'):
    form = None
    if req.method == 'GET' and req.GET:
        form = input_form(req.GET)
    elif req.method == 'POST' and req.POST:
        form = input_form(req.POST)
    if form and form.is_valid():
        session = form.cleaned_data['transactionId']
        request_string = form.cleaned_data['ussdRequestString']
        response_screen = advance_progress(session,request_string)

        action = 'end' if response_screen.is_terminal() else 'request'
        return render_to_response(output_template, {
            'response_content':urllib.quote(str(response_screen)),
            'action':action,
            }, context_instance=RequestContext(req))
    return HttpResponse(str(form.errors))

    return HttpResponse(status=404)

