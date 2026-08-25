---
title: Port Number
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


Each single network node can run multiple applications that use the same network interface, and therefore 
use the same [IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address). 
For example, an RTOS application can run a TFTP server, an echo server and a Nabto client at the same 
time - all of which make use of 
the [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP)/[IP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol) 
stack. Different applications running on the same network node, and therefore at the same IP address, 
are identified by their port number.

The source and destination address of 
each [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP)
or [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP)
packet is therefore a combination of an IP address and a port number. The IP address identifies the node 
on the network and the port number identifies the application within the 
node (see [sockets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)).

In FreeRTOS-Plus-TCP the port number is unique across the system, so each port number can only be bound 
to a single socket across the entire system. This ensures that network code remains simple and communication 
is efficient and has a low memory footprint. 

