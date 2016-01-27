from maintenance_calendar.parser.parser import Parser
from flask import json

class JSONParser(Parser):

	def from_model(self, data):
		return json.dumps(data.to_dict(), default=lambda o: o.__dict__)