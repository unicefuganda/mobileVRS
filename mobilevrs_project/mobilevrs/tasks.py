from django.conf import settings
from mobilevrs.utils import get_summary_dict, get_dictionary_for_session
import urllib2, urllib
import logging

logger = logging.getLogger(__name__)

def forward_to_utl(session,**kwargs):
    logger.info("forwarding to utl...")
    collected_data = get_summary_dict(session, get_dictionary_for_session(session))
    result = urllib2.urlopen('%s?%s' % (settings.FORWARD_URL,urllib.urlencode(collected_data)))
    logger.info('Submitting to UTL: %s' % result.url)
    logger.info('UTL Replied: %s' % result.read().strip())
    return result