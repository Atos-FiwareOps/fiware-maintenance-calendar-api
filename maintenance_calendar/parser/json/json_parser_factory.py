from maintenance_calendar.parser.json.json_calendar_parser import JSONCalendarParser
from maintenance_calendar.parser.json.json_event_parser import JSONEventParser
from maintenance_calendar.parser.parser import Parser
from maintenance_calendar.parser.json.json_calendar_collection_parser import JSONCalendarCollectionParser
from maintenance_calendar.parser.json.json_event_collection_parser import JSONEventCollectionParser
from maintenance_calendar.parser.json.json_exception_parser import JSONExceptionParser

class JSONParserFactory():
    def get_parser(self, type_):
        if type_.__name__ in 'Calendar':
            return JSONCalendarParser()
        elif type_.__name__ in 'CalendarCollection':
            return JSONCalendarCollectionParser()
        elif type_.__name__ in 'Event':
            return JSONEventParser()
        elif type_.__name__ in 'EventCollection':
            return JSONEventCollectionParser()
        elif type_.__name__ in 'MaintenanceCalendarSyncError':
            return JSONExceptionParser()
        else:
            return Parser()