from jsonschema import Draft4Validator
from maintenance_calendar.validator.validator import Validator
import json
from jsonschema.exceptions import ValidationError

class JSONValidator(Validator):
    def validate(self, data):
        with open(self.schema_file) as json_data:
            schema = json.load(json_data)
        request = json.loads(data)
        
        try:
            validator = Draft4Validator(schema)
            validator.validate(request)
        except ValidationError as error:
            if self.error:
                raise self.error
            else:
                raise error