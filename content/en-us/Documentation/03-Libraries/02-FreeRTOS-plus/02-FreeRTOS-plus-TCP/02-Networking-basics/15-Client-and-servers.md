---
title: Client and Server
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### Client

Clients are applications that actively connect to remote applications in order to obtain a service from 
the remote application. The remote application is the Server.
 

### Server

Servers are applications that wait for and then reply to incoming requests from clients.
 
Clients need to locate servers, and the simplest way to achieve this is by having the server bind to a 
pre-agreed address (other more complex methods also exist).
 
Servers do not need to know the client's address in advance, they just send their replies to the address 
from which the client's request originated.  Therefore clients can (normally) bind to nearly any port 
number, although high port numbers in the range 0xC000 to 0xFFFF are reserved for use by FreeRTOS-Plus-TCP
itself, and many low port numbers are (by convention 
only) [reserved for common network services](http://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers).
 
The [standard echo service](http://en.wikipedia.org/wiki/Echo_Protocol) provides a convenient example. 
Echo servers simply echo back the data sent to them by clients. Echo servers use port 7 by convention. 
The sequence diagram below shows a socket being created and bound on both an echo client and an echo 
server, and then a single echo transaction between the client and the server (it should be noted that 
the sockets only need to be created and bound once, not for each transaction).
 
![network clients and servers](/media/2018/client_server.png)   
*A simple transaction between an echo client and an echo server*
 
