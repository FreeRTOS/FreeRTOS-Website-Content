---
title: MQTT Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


*Broker/Server*   
The MQTT broker (or server) is the central server to which MQTT clients connect. The MQTT broker manages 
message topics. When a client publishes a message to a topic, the message broker sends a copy of the message 
to each of the clients that are subscribed to the topic.


*Topics*   
MQTT Messages are arranged in a hierarchy of topics that are addressed as UTF-8 strings. Levels in the 
topic hierarchy are separated by forward slash characters ('/') similar to how files are arranged on 
your local disk. Topic strings (paths) are used to access MQTT messages in the same way file paths 
are used to access files. 

Valid examples include:

"my\_house/family\_room/temperature" and "my\_house/kitchen/temperature".


*MQTT Payloads*   
MQTT payloads are the body of each MQTT message - the application data carried by the MQTT packet.  
The payload is data format agnostic and can support anything including text, images, binary numbers, etc.


*Publish*   
When a client publishes to a topic on the MQTT broker, it is updating the data associated with that 
topic on the broker, and publishing new messages for the topic’s subscribers (if any). There is no limit 
to the number of clients that can publish to a topic.  A message can only be published to one topic at a time.


*Subscribe*   
Once a client subscribes to a topic on the MQTT broker, it will receive all of the subsequent messages 
that have been published to the topic.    There is no limit to the number of clients that can subscribe 
to a topic.  Clients can subscribe to either a specific topic such as “my\_house/kitchen/temperature” 
or to a range of topics (Topic Wildcards). 


*Topic Filters*   
A topic filter is used by the client to define its subscription to topic(s).  A subscription’s topic filter 
can contain wild cards to subscribe to multiple topics. 


*Topic Wildcards*   
Topic Wildcards enable a single subscription to receive updates from multiple topics. 

The multi-level (‘#’) wildcard is used to specify all remaining levels of hierarchies and **must be 
the last character** in the topic subscription string. 

* If the client subscribes to “my\_house/#”, then the client will receive the messages published 
  to “my\_house/family\_room” and “my\_house/kitchen”.

* If the client subscribes to “my\_house/family\_room/#”, then the client will receive the messages 
  published to “my\_house/family\_room/temperature” and “my\_house/family\_room/humidity”.  However, 
  it would not receive any messages published to “my\_house/kitchen”.

The single level (‘+’) wildcard is used to match one topic level of hierarchy.  The single (‘+’) wildcard 
can be used more than once in the topic filter and in conjunction with the multi-level wildcard. 

* If the client subscribes to “my\_house/+/temperature”, then the client will receive the messages published 
  to both “my\_house/family\_room/temperature” and my\_house/kitchen/temperature”.

* If the client subscribes to “my\_house/+/temperature/#, then the client will receive the messages 
  published to both “my\_house/family\_room/temperature/sensor\_1” and “my\_house/kitchen/temperature/sensor\_2”


*Quality of Service (QoS)*   
Quality of Service ([QoS](https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/)) 
refers to the reliability of message delivery between the publisher and subscriber. MQTT defines three quality 
of service levels.

* QoS0 is the lowest reliability level and is defined as "at most once" delivery. QoS0 messages are the 
  fastest to send but do not guarantee delivery.  This is analogous to an UDP packet on an IP network – 
  the UDP/IP protocol does not guarantee that UDP packets will reach their intended destination.

* QoS1 is defined as "at least once" delivery. QoS1 messages are guaranteed to be delivered (if delivery 
  is feasible), but may get delivered multiple times (duplicated).

* QoS2 is the highest reliability level and is defined as "exactly once" delivery. QoS2 messages are 
  guaranteed to be delivered (if delivery is feasible) and guaranteed not to be duplicated.  QoS2 is 
  the safest but the slowest quality of service level.


*Clean and Persistent Sessions*   
A client can specify a connection to an MQTT broker as a 'clean session' or a 'persistent' session.

If a client disconnects from a clean session, the broker will delete the client’s subscriptions, and 
the client must re-create the subscriptions the next time it connects. The client will not receive any 
messages that were published while disconnected.

If a client disconnects from a persistent session, the broker will queue (remember) the client’s subscriptions, 
and the broker will store all non QoS0 messages that were published while the client was disconnected.  
When the client re-connects, its subscriptions are automatically re-established, and it will receive all 
of the messages that were published while disconnected.


*Last Will and Testament*   
The Last Will and Testament (LWT) message is an MQTT message used to notify other clients about an ungracefully 
disconnected client. Clients can get ungracefully disconnected if they are disconnected unexpectedly while 
an MQTT connection is active.

A Last Will and Testament message is a normal MQTT message that contains a topic, a QoS level and a payload.  
Each client can optionally specify its own LWT message when it connects to a broker.  The broker stores this 
message so that if the client disconnects ungracefully, the broker will send the disconnected client’s LWT 
message to all the other clients that are subscribed to that last will message topic. 
