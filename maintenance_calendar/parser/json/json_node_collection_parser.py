from flask import json

from maintenance_calendar.parser.json.json_parser import JSONParser

class JSONNodeCollectionParser(JSONParser):
    def __init__(self):
        super(JSONNodeCollectionParser, self).__init__()