---
title: Network Sockets
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


A [socket](http://en.wikipedia.org/wiki/Network_socket) is conceptually an end point for communication, 
and the [Berkeley sockets](https://en.wikipedia.org/wiki/Berkeley_sockets) API is the defacto cross 
platform standard API used to create, configure, read from, write to, and otherwise manage sockets.

A socket is identified using 
the [IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address)
of the network node, and the [port number](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number) 
within the network node.

If a network node wants to 
send [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) 
data onto the network it first creates a socket, then sends the data to that socket. If a network node 
wants to receive UDP data it first creates a socket on an address that is known by the node that will 
send the data, then reads the data from that socket.

If a network node wants to 
send [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP) data
onto the network it first creates a socket, connects that socket to a socket on a remote node, then sends 
the data to that socket. If a network node wants to receive TCP data it first creates a socket, then 
listens on that socket for incoming connections. When a connection is received it may (optionally)
create a new socket to handle the connection and then receive the data on the new socket - leaving 
the original socket listening for additional incoming connections.

It can be seen then that any one network node can be involved in multiple network conversations simultaneously - 
with a socket being used at each end of each unique conversation.

Sockets can also be used to send and receive broadcast and multicast communications - which are both a 
form of one to many communications.

The API function [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
is used to create a socket.

The [FreeRTOS-Plus-TCP networking tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
demonstrates how to use sockets.

