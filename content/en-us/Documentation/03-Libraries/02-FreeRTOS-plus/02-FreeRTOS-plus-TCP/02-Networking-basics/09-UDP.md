---
title: UDP
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[Ethernet packets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)
can carry [IP packets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol),
which in turn can carry UDP packets.

UDP standard for [User Datagram Protocol](http://en.wikipedia.org/wiki/User_Datagram_Protocol). UDP is 
used to send and receive data in connectionless packets called datagrams. The packets are considered 
connectionless because, unlike [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP) 
packets, they do not need to establish a connection to another network node before they can send or 
receive data.

The UDP protocol does not include a means of knowing if transmitted data ever reached its intended recipient. 
If such an acknowledgement is required then it must be provided by the application itself. For example,
an application might very crudely use separate UDP packets to echo received data back to the sender to let 
the sender know the data was received.

UDP is much faster, simpler, and requires less RAM than TCP.

See also [UDP Sockets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket).

