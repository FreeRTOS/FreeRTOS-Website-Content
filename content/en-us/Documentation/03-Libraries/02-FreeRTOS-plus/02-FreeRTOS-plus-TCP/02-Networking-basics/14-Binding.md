---
title: Binding
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


Each [socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
needs a unique address. As already stated, an address is the combination of 
an [IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address)
and a [port number](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number).

When a socket is created it assumes the IP address of the network node that created it. If a socket 
has an IP address but not a port number it is said to be 'unbound'. An unbound socket cannot receive 
data because it does not have a complete address.

When a socket has both an IP address and a port number it is said to be 'bound to a port', or 'bound 
to an address'. A bound socket can receive data because it has a complete address.

The process of allocating a port number to a socket is called 'binding'.

The API function [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind)
is used to bind a FreeRTOS-Plus-TCP socket to a port number.

If [ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigallow_socket_send_without_bind)
is set to 0 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
then FreeRTOS\_bind() must be used to bind a socket to a port number before
the socket can be used to either send or receive data. If
ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND is set to 1 in FreeRTOSIPConfig.h
then an unbound socket will be automatically bound to a port number the
first time it attempts to send data (for UDP sockets) or connect (for TCP
sockets), but can still only receive data after it
has been bound.

