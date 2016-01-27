from lxml import etree
from lxml import objectify
from maintenance_calendar.parser.xml.xml_parser import XMLParser

class XMLExceptionParser(XMLParser):
    def from_model(self, exception):
        self._create_xml_root_element()
        self._insert_infrastructure_xml_data(exception)
        self._remove_xml_namespaces()
        
        return etree.tostring(self.xml)
    
    def _create_xml_root_element(self):
        maker = objectify.ElementMaker()
        self.xml = maker.error()
    
    def _insert_infrastructure_xml_data(self, infrastructure):
        self.xml.message = infrastructure.message