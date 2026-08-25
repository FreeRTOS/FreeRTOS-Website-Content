---
title: Shutting Down and Closing a TCP Socket
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

A TCP socket that is **not** connected can be closed using the [FreeRTOS_closesocket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/13-close)
API function.

A TCP socket that **is** connected should not be closed until the
connection has been shut down. To gracefully shut down a socket first
call [FreeRTOS_shutdown()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/12-shutdown),
then wait for read attempts on the socket to return -pdFREERTOS_ERRNO_EINVAL, indicating
that the socket is no longer connected.

The source code examples on both the [Sending TCP Data](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/06-Sending-TCP-data)
and the [Receiving TCP Data](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/07-Receiving-TCP-data) pages demonstrate a connected
socket being shut down then closed.

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
