#!/bin/bash

set -x 

# Script to inizialize the Orion Context broker instance with the structure of the notification for
# the UptimeRequest and the different nodes
IP_CONTEXT_BROKER='orion.lab.fiware.org'
TOKEN_CONTEXT_BROKER='obuPMF1cLEFBfWjhsz6EM4IllUUGYy'

echo 'Configuration of the Maintenance Calendar for notifications with:'
echo ' ***Context Borke IP:'$IP_CONTEXT_BROKER
echo ' ***Token:'$TOKEN_CONTEXT_BROKER


curl $IP_CONTEXT_BROKER:1026/v1/updateContext -s -S --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'X-Auth-Token:$TOKEN_CONTEXT_BROKER' -d @- <<EOF
{
    "contextElements": [
         {
            "type": "UptimeRequest",
            "isPattern": "false",
            "id": "maintenancecalendar:UptimeRequest",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "UptimeRequest"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "uptimerequest_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Spain2",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Spain"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Trento2",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Italy"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
         },
         {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Berlin2",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Germany"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Budapest2",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Hungary"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Crete",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Greece"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Gent",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Belgium"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Karlskrona2",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Sweden"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Lannion2",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "France"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Mexico",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Mexico"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
                {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:PiraeusN",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Greece"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:PiraeusU",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Greece"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
                {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Poznan",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Poland"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Prague",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Czech Republic"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
	{
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:SaoPaulo",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Brazil"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:SophiaAntipolis",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "France"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Stockholm2",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Sweden"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
	{
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Volos",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Greece"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Waterford",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Ireland"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        },
        {
            "type": "Node",
            "isPattern": "false",
            "id": "maintenancecalendar:Zurich",
            "attributes": [
	            {
	                "name": "event",
	                "type": "string",
	                "value": "Maintenance"
	            },
	            {
	                "name": "type_event",
	                "type": "string",
	                "value": "New"
	            },
	            {
	                "name": "location",
	                "type": "string",
	                "value": "Switzerland"
	            },
	            {
	                "name": "maintenance_description",
	                "type": "string",
	                "value": "Initial notification"
	            }
        	]
        }
    ],
    "updateAction": "APPEND"
}
EOF

