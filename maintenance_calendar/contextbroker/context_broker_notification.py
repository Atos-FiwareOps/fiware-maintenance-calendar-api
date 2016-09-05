
import requests
from maintenance_calendar import config
from flask import json
import logging

log = logging.getLogger(__name__)


class ContextBrokerNotificator():

	#Context Broker parameters
	_prefix_maintenance_id = 'maintenancecalendar:'
	_host_contex_broker = config.host_contex_broker
	_update_url= "/v1/updateContext"
	_token = None
	_header = {'X-Auth-Token': '', 'Content-Type':'application/json', 'Accept':'application/json'}
	
	_payload_maintenance =  {'contextElements': [ {"type": "Node","isPattern": "false","id": "", 
			"attributes": [ {"name": "type_event", "type": "string","value": ""},{"name": "maintenance_description",
			"type": "string","value": ""}]}],"updateAction": "UPDATE"}
	_payload_uptimerequest =  {'contextElements': [ {"type": "UptimeRequest","isPattern": "false","id": "maintenancecalendar:UptimeRequest", 
			"attributes": [ {"name": "type_event", "type": "string","value": ""},{"name": "uptimerequest_description",
			"type": "string","value": ""}]}],"updateAction": "UPDATE"}

	NEW_EVENT = 'NEW'
	UPDATED_EVENT = 'UPDATED'
	DELETED_EVENT = 'DELETED'

	#token parameters
	_header_idm = {'Content-Type': 'application/x-www-form-urlencoded'}
	_payload_idm = {'grant_type':'password', 'username':config.user_context_broker, 'password':config.pwd_user_context_broker}

	_timeout = config.timeout_context_broker

	## This constructor is using the token of the user directly, so if the user has been registered in the Context Broker application (IdM), he could notify the event.
	## Nevertheless, this user token is managed by the FIDASH and this user will be register in the FIDASH. 
	## To avoid to syncronize the users, we have created another constructor to generate a token with the credentials in the Context Broken application (see __init__(self)).
	def __init__(self, token = None):
		
		if (config.active_context_broker=='True'):
			if token is None:
				## Generate the token with the credential of th user, who has been regestered in the Context Broker application in the IdM.
				if log.isEnabledFor(logging.DEBUG):
					log.debug("__init__: The token is generated with the Context Broker application in the IdM")
				self._token = self._get_token_context_broker()
			else:
				if log.isEnabledFor(logging.DEBUG):
					log.debug("__init__: The token of the user is used directly")
				self._token = token
		else:
			log.warning("__init__: The notification system is disabled. The system will not notify anything")

	def notify_event(self, event, type_event):

		if (config.active_context_broker=='True'):
			self._header['X-Auth-Token'] = self._token

			if event.location == 'UptimeRequests':
				self._notify_uptimerequests_event(type_event, event.summary)
			else:
				self._notify_maintenance_event(event.location, type_event, event.summary)
		else:
			log.warning("notify_event(): PLEASE review the configuration of the Context Broker, since the subscriber will not receive the notifications!!!!")


	def _notify_maintenance_event(self,  node,  type_event,  maintenance_description):

		##assign the node
		self._payload_maintenance['contextElements'][0]['id'] = self._prefix_maintenance_id + node

		##assign the type of event (New, Updated, Deleted)
		self._payload_maintenance['contextElements'][0]['attributes'][0]['value'] = type_event

		##assign the description
		self._payload_maintenance['contextElements'][0]['attributes'][1]['value'] = maintenance_description

		self._connect_to_context_broker(self._host_contex_broker + self._update_url, self._payload_maintenance)


	def _notify_uptimerequests_event(self,  type_event,  uptimerequest_description):

		self._header['X-Auth-Token'] = self._token

		##assign the type of event (New, Updated, Deleted)
		self._payload_uptimerequest['contextElements'][0]['attributes'][0]['value'] = type_event

		##assign the description
		self._payload_uptimerequest['contextElements'][0]['attributes'][1]['value'] = uptimerequest_description

		self._connect_to_context_broker(self._host_contex_broker + self._update_url, self._payload_uptimerequest)


	def _connect_to_context_broker(self,  url, payload):

		## if something happens during the connection with the Context Broker, we don't want to stop the execution. 
		## Hence, we will manage the error and introduce the trace to indicate this error.
		## Nevertheless, we should analize how to manage the peding notification, 
		## to be sure that all the registered people will realize of this notification. TO be completed

		try:
			if log.isEnabledFor(logging.DEBUG):
				log.debug("_connect_to_context_broker(): Payload --> " + str(payload))

			response = requests.post(url, headers= self._header, json=payload, timeout=self._timeout)
			#response = requests.post(url, headers=self._header, json=payload, timeout=5)

			if (response.status_code == 200):

				if (response.text.find('orionError')!=-1):
					log.warning("_connect_to_context_broker(): POST --> " + self._host_contex_broker + self._update_url)
					log.warning("_connect_to_context_broker(): Error status: " + response.text)
					log.warning("_connect_to_context_broker(): PLEASE review the error Status in order to fix the problems, since the subscriber might not be receiving the notifications!!!!")
					
				else:
					if log.isEnabledFor(logging.DEBUG):
						log.debug("_connect_to_context_broker(): OK POST --> " + self._host_contex_broker + self._update_url)
			else:
				log.warning("_connect_to_context_broker(): POST --> " + self._host_contex_broker + self._update_url)
				log.warning("_connect_to_context_broker(): Error status: " + response.text)
				log.warning("_connect_to_context_broker(): PLEASE review the error Status in order to fix the problems, since the subscriber might not be receiving the notifications!!!!")
				

		except Exception, e:
			## we control the error, and we will do necessary actions, for the moment only logging the error to follow up.
			log.warning("_connect_to_context_broker(): ERROR when connecting with the context broker - " + str(e))
			log.warning("_connect_to_context_broker(): PLEASE review the error in order to fix the problems, since the subscriber are not receiving the notifications!!!!")


	def _get_token_context_broker(self):

		#Method responsible of obtaining the token in order to create the notification in the Context Broker
		token = None
		try:
			if log.isEnabledFor(logging.DEBUG):
					log.debug("_get_token_context_broker(): Start to obtain the token")

			response = requests.post(config.url_idm, headers= self._header_idm, data=self._payload_idm, auth=(config.client_id_context_broker,config.client_secret_context_broker), timeout= self._timeout)

			if (response.status_code == 200):

				if log.isEnabledFor(logging.DEBUG):
					log.debug("_get_token_context_broker(): response: " + response.text)

				r = json.loads(response.text)
				
				token = r['access_token']

			else:
				log.warning("_get_token_context_broker(): POST --> " + config.url_idm)
				log.warning("_get_token_context_broker(): Error status: " + response.text)
				log.warning("_get_token_context_broker(): PLEASE review the error Status in order to fix the problems, since the infrastructure cannot create the notifications!!!!")		
		
		except Exception, e:
			## we control the error, and we will do necessary actions, for the moment only logging the error to follow up.
			log.warning("_get_token_context_broker(): ERROR when connecting with the IdM - " + str(e))
			log.warning("_get_token_context_broker(): PLEASE review the error in order to fix the problems, since the infrastructure cannot create the notifications!!!!")

		return token

