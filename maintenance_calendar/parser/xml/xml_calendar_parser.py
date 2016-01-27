from lxml import etree
from lxml import objectify

from maintenance_calendar.parser.xml.xml_parser import XMLParser

class XMLCalendarParser(XMLParser):
    def __init__(self):
        super(XMLCalendarParser, self).__init__()
    
    def to_dict(self, xml_data):
        obj = objectify.fromstring(xml_data)
        
        if 'name' in objectify.dump(obj):
            self.dict["name"] = str(obj.name)
        
        return self.dict
    
    def from_model(self, calendar):
        self._create_xml_root_element()
        self._insert_calender_xml_data(calendar)
        self._remove_xml_namespaces()
        
        return etree.tostring(self.xml)
    
    def _create_xml_root_element(self):
        maker = objectify.ElementMaker()
        self.xml = maker.calendar()
    
    def _insert_calendar_xml_data(self, calendar):
        self.xml.set('id', calendar.id)
        self.xml.name = calendar.name
                    
        self.xml.node = nodes