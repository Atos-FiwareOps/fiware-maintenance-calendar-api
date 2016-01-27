from maintenance_calendar.validator.validator import Validator
from lxml import etree

class XMLValidator(Validator):
    def validate(self, data):
        schema = etree.XMLSchema(file=self.schema_file)
        parser = etree.XMLParser(schema=schema)
        
        try:
            etree.fromstring(data, parser)
        except etree.XMLSyntaxError as error:
            if self.error:
                raise self.error
            else:
                raise error