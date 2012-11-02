#!/usr/bin/env python
"""Gevent based crontab implementation"""

from datetime import datetime, timedelta
import gevent
import jsonrpclib, time

server = jsonrpclib.Server("http://localhost:8080")

# Some utility classes / functions first
def conv_to_set(obj):
    """Converts to set allowing single integer to be provided"""

    if isinstance(obj, (int, long)):
        return set([obj])  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj

class AllMatch(set):
    """Universal set - match everything"""
    def __contains__(self, item): 
        return True

allMatch = AllMatch()

class Event(object):
    """The Actual Event Class"""

    def __init__(self, action, minute=allMatch, hour=allMatch, 
                       day=allMatch, month=allMatch, daysofweek=allMatch, 
                       args=(), kwargs={}):
        self.mins = conv_to_set(minute)
        self.hours = conv_to_set(hour)
        self.days = conv_to_set(day)
        self.months = conv_to_set(month)
        self.daysofweek = conv_to_set(daysofweek)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t1):
        """Return True if this event should trigger at the specified datetime"""
        return ((t1.minute     in self.mins) and
                (t1.hour       in self.hours) and
                (t1.day        in self.days) and
                (t1.month      in self.months) and
                (t1.weekday()  in self.daysofweek))

    def check(self, t):
        """Check and run action if needed"""

        if self.matchtime(t):
            self.action(*self.args, **self.kwargs)

class CronTab(object):
    """The crontab implementation"""

    def __init__(self, *events):
        self.events = events

    def _check(self):
        """Check all events in separate greenlets"""

        t1 = datetime(*datetime.now().timetuple()[:5])
        for event in self.events:
            gevent.spawn(event.check, t1)

        t1 += timedelta(minutes=1)
        s1 = (t1 - datetime.now()).seconds + 1
        print "Checking again in %s seconds" % s1
        job = gevent.spawn_later(s1, self._check)

    def run(self):
        """Run the cron forever"""

        self._check()
        while True:
            gevent.sleep(60)

import os 
def test_task( node ):
	server.light_on( node )


cron = CronTab(
  Event(test_task(7), 55, 16 ),
  Event(test_task(3), 54, 16 ),
)
#Event(test_task, 0, range(9,18,2), daysofweek=range(0,5)),
cron.run()



