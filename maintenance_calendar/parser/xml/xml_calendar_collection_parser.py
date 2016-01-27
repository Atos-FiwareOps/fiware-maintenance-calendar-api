from lxml import etree
from lxml import objectify

from maintenance_calendar.parser.xml.xml_parser import XMLParser
from maintenance_calendar.parser.xml.xml_calendar_parser import XMLCalendarParser

class XMLCalendarCollectionParser(XMLParser):
    def from_model(self, calendar_collection):
        self._create_xml_root_element()
        self._insert_calendar_collection_xml_data(calendar_collection)
        self._remove_xml_namespaces()
        
        return etree.tostring(self.xml)
    
    def _create_xml_root_element(self):
        maker = objectify.ElementMaker()
        self.xml = maker.calendar()
    
    def _insert_calendar_collection_xml_data(self, flavor_collection):
        xml_calendars = []
        calendar_parser = XMLCalendarParser()
        for calendar in calendar_collection.calendars:
            calendar_parser.from_model(calendar)
            xml_calendars.append(calendar_parser.xml)
        
        self.xml.calendar = xml_calendars