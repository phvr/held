#!/usr/bin/env python

import requests
import icalendar
from os import getenv

pd_url = getenv('PD_URL')
if not pd_url:
    raise RuntimeError("No pagerduty schedule URL set!")

def getcal():
    r =  requests.get(pd_url)
    cal = icalendar.Calendar.from_ical(r.text)
    return cal
