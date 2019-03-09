import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from contextlib import closing
from .dates import Dates
from .event import Event

URL = "https://www.ul.ie/news-centre/events"

def simple_get():
    payload = {
                "field_event_date_value[min][date]":"2019-04-02",
                "field_event_date_value[max][date]":"2019-04-05",
                "edit-submit-news-events":"Apply"
            }

    events = None
    session = requests.Session()
    try:
        result = session.post(URL, data=payload)
        events = parse(result.text)
    except RequestException as e:
        log_error("did not work")
    print(len(events))
    return events

def parse(event_html):

    soup = BeautifulSoup(event_html, 'html.parser')
    #print(soup.p)
    p_events = []
    events = soup.findAll("div",{"class":"col-md-4 col-sm-6 news-piece"})
    #print(len(events))
    for event in events:
        dates = parse_date(event.div)
        title = parse_informationTitle(event.div)
        description = parse_informationBody(event.div)
        ev = Event(title, description, dates)
        p_events.append(ev)
    print(len(p_events))
    return p_events

def parse_date(events_html):
    #print(events_html)
    dates = None
    date = events_html.find("span",{"class":"date-display-single"})
    if date is None:
        date = events_html.find("span",{"class":"date-display-range"})
        if date is not None:
            sd = date.find("span",{"class":"date-display-start"})
            fd = date.find("span",{"class":"date-display-end"})
            print(sd.text)
            print(fd.text)
            print("two_of_them")
            dates = Dates(sd.text, fd.text)
    else:
        print(date.text, "one_of_them")
        dates = Dates(date.text)
        
    return dates

def parse_informationTitle(events_html):
    return  events_html.find("h4", {"class":"db-content-chunk-title"}).a.a.getText()

def parse_informationBody(events_html):
    return events_html.find("p").getText()

if __name__ == '__main__':
    simple_get()
