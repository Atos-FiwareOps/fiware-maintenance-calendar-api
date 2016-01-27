from maintenance_calendar.validator.validator_factory import ValidatorFactory
from maintenance_calendar.validator.concrete_validators.json_validator import JSONValidator
from maintenance_calendar.exceptions import EventBadRequestError, CalendarBadRequestError

class JSONValidatorFactory(ValidatorFactory):
    
    def create_event_request_validator(self):
        print "*******************"
        exception = EventBadRequestError()
        return JSONValidator("maintenance_calendar/validator/schema/json/event_request.schema.json", exception)

    def create_exception_validator(self):
        return JSONValidator("maintenance_calendar/validator/schema/json/exception_response.schema.json")

    def create_calendar_request_validator(self):
    	print "*******************"
        exception = CalendarBadRequestError()
        return JSONValidator("maintenance_calendar/validator/schema/json/calendar_request.schema.json", exception)
    
    def create_calendar_validator(self):
        return JSONValidator("maintenance_calendar/validator/schema/json/calendar.schema.json")

