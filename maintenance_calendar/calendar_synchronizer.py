from maintenance_calendar import config
from datetime import datetime, date
import pytz
import caldav
from caldav.elements import dav, cdav
from model import CalendarCollection, Calendar, EventCollection, Event, Node, NodeCollection
import uuid
import dateutil.parser
import ast

class CalendarSynchronizer():


	_vcal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:{0}
DTSTAMP:{1}
DTSTART:{2}
DTEND:{3}
SUMMARY:{4}
DESCRIPTION:{5}
LOCATION:{6}
END:VEVENT
END:VCALENDAR
"""

	# Caldav url
	_url = config.url_calendar


	def get_available_nodes(self):
		listNodes = ast.literal_eval(config.node_list)
		nodes = []
		for node in listNodes:
			print node
			nodeModel = Node(node['id'],node['name'])
			print nodeModel
			nodes.append(nodeModel)

		return NodeCollection(nodes)
	
	def get_calendars(self):

		remote_calendar_collection = self._get_remote_calendars()
		return CalendarCollection.from_remote_calendar(remote_calendar_collection)
	
	def register_calendar(self, calendar):
		
		remote_calendar = self._register_remote_calendar(calendar)
		return Calendar.from_remote_calendar(remote_calendar)

	def _get_remote_calendars(self):
		client = caldav.DAVClient(self._url)
		print "_get_remote_calendars(): Created client"
		principal = client.principal()
		print "_get_remote_calendars(): Created principal"
		calendars = principal.calendars()
		print "_get_remote_calendars(): len of calendars " , calendars
		if len(calendars) > 0:
			print "_get_remote_calendars(): There are calendars!!!"
		for calendar in calendars:
			print "_get_remote_calendars(): A calendar of type: %s" % calendar

		return calendars

	def _register_remote_calendar(self, calendar):

		client = caldav.DAVClient(self._url)
		principal = client.principal()
		remote_calendar = principal.make_calendar(name=calendar.name, cal_id= str(uuid.uuid1()))
		return remote_calendar

	
	def _filter_remote_events(self, remote_event_collection, node = None, start_date = None, end_date = None):
		if (start_date is not None):
			input_start = pytz.utc.localize(dateutil.parser.parse(start_date))
		if (end_date is not None):
			input_end = pytz.utc.localize(dateutil.parser.parse(end_date))
		
		filter_remote_event_collection = []
		for event in remote_event_collection:
			event.load()
			vobj = event.instance
			_dtstart = vobj.vevent.dtstart.value
			_dtend = vobj.vevent.dtend.value
			if (node is not None):
				if (node == vobj.vevent.location.value):
					if (start_date is None) and (end_date is None):
						filter_remote_event_collection.append(event)
					elif (start_date is not None) and (end_date is None):
						if (input_start < _dtstart):
							filter_remote_event_collection.append(event)
					elif (start_date is not None) and (end_date is not None):
						if (input_start < _dtstart) and ( _dtend < input_end):
							filter_remote_event_collection.append(event)

			elif (start_date is not None) and (end_date is None):
				if (input_start < _dtstart):
					filter_remote_event_collection.append(event)
			elif (start_date is not None) and (end_date is not None):
				if (input_start < _dtstart) and ( _dtend < input_end):
					filter_remote_event_collection.append(event)

		return filter_remote_event_collection

	def get_events(self, node = None, start_date = None, end_date = None):

		print node
		remote_event_collection = self._get_remote_events()
		if (node is not None) or (start_date is not None) or (end_date is not None):
			#apply the filter to the collection
			remote_event_collection = self._filter_remote_events(remote_event_collection, node, start_date, end_date)

		return EventCollection.from_remote_event(remote_event_collection)

	def get_event(self, eventId):
		remote_event = self._get_remote_event(eventId)
		if remote_event is None:
			return None
		else:
			return Event.from_remote_event(remote_event)

	def _get_remote_events(self):
		client = caldav.DAVClient(self._url)
		principal = client.principal()
		calendars = principal.calendars()

		if len(calendars) > 0:
			calendar = calendars[0]
			events = calendar.events()
		else:
			events = []
		return events	

	def _get_remote_event(self, eventId):
		events = self._get_remote_events()
		for event in events:
			event.load()
			vobj = event.instance
			if eventId == vobj.vevent.uid.value:
				return event
		return None

	def _register_remote_event(self, event):
		client = caldav.DAVClient(self._url)
		principal = client.principal()
		calendars = principal.calendars()

		if len(calendars) > 0:
			calendar = calendars[0]
			UID =uuid.uuid1()
			SUMMARY = event.summary
			DESCRIPTION = event.description
			LOCATION = event.location

			#parse Date
			input_start = dateutil.parser.parse(event.dtstart)
			input_end = dateutil.parser.parse(event.dtend)
			input_stamp = datetime.today()
			DTSTAMP = input_stamp.strftime("%Y%m%dT%H%M%SZ%z")
			DTSTART = input_start.strftime("%Y%m%dT%H%M%SZ%z")
			DTEND = input_end.strftime("%Y%m%dT%H%M%SZ%z") 

			vcal_parsed = self._vcal.format(UID,DTSTAMP,DTSTART,DTEND,SUMMARY,DESCRIPTION,LOCATION)
			print vcal_parsed

			new_event = calendar.add_event(vcal_parsed)
			return new_event
	
	def register_event(self, event):
		
		remote_event = self._register_remote_event(event)
		return Event.from_remote_event(remote_event)

	def _remove_remote_event(self, eventId, remote_event):
		if remote_event is not None:
			remote_event.load()
			vobj = remote_event.instance
			print vobj.vevent.uid.value
			if (eventId == vobj.vevent.uid.value):
				print ("////////////_remove_remote_event(): START/////////")
				print ("////////////Deleting event")
				print ("////////////eventRadicale summary")
				print vobj.vevent.summary.value
				print ("////////////eventRadicale dtstar")
				print vobj.vevent.dtstart.value
				print ("////////////eventRadicale dtstar")
				print vobj.vevent.dtend.value
				print ("////////////eventRadicale description")
				print vobj.vevent.description.value
				print ("////////////eventRadicale uuid")
				print vobj.vevent.uid.value
				print ("////////////eventRadicale LOCATION")
				print vobj.vevent.location.value
				remote_event.delete()
				print ("////////////deleted event")
				print ("////////////_remove_remote_event(). END/////////")
				return True
			else:
				return False
		else:
			return False

	def remove_event(self, eventId):
		remote_event = self._get_remote_event(eventId)
		return self._remove_remote_event(eventId,remote_event)