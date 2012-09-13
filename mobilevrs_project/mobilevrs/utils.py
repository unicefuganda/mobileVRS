'''
Created on Jul 12, 2012

@author: asseym
'''
from django.conf import settings

def dictinvert(dict):
    inv = {}
    for k, v in dict.iteritems():
        inv[v]=k
    return inv



def get_summary_dict(session, ussd_menu_dict, action):
    results = ussd_menu_dict
    pin = None
    keys=dictinvert(ussd_menu_dict)
    for nav in session.navigations.all():
        if nav.screen.downcast().slug in settings.PIN_SLUGS:
            pin = nav.response
        else:
            if keys.get(nav.screen.downcast().slug):
                results[keys.get(nav.screen.downcast().slug)] = nav.response
    results['SESSION'] = session.transaction_id
    results['MSISDN'] = session.connection.identity
    results['PIN'] = pin
    results['ACTION'] = action
    return results

def get_session_data_turples(session, ussd_menu_dict, action):
    
    results = ussd_menu_dict
    pin = None
    keys=dictinvert(ussd_menu_dict)
    for nav in session.navigations.all():
        val = settings.TRANSLATION_DICT.get(nav.screen.downcast().slug,None)
        if val in ["death_summary","birth_summary"]:
            pin = nav.screen.downcast().slug
        if val:
            results[keys.get(nav.screen.downcast().slug)] = nav.response
    results['SESSION'] = 1123
    results['MSISDN'] = session.connection.identity
    results['PIN'] = pin
    results['ACTION'] = action
    
    return results.items()


def get_summary(session):
    summary = ""
    for nav in session.navigations.all():
        val = settings.TRANSLATION_DICT.get(nav.screen.downcast().slug,None)
        if val:
            summary += "%s %s " % (val, nav.response)
    return summary