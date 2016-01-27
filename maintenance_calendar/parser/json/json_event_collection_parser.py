from flask import json

from maintenance_calendar.parser.json.json_parser import JSONParser

class JSONEventCollectionParser(JSONParser):
    def __init__(self):
        super(JSONEventCollectionParser, self).__init__()