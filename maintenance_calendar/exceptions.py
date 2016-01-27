from maintenance_calendar import app
from flask import request
from flask import Response
from maintenance_calendar.parser.parser_factory import ParserFactory


class UnAuthorizedMethodError(Exception):
    status_code = 405
    def __init__(self):
        Exception.__init__(self, "UnAuthorized method")


class UnimplementedMethodError(Exception):
    def __init__(self):
        Exception.__init__(self, "Uninplemented method")

class MaintenanceCalendarError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        print "init Exception !!!!!!!!!!!!!!!!"
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error']= {"message" : self.message}
        return rv
    
    def super_class(self):
        return self.__class__


class EventBadRequestError(MaintenanceCalendarError):
    status_code = 400
    
    def __init__(self):
        message = "The Event is not well formed"
        super(EventBadRequestError, self).__init__(message, self.status_code)

class CalendarBadRequestError(MaintenanceCalendarError):
    status_code = 400
    
    def __init__(self):
        message = "The Calendar is not well formed"
        super(CalendarBadRequestError, self).__init__(message, self.status_code)

class UnsupportedMediaTypeError(MaintenanceCalendarError):
    status_code = 415
    
    def __init__(self, content_type):
        if content_type:
            message = "Unrecognized content type '{0}'.".format(content_type)
            message += " Mustbe 'application/xml or 'application/json'"
        else:
            message = "Unrecognized content type. Mustbe 'application/xml'"
            message += " or 'application/json'"
        
        super(UnsupportedMediaTypeError, self).__init__(message, self.status_code)

@app.errorhandler(MaintenanceCalendarError)
def handle_invalid_usage(error):
    mimetype = request.accept_mimetypes
    
    parser_factory = ParserFactory()
    print "valor mimetype!!!!", mimetype
    parser = parser_factory.get_parser(mimetype, MaintenanceCalendarError)
    print "inicializado parser!!!!"
    
    response_body = parser.from_model(error)
    
    return Response(response_body, status=error.status_code, mimetype=mimetype[0][0])