from maintenance_calendar.parser.parser import Parser

from lxml import etree
from lxml import objectify

class XMLParser(Parser):
    def __init__(self):
        self.xml = ""
        self.dict = {}
    
    def _remove_xml_namespaces(self):
        objectify.deannotate(self.xml)
        etree.cleanup_namespaces(self.xml)