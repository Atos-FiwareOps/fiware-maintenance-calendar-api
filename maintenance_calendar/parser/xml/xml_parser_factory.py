from maintenance_calendar.parser.xml.xml_calendar_parser import XMLCalendarParser
from maintenance_calendar.parser.parser import Parser
from maintenance_calendar.parser.xml.xml_calendar_collection_parser import XMLCalendarCollectionParser
from maintenance_calendar.parser.xml.xml_exception_parser import XMLExceptionParser

class XMLParserFactory():
    def get_parser(self, type_):
        if type_.__name__ in 'Calendar':
            return XMLCalendarParser()
        elif type_.__name__ in 'CalendarCollection':
            return XMLCalendarCollectionParser()
        elif type_.__name__ in 'MaintenanceCalendarSyncError':
            return XMLExceptionParser()
        else:
            return Parser()