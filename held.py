import requests
import icalendar
import pytz
from os import getenv
from datetime import datetime

timestr = '%d %b %H:%M'
cet = pytz.timezone('CET')

pd_url = getenv('PD_URL')
pd_user = getenv('PD_USER')

if not pd_url or not pd_user:
    raise RuntimeError("No pagerduty schedule URL or user set!")


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
    return [e for e in events if pd_user in e['ATTENDEE']]


def event_time(event, key):
    return event[key].dt.astimezone(cet).strftime(timestr)


for e in get_my_events(get_relevant_events(get_events(get_cal()))):
    print(event_time(e, 'DTSTART'), ' - ', event_time(e, 'DTEND'))
