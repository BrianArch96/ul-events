from adapt.intent import IntentBuilder

import requests
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import getLogger
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from contextlib import closing
from .Webscrape import webscrape
class ULEventsSkill(MycroftSkill):
    def __init__(self):
        super(ULEventsSkill, self).__init__(name="ULEventsSkill")
        self._events = []
        self._events = webscrape.simple_get()
        print(len(self._events), "Hello")
        for ev in self._events:
            print(ev.title)

    @intent_handler(IntentBuilder("").require("List_All_Events"))
    def handle_list_all(self, message):
        print(len(self._events))
        for event in self._events:
            print(event.title)
            self.speak_dialog(event.title)

    @intent_handler(IntentBuilder("").require("Next_Event"))
    def handle_next_event(self, message):
        self.speak_dialog(self._events[0].title)
        self.set_context("tell_more", "None")

    @intent_handler(IntentBuilder("").require("tell_me_more").require("tell_more"))
    def handle_tell_more(self, message):
        self.speak_dialog(self._events[0].description)

    @intent_handler(IntentBuilder("").require("event_time"))
    def handle_event_time(self, message):
        self.speak_dialog(self._events[0].dates.startTime)

def create_skill():
    return ULEventsSkill()
