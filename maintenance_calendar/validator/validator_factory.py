from maintenance_calendar.exceptions import UnsupportedMediaTypeError,\
    UnimplementedMethodError
import logging

log = logging.getLogger(__name__)

class ValidatorFactory():
    def __init__(self, mimetype=None):
        self.mimetype = mimetype
    
    def create_exception_validator(self):
        self._raise_error()
    
    def create_calendar_request_validator(self):
        self._raise_error()
    
    def create_calendar_validator(self):
        self._raise_error()
    
    def _raise_error(self):
        if self.mimetype:
            log.info("ValidatorFactory-_raise_error(): raise UnsupportedMediaTypeError - " + str(self.mimetype.split(';')[0]))
            raise UnsupportedMediaTypeError(self.mimetype.split(';')[0])
        else:
            raise UnimplementedMethodError()