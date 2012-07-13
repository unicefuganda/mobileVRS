from ussd.forms import YoForm
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib
from ussd.models import *
from django.conf import settings
from mobilevrs.tasks import forward_to_utl
from mobilevrs.utils import get_summary
from mobilevrs.models import *
from django.core.cache import cache
def advance_progress(session,input):
    '''
        Navigate down the tree, based on the number the user has input.
        '''
#    import ipdb;ipdb.set_trace()
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
        #start caching for navigations>3
        if session.navigations.count()>=3:
            if not session.connection.identity in cache:
                sess={}
                sess['pk']=session.pk
                sess['transaction_id']=session.transaction_id
                cache.set(session.connection.identity,sess,1800)

        if session.navigations.count():
            if session.navigations.order_by('-date')[0].screen.downcast().is_terminal():
                #forward the responses in the session to utl
                response = forward_to_utl(session)
                
                if not response.status_code == 200:
                    #if the submission into utl does not return success?
                    resp = "The information was not saved. Please start again"
                    return render_to_response(output_template, {
                        'response_content':urllib.quote(str(resp)),
                        'action':'end',
                        }, context_instance=RequestContext(req))

        #submit input and advance to the next screen
        response_screen = advance_progress(session,request_string)
        
        #is this a terminal screen or not?
        action = 'end' if response_screen.is_terminal() else 'request'
        
        #Pre-pend a summary to the second last question
        if str(response_screen) in ["Enter Pin to comfirm or 0 to cancel","Death Summary:"]:
            response_screen="Summary %s %s " % (get_summary(session), str(response_screen))
        
        #Determine if a resume option has been selected and serve the last dropped session    
        label = response_screen if type(response_screen) == unicode else response_screen.label 
        if label == "Resume Previous" :
            if session.connection.identity in cache:
                ses=cache.get(session.connection.identity)
                prev_session=Session.objects.get(pk=ses.get('pk'))
                response_screen=prev_session.navigations.latest('date').text
                prev_session.transaction_id=session.transaction_id
                prev_session.save()
                session.delete()
            else:
                response_screen="You Have No Resumable Sessions"
                
        #TODO: handle edit function
        #TODO: handle user management
        #TODO: handle skips

        return render_to_response(output_template, {
            'response_content':urllib.quote(str(response_screen)),
            'action':action,
            }, context_instance=RequestContext(req))


    return HttpResponse(status=404)

