
import requests
from maintenance_calendar import config
##from flask import json

class ContextBrokerNotificator():

	_prefix_maintenance_id = 'maintenancecalendar:'
	_host_contex_broker = config.host_contex_broker
	_update_url= "/v1/updateContext"
	_token = 'ymDdO9IqHNIyjcNOQLtglqJocT3msZ'
	_header = {'X-Auth-Token': _token, 'Content-Type':'application/json', 'Accept':'application/json'}
	_payload_maintenance =  {'contextElements': [ {"type": "Node","isPattern": "false","id": "", 
			"attributes": [ {"name": "type_event", "type": "string","value": ""},{"name": "maintenance_description",
			"type": "string","value": ""}]}],"updateAction": "UPDATE"}
	_payload_uptimerequest =  {'contextElements': [ {"type": "UptimeRequest","isPattern": "false","id": "maintenancecalendar:UptimeRequest", 
			"attributes": [ {"name": "type_event", "type": "string","value": ""},{"name": "uptimerequest_description",
			"type": "string","value": ""}]}],"updateAction": "UPDATE"}

	NEW_EVENT = 'NEW'
	UPDATED_EVENT = 'UPDATED'
	DELETED_EVENT = 'DELETED'

	
	## To be clarify, we are using the token of the user, but it should be the provider token.
	## We need to see how to create a user for the Maintenace Calendar module (if it is possible)
	def __init__(self, token):
		self._token = token

	def notify_maintenance_event(self,  node,  type_event,  maintenance_description):

		##assign the node
		self._payload_maintenance['contextElements'][0]['id'] = self._prefix_maintenance_id + node

		##assign the type of event (New, Updated, Deleted)
		self._payload_maintenance['contextElements'][0]['attributes'][0]['value'] = type_event

		##assign the description
		self._payload_maintenance['contextElements'][0]['attributes'][1]['value'] = maintenance_description

		self._connect_to_context_broker(self._host_contex_broker + self._update_url, self._payload_maintenance)


	def notify_uptimerequests_event(self,  type_event,  uptimerequest_description):


		##assign the type of event (New, Updated, Deleted)
		self._payload_uptimerequest['contextElements'][0]['attributes'][0]['value'] = type_event

		##assign the description
		self._payload_uptimerequest['contextElements'][0]['attributes'][1]['value'] = uptimerequest_description

		self._connect_to_context_broker(self._host_contex_broker + self._update_url, self._payload_uptimerequest)

	def notify_event(self, event, type_event):
		if event.location == 'UptimeRequests':
			self.notify_uptimerequests_event(type_event, event.summary)
		else:
			self.notify_maintenance_event(event.location, type_event, event.summary)

	def _connect_to_context_broker(self,  url, payload):

		## if something happens during the connection with the Context Broker, we don't want to stop the execution. 
		## Hence, we will manage the error and introduce the trace to indicate this error.
		## Nevertheless, we should analize how to manage the peding notification, 
		## to be sure that all the registered people will realize of this notification. TO be completed

		try:
			print (payload)
			response = requests.post(url, headers= self._header, json=payload)

			if (response.status_code == 200):

				if (response.text.find('orionError')!=-1):
					print ("POST --> " + self._host_contex_broker + self._update_url)
					print ("Error status: " + response.text)
				else:
					print ("OK POST --> " + self._host_contex_broker + self._update_url)
			else:
				print ("POST --> " + self._host_contex_broker + self._update_url)
				print ("Error status: " + response.text)

		except Exception, e:
			## we control the error, and we will do necessary actions, for the moment only print the error to follow up.
			print ("Exception: ")
			print (e)
