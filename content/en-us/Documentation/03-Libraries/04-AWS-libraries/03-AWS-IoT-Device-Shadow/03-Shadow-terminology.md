---
title: Shadow Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*Device Shadow Service Document*   
The Device Shadow Service Document is a JSON document maintained by the Shadow service in the Amazon 
Web Services (AWS) cloud. It is used to store and retrieve current state information for a device.

Example document:

```c
{  
    "state" : {
        "desired" : {
            "color" : "RED"
        },
        "reported" : {
            "color" : "GREEN"
        }
    },
    "metadata" : {
        "desired" : {
            "color" : {
                "timestamp" : 12345
            }
        },
        "reported" : {
            "color" : {
                "timestamp" : 12345
            }
        }
    },
    "version" : 10,
    "clientToken" : "UniqueClientToken",
    "timestamp": 123456789
}
```

*Device Shadow Service Document Properties*   
A device's shadow service document contains the following properties: 

+ `state`

+ `desired`

  The desired state of the device (thing). Applications can write to this portion of the document to 
  update the state of a thing without having to directly connect to a thing. An example state as shown 
  above is "color": "RED". 

+ `reported`

  The reported state of the thing is the current state. A thing writes to this section of the document 
  to report a new state. 

+ `metadata`

  Information about the data stored in the `state` section, such as timestamps (in Epoch time) for each 
  attribute in the `state` section. This enables you to determine when these sections were updated.

+ `timestamp`

  Indicates when the message was transmitted by AWS IoT. By using the timestamp in the message and the 
  timestamps for individual attributes in the `desired` or `reported` section, a thing can determine 
  how old an updated item is, even if it doesn't implement an internal clock.

+ `clientToken`

  A string which is unique to the device and that enables you to associate responses with requests in 
  an MQTT environment.

+ `version`

  The document version is incremented with each document update. It is used to ensure the version of 
  the document being updated is the most recent.


*Shadow Update*   
A Shadow Update operation creates a device's shadow (if it doesn't exist), or updates the contents of 
a device's shadow service document. Any content change is stored with a timestamp to show when it was 
last updated. Messages are sent to all subscribers with the difference between the `desired` and 
the `reported` state (delta). Things or apps that receive these messages can perform an action based 
on the difference between the `desired` and `reported` states. For example, a device can update its 
state to the desired state, or an app can update its UI to show the change in the device's state.


*Shadow Get*   
A Shadow Get operation retrieves the latest state stored in the device's shadow. For example, at startup, 
a device connects to AWS IoT Core to retrieve configuration data and the last state of operation. This 
method returns the full JSON document, including metadata.


*Shadow Delete*   
A Shadow Delete operation deletes a device's shadow, including all of its content. This removes the 
JSON document from the database. Once a Device Shadow has been deleted, it can't be restored, but a 
new Device Shadow (with the same name) can be created.


*Shadow Delta Callback*   
A Shadow Delta Callback returns the Shadow Delta State, a virtual state that contains the difference 
between the `desired` and `reported` states. Fields in the `desired` section that do not match 
the `reported` section are included in the Delta. Fields that are in the `reported` section and not 
in the `desired` section are not included in the delta. When a device's shadow is updated, and this 
results in a Shadow document with different `desired` and `reported` states, a message is published 
to the topic $aws/things/*`thing-name`*/shadow/update/delta.

This message contains only the difference between the `desired` and `reported` sections of the device's 
shadow document. Upon receiving this message, the device should decide whether to make the requested 
change. In the Shadow library, the delta state can be retrieved by registering a Shadow Delta Callback.


*Shadow Updated Callback*   
A Shadow Updated Callback returns a state document to this topic from AWS IoT whenever an update to 
the shadow is successfully performed:


$aws/things/*`thingName`*/shadow/update/documents

The JSON document will contain two primary nodes: `previous` and `current`. The `previous` node will 
contain the contents of the full shadow document before the update was performed while `current` will 
contain the full shadow document after the update is successfully applied. When the shadow is 
updated (created) for the first time, the `previous` node will contain `null`. In the Shadow library, 
the updated state document can be retrieved by registering a Shadow Updated Callback.
