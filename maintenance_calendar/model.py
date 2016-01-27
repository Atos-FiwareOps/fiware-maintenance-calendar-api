from maintenance_calendar.parser.parser_factory import ParserFactory
import re
from caldav.elements import dav, cdav


class ParseableModel(object):
    @classmethod
    def deserialize(cls, mimetype, data):
        parser_factory = ParserFactory()
        parser = parser_factory.get_parser(mimetype, cls)
        return parser.to_dict(data)
    
    def serialize(self, mimetype):
        parser_factory = ParserFactory()
        parser = parser_factory.get_parser(mimetype, self.__class__)
        return parser.from_model(self)

# classes of model

class Calendar(ParseableModel):
  
    name = None
    cal_id = None

    def __init__(self, name=None, cal_id=None):
        self.name = name
        self.cal_id = cal_id
        
    def __repr__(self):
        return '<Calendar %r>' % self.name
    
    @classmethod
    def deserialize(cls, mimetype, data):
        calendar_dict = super(Calendar, cls).deserialize(mimetype, data)

        print "Calendar-deserialize(): deserialize Calendar: ", calendar_dict
        return Calendar( calendar_dict.get('name'))
    
    @classmethod
    def from_remote_calendar(cls, remote_calendar):
        props = remote_calendar.get_properties([dav.DisplayName(),])
        return (Calendar(props[dav.DisplayName.tag], remote_calendar.id))
    
    def serialize(self, mimetype):
        return ParseableModel.serialize(self, mimetype)
    
    def _to_content_dict(self):
        return {
                   "cal_id": self.cal_id,
                   "name" : self.name

               }
    
    def to_dict(self):
        return {"calendar" : self._to_content_dict()}
    

class CalendarCollection(ParseableModel):
    def __init__(self, calendars):
        self.calendars = calendars
    
    @classmethod
    def from_remote_calendar(cls, remote_calendar_list):
        calendars = []
        print "CalendarCollection-from_remote_calendar(): remote_calendar_list", remote_calendar_list
        for remote_calendar in remote_calendar_list:
            calendars.append(Calendar.from_remote_calendar(remote_calendar))
            
        return CalendarCollection(calendars)
    
    def serialize(self, mimetype):
        return ParseableModel.serialize(self, mimetype)
    
    def extend(self, calendar_collection):
        self.calendars.extend(calendar_collection.calendars)
    
    def to_dict(self):
        calendars = []
        for calendar in self.calendars:
            print "CalendarCollection-to_dict(): CALENDAR", calendar
            calendar_dict = calendar._to_content_dict()
            calendars.append(calendar_dict)
        
        return {"calendars" : calendars}


class Event(ParseableModel):
  
    uid =None
    dtstamp = None
    dtstart = None
    dtend = None
    summary = None
    description = None
    location = None

    def __init__(self, dtstart, dtend, summary, description, location, uid = None, dtstamp = None):
        self.uid = uid
        self.dtstamp = dtstamp
        self.dtstart = dtstart
        self.dtend = dtend
        self.summary = summary
        self.description = description
        self.location = location

    def __repr__(self):
        return '<Event %r>' % self.location

    @classmethod
    def deserialize(cls, mimetype, data):
        event_dict = super(Event, cls).deserialize(mimetype, data)

        #print "deserialize Event: ", event_dict
        
        return (Event(dtstart = event_dict.get('dtstart'),
            dtend = event_dict.get('dtend'),
            summary = event_dict.get('summary'),
            description = event_dict.get('description'),
            location = event_dict.get('location'),
            uid = event_dict.get('uid'),
            dtstamp = event_dict.get('dtstamp')))
    
    @classmethod
    def from_remote_event(cls, remote_event):

        remote_event.load()
        vobj = remote_event.instance

        return (Event(uid = vobj.vevent.uid.value, 
            dtstamp = vobj.vevent.dtstamp.value.strftime("%Y-%m-%d %H:%M:%S%z"), 
            dtstart = vobj.vevent.dtstart.value.strftime("%Y-%m-%d %H:%M:%S%z"),
            dtend = vobj.vevent.dtend.value.strftime("%Y-%m-%d %H:%M:%S%z"),
            summary = vobj.vevent.summary.value,
            description = vobj.vevent.description.value,
            location = vobj.vevent.location.value))
    
    def serialize(self, mimetype):
        return ParseableModel.serialize(self, mimetype)
    
    def _to_content_dict(self):
        #print "_to_content_dict"
        return {
                   "uid": self.uid,
                   "dtstamp" : self.dtstamp,
                   "dtstart" : self.dtstart,
                   "dtend" : self.dtend,
                   "summary" : self.summary,
                   "description" : self.description,
                   "location" : self.location
               }
    
    def to_dict(self):
        #print "to_dict Event"
        return {"event" : self._to_content_dict()}
    


class EventCollection(ParseableModel):
    def __init__(self, events):
        self.events = events
    
    @classmethod
    def from_remote_event(cls, remote_event_list):
        events = []
        #print "remote_event_list", remote_event_list
        for remote_event in remote_event_list:
            events.append(Event.from_remote_event(remote_event))
            
        return EventCollection(events)
    
    def serialize(self, mimetype):
        return ParseableModel.serialize(self, mimetype)
    
    def extend(self, event_collection):
        self.events.extend(event_collection.events)
    
    def to_dict(self):
        #print "to_dict Collection Event" , self.events
        events = []
        for event in self.events:
            print "EventCollection-to_dict(): Event", event
            event_dict = event._to_content_dict()
            events.append(event_dict)
        
        return {"events" : events}