from maintenance_calendar.exceptions import UnsupportedMediaTypeError,\
    UnimplementedMethodError

class ValidatorFactory():
    def __init__(self, mimetype=None):
        self.mimetype = mimetype
    
    def create_exception_validator(self):
        self._raise_error()
    
    def create_calendar_request_validator(self):
        print "ERRRRRRRRRRR"
        self._raise_error()
    
    def create_calendar_validator(self):
        self._raise_error()
    
    def _raise_error(self):
        if self.mimetype:
            print "lanzo UnsupportedMediaTypeError!!!!"
            print self.mimetype.split(';')[0]
            print "fin lanzar!!!!"
            raise UnsupportedMediaTypeError(self.mimetype.split(';')[0])
        else:
            raise UnimplementedMethodError()