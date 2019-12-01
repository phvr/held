import requests
import icalendar
import pytz
from os import getenv
from datetime import datetime

timestr = '%d %b %H:%M'
cet = pytz.timezone('CET')

me = 'philip.vanreeuwijk'
pd_url = getenv('PD_URL')

if not pd_url:
    raise RuntimeError("No pagerduty schedule URL set!")


def get_cal():
    r = requests.get(pd_url)
    cal = icalendar.Calendar.from_ical(r.text)
    return cal.walk()


def get_events(cal):
    return cal[1:]


def get_relevant_events(events):
    now = datetime.now(pytz.utc)
    return [e for e in events if e['DTEND'].dt > now]


def get_my_events(events):
    return [e for e in events if me in e['ATTENDEE']]


def event_time(event, key):
    return e[key].dt.astimezone(cet).strftime(timestr)


events = get_my_events(get_relevant_events(get_events(get_cal())))

for e in events:
    print(event_time(e, 'DTSTART'), ' - ', event_time(e, 'DTEND'))
