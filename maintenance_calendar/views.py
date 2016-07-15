import requests
from functools import wraps
from flask import json, session
import maintenance_calendar.common.util as util
from maintenance_calendar.calendar_synchronizer import CalendarSynchronizer
from maintenance_calendar import app
from flask import request
import re
from werkzeug.wrappers import Response

from maintenance_calendar.validator import factory_selector
from maintenance_calendar.model import Calendar, Event
from exceptions import UnAuthorizedMethodError

from maintenance_calendar import config
import ast

from maintenance_calendar.contextbroker.context_broker_notification import ContextBrokerNotificator

import logging

log = logging.getLogger(__name__)

# set the secret key.  keep this really secret:
#To generate the new secret Key use this:
#>>> import os
#>>> os.urandom(24)
app.secret_key = '\x14B\t\xeeEY\xa0\x96O\xac\xd0\xa7;;f\x06\xd7&y\xd6\xd9\xab`{'

#authentication and authorization part
def check_auth(token):
    """This function is called to check if the token is valid
    """
    chech_auth = False
    url_keystone = config.url_keystone + token
    responseToken = requests.get(url_keystone)
    if (responseToken.status_code == 200):
        try:
            user = json.loads(responseToken.content)
            session['user'] = user
            session['token'] = token
            chech_auth = True
        except Exception, e:
            log.error("check_auth(): Error - " + str(e))
            chech_auth = False
    else:
        chech_auth = False
    return chech_auth

def authenticate():
    """Sends a 401 response that enables Auth2 authentication"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper token', 401,
    {'X-Auth-Token': 'Auth2 realm="Token Required"'})

def authorization():
    """Sends a 401 response that enables Auth2 authentication"""
    log.info("authorization(): creation of message 405")
    return Response(
    'The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.\n', 405 )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Auth-Token')
        if not token or not check_auth(token):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def exists_node_calendar(node):
    listNodes = ast.literal_eval(config.node_list)
    if any(d.get('id', None) == node for d in listNodes):
        return True
    else:
        return False

def authorization(location):
    ##This method is reponsible to manage the authorization for the different events.
    ##This method validate if the user has the apropiate rol for manage events for one node or for non-maintenance periods
    is_authorized = False
    try:
        user = session['user']
        if location == 'UptimeRequests':
            #validate if the user has privileges to manage the events of the non-maintenance periods
            roles = user['roles']
            for role in roles:
                role_name =  role['name']
                if role_name=='UptimeRequester':
                    is_authorized = True
                    break

        else:
            #validate if the node is in the list of available node calendars
            if exists_node_calendar(location):
                #validate if the user has privileges to manage the events of this node
                organizations = user['organizations']
                if log.isEnabledFor(logging.DEBUG):
                    log.debug ("authorization(): organizations - " + str(organizations))

                for organization in organizations:
                    name = organization['name']
                    position = name.find("FIDASH")
                    if position != -1:
                        name_organization = name[:position-1]
                        if name_organization==location:
                            roles = organization['roles']
                            for role in roles:
                                role_name =  role['name']
                                if role_name=='InfrastructureOwner':
                                    is_authorized = True
                                    break
                            break
            else:
                log.info('authorization(): The name of the node is not included in the list of available calendars')

    except Exception, e:
            #any error indicate that the structure is not correct and we don't allow to connect for this user.
            is_authorized = False
            log.error("authorization(): Error for location " + str(location) +" exception - " + str(e))
    
    if not is_authorized:
        log.warning("authorization(): The user is not authorized for the location" + str(location))
        raise UnAuthorizedMethodError()
        

#definition of the different views
@app.errorhandler(404)
def not_found(error):
    return "The requested resource does not exist", 404

@app.errorhandler(UnAuthorizedMethodError)
def not_authorized(error):
    return Response('The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.', status=405)
    #return "The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.", 405

@app.route('/api/v1')
@requires_auth
def hello_world():
    
    ##example for creating subscriptions of the Calendar.
    #_contextbroker = ContextBrokerNotificator(session['token'])
    #_contextbroker.notify_maintenance_event("Spain2",  _contextbroker.NEW_EVENT,  "maintenance_description_definitivo")
    #_contextbroker.notify_uptimerequests_event( _contextbroker.UPDATED_EVENT,  "UptimeRequests_definitivo")

    return 'Hello World! '
  

@app.route("/api/v1/events", methods=['GET'])
@requires_auth
def get_events():

    location = request.args.get('location')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    if log.isEnabledFor(logging.DEBUG):
        log.debug ("get_events(): args - " + str(location) + str(start_date) + str(end_date))
    calendarSynchronizer = CalendarSynchronizer()
    calendar_collection = calendarSynchronizer.get_events(location, start_date, end_date)
    response_body = calendar_collection.serialize(request.accept_mimetypes)  
    return Response(response_body, mimetype=request.accept_mimetypes[0][0]) 

@app.route("/api/v1/events", methods=['POST'])
@requires_auth
def create_event():
    body = util.remove_non_usable_characters(
                        util.remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type

    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.create_event_request_validator()
    validator.validate(body)


    event = Event.deserialize(content_type, body)

    #validate the authorization to create it 
    if log.isEnabledFor(logging.DEBUG):
        log.debug ("create_event(): location - " + str(event.location))
    authorization(event.location)

    manager = CalendarSynchronizer()
    new_event = manager.register_event(event)
    
    response_body = new_event.serialize(request.accept_mimetypes)

    #Notify when a new event is created
    _contextbroker = ContextBrokerNotificator(session['token'])
    _contextbroker.notify_event(new_event, _contextbroker.NEW_EVENT)
    
    return Response(response_body, status=201, mimetype=request.accept_mimetypes[0][0])

@app.route("/api/v1/events/<event_id>", methods=['GET'])
@requires_auth
def get_event(event_id):

    manager = CalendarSynchronizer()
    event = manager.get_event(event_id)
    if event is None:
        return Response('Not Found Event', status=404)
    
    response_body = event.serialize(request.accept_mimetypes)
    return Response(response_body, status=200, mimetype=request.accept_mimetypes[0][0])


#To be confirmed if the radicalle accept modify a calendar event
@app.route("/api/v1/events/<event_id>", methods=['PUT'])
@requires_auth
def modify_event(event_id):
    return 'Not implemented, modifying event {0}'.format(event_id)

@app.route("/api/v1/events/<event_id>", methods=['DELETE'])
@requires_auth
def delete_event(event_id):

    manager = CalendarSynchronizer()
    #before to remoe it, we need to collect the event to know the location, we don't want to delegate this action to the CalendarSynchronizer
    #if we didn't want to create two calls to the calendar, we will need to translate this validation to the CalendarSynchronizer
    event = manager.get_event(event_id)
    if event is None:
        return Response('Not Found Event', status=404)
    #validate the authorization to delete it
    authorization(event.location)

    status = manager.remove_event(event_id)
    if status:
        #Notify when a new event is created
        _contextbroker = ContextBrokerNotificator(session['token'])
        _contextbroker.notify_event(event, _contextbroker.DELETED_EVENT)

        return Response(status=204)
    else:
        return Response('Not Found Event', status=404)

if __name__ == '__main__':
    app.run()


@app.route("/api/v1/nodes", methods=['GET'])
@requires_auth
def get_nodes():
    manager = CalendarSynchronizer()
    node_collection = manager.get_available_nodes()
    response_body = node_collection.serialize(request.accept_mimetypes)  
    return Response(response_body, mimetype=request.accept_mimetypes[0][0]) 


@app.route("/api/v1/ics/maintenanceCalendarFiwareLab", methods=['GET'])
def get_ics():
    ics_url = config.url_calendar + config.ics_calendar
    response = requests.get(ics_url)
    if (response.status_code == 200):
        try:
            if log.isEnabledFor(logging.DEBUG):
                log.debug ("get_ics(): ICS content - " + str(response.content))
            log.info("get_ics(): Return ICS calendar!!!!")
        except Exception, e:
            log.error("get_ics(): Error - " + str(e))
            return Response('Not Found Ics Calendar', status=404)
            
    return Response(response.content)
