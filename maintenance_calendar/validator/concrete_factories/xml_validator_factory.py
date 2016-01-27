from maintenance_calendar.exceptions import CalendarBadRequestError
from maintenance_calendar.validator.validator_factory import ValidatorFactory
from maintenance_calendar.validator.concrete_validators.xml_validator import XMLValidator

class XMLValidatorFactory(ValidatorFactory):
    def create_exception_validator(self):
        return XMLValidator("maintenance_calendar/validator/schema/xml/exception_response.xsd")
    
    def create_calendar_request_validator(self):
        exception = CalendarBadRequestError()
        return XMLValidator("maintenance_calendar/validator/schema/xml/calendar_request.xsd", exception)
    
    def create_calendar_validator(self):
        return XMLValidator("maintenance_calendar/validator/schema/xml/calendar.xsd")