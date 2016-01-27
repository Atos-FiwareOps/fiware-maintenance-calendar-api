from flask import json

from maintenance_calendar.parser.json.json_parser import JSONParser

class JSONEventParser(JSONParser):
    def to_dict(self, data):
        return json.loads(data)