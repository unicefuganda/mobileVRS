from django.conf import settings
from mobilevrs.utils import get_summary_dict
import urllib2, urllib
import logging

logger = logging.getLogger(__name__)

def forward_to_utl(session,**kwargs):
    logger.info("forwarding to utl...")
    if session.navigations.order_by('date')[0].response=='1':
        collected_data = get_summary_dict(session, settings.UTL_BIRTH_DICT)
        result = urllib2.urlopen('%s?%s' % (settings.FORWARD_URL,urllib.urlencode(collected_data)))
        logger.info('Submitting to UTL: %s' % result.url)
        logger.info('UTL Replied: %s' % result.read().strip())
        return result
    elif session.navigations.order_by('date')[0].response=='2':
        collected_data = get_summary_dict(session, settings.UTL_DEATH_DICT)
        result = urllib2.urlopen('%s?%s' % (settings.FORWARD_URL,urllib.urlencode(collected_data)))
        logger.info('Submitting to UTL: %s' % result.url)
        logger.info('UTL Replied: %s' % result.read().strip())
        return result
    elif session.navigations.order_by('date')[0].response=='4' and session.navigations.order_by('date')[1].response=='1':
        collected_data = get_summary_dict(session, settings.UTL_CREATE_USER_DICT)
        result = urllib2.urlopen('%s?%s' % (settings.FORWARD_URL,urllib.urlencode(collected_data)))
        logger.info('Submitting to UTL: %s' % result.url)
        logger.info('UTL Replied: %s' % result.read().strip())
        return result
    elif session.navigations.order_by('date')[0].response=='4' and session.navigations.order_by('date')[1].response=='2':
        collected_data = get_summary_dict(session, settings.UTL_MODIFY_PIN_DICT)
        result = urllib2.urlopen('%s?%s' % (settings.FORWARD_URL,urllib.urlencode(collected_data)))
        logger.info('Submitting to UTL: %s' % result.url)
        logger.info('UTL Replied: %s' % result.read().strip())
        return result
