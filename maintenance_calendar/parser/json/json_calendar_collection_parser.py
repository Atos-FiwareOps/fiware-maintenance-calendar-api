from flask import json

from maintenance_calendar.parser.json.json_parser import JSONParser

class JSONCalendarCollectionParser(JSONParser):
    def __init__(self):
        super(JSONCalendarCollectionParser, self).__init__()