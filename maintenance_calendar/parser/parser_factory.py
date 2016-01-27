from maintenance_calendar.parser.json.json_parser_factory import JSONParserFactory
from maintenance_calendar.parser.xml.xml_parser_factory import XMLParserFactory
from maintenance_calendar.parser.parser import Parser

class ParserFactory():
    def get_parser(self, mimetype, type_):
        if 'application/json' in mimetype:
        	concrete_factory = JSONParserFactory()
        elif 'application/xml' in mimetype:
            concrete_factory = XMLParserFactory()
        else:
            return Parser()
        
        return concrete_factory.get_parser(type_)