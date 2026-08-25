---
title: TCP
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[Ethernet packets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)
can carry [IP packets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol),
which in turn can carry TCP packets.

TCP stands for [Transmission Control Protocol](http://en.wikipedia.org/wiki/Transmission_control_protocol).
TCP is used to send and receive a stream of data on a pre-established connection. The TCP protocol itself 
takes care of setting up the connection, and ensuring that all transmitted data is received correctly.

TCP is more reliable than [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP),
but is more complex to use and requires more RAM. The additional RAM usage comes from, in part, the necessity 
to retain packets that have already been sent onto the network until they have been correctly acknowledged (in 
case the packets need to be retransmitted), and the need to assemble data that is split between multiple 
packets into a reliable stream.

See also [TCP Sockets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket).

