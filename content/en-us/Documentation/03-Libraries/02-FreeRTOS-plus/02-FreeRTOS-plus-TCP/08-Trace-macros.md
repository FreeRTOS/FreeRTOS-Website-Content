---
title: TCP/IP Specific Trace Hook Macros
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

For Debugging and Optimising FreeRTOS-Plus-TCP Behaviour

**Also see the [Debug, Trace and Logging](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#LOGGING) settings in FreeRTOSIOConfig.h.**


### Description

Trace hook macros allow you to collect data while your FreeRTOS-Plus-TCP
application is running. The data can be used for both debugging and
optimisation purposes.

Key points of interest within the RTOS's TCP source code contain
macros that an application can define for the purpose of providing
application specific trace functionality. The application need only
implement the macros of interest - unimplemented macros will remain
empty (not generate any code) by default.

It is recommended to implement trace macros in a header file, then #include the header file at the bottom
of [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration).

The FreeRTOS-Plus-TCP example that runs in the Windows simulator (available
for download from this website) uses the
trace macros to collect TCP/IP stack run time information that can then be
viewed using the TCP/IP CLI interface.

The macros that can be defined are:

+ iptraceNETWORK\_DOWN()

  Called when the network driver indicates that the network connection has been lost (not implemented by all network drivers).

+ iptraceNETWORK\_BUFFER\_RELEASED( pxBufferAddress )

  Called when the network buffer at address pxBufferAddress is released back to the TCP/IP stack.

+ iptraceNETWORK\_BUFFER\_OBTAINED( pxBufferAddress )

  Called when the network buffer at address pxBufferAddress is obtained from the TCP/IP stack by an RTOS task.

+ iptraceNETWORK\_BUFFER\_OBTAINED\_FROM\_ISR( pxBufferAddress )

  Called when the network buffer at address pxBufferAddress is obtained from the TCP/IP stack by an interrupt service routine.

+ iptraceFAILED\_TO\_OBTAIN\_NETWORK\_BUFFER()

  Called when a task attempts to obtain a network buffer, but a buffer was not available even after any defined block period.

+ iptraceFAILED\_TO\_OBTAIN\_NETWORK\_BUFFER\_FROM\_ISR()

  Called when an interrupt service routine attempts to obtain a network buffer, but a buffer was not available.

+ iptraceCREATING\_ARP\_REQUEST( ulIPAddress )

  Called when the IP generates an ARP request packet.

+ iptraceARP\_TABLE\_ENTRY\_WILL\_EXPIRE( ulIPAddress )

  Called when an ARP request is about to be sent because the entry for the IP address ulIPAddress in the ARP
  cache has become stale. ulIPAddress is expressed as a 32-bit number in network byte order.

+ iptraceARP\_TABLE\_ENTRY\_EXPIRED( ulIPAddress )

  Called when the entry for the IP address ulIPAddress in the ARP cache is removed. ulIPAddress is expressed as
  a 32-bit number in network byte order.

+ iptraceARP\_TABLE\_ENTRY\_CREATED( ulIPAddress, ucMACAddress )

  Called when a new entry in the ARP table is created to map the IP address ulIPAddress to the MAC address
  ucMACAddress. ulIPAddress is expressed as a 32-bit number in network byte order. ucMACAddress is a pointer
  to an MACAddress\_t structure.

+ iptraceSENDING\_UDP\_PACKET( ulIPAddress )

  Called when a UDP packet is sent to the IP address ulIPAddress. ulIPAddress is expressed as a 32-bit number in network byte order.

+ iptracePACKET\_DROPPED\_TO\_GENERATE\_ARP( ulIPAddress )

  Called when a packet destined for the IP address ulIPAddress is dropped because the ARP cache does not
  contain an entry for the IP address. The packet is automatically replaced by an ARP packet. ulIPAddress is
  expressed as a 32-bit number in network byte order.

+ iptraceICMP\_PACKET\_RECEIVED()

  Called when an ICMP packet is received.

+ iptraceSENDING\_PING\_REPLY( ulIPAddress )

  Called when an ICMP echo reply (ping reply) is sent to the IP address ulIPAddress in response to an ICMP
  echo request (ping request) originating from the same address. ulIPAddress is expressed as a 32-bit number
  in network byte order.

+ traceARP\_PACKET\_RECEIVED()

  Called when an ARP packet is received, even if the local network node is not involved in the ARP transaction.

+ iptracePROCESSING\_RECEIVED\_ARP\_REPLY( ulIPAddress )

  Called when the ARP cache is about to be updated in response to the reception of an ARP reply. ulIPAddress
  holds the ARP message's target IP address (as a 32-bit number in network byte order), which may not be the
  local network node (depending on the [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration) settings).

+ iptraceSENDING\_ARP\_REPLY( ulIPAddress )

  An ARP reply is being sent in response to an ARP request from the IP address ulIPAddress. ulIPAddress is
  expressed as a 32-bit number in network byte order.

+ iptraceFAILED\_TO\_CREATE\_SOCKET()

  A call to FreeRTOS\_socket() failed because there was insufficient [FreeRTOS heap memory](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
  available for the socket structure to be created.

+ iptraceRECVFROM\_DISCARDING\_BYTES( xNumberOfBytesDiscarded )

  FreeRTOS\_recvfrom() is discarding xNumberOfBytesDiscarded bytes because the number of bytes received is
  greater than the number of bytes that will fit in the user supplied buffer (the buffer passed in as a
  FreeRTOS\_recvfrom() function parameter).

+ iptraceETHERNET\_RX\_EVENT\_LOST()

  Called when a packet received by the network driver is dropped for one of the following reasons: There is
  insufficient space in the network event queue (see the ipconfigEVENT\_QUEUE\_LENGTH setting
  in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)), the received packet has an invalid data length, or there
  are no network buffers available (see the ipconfigNUM\_NETWORK\_BUFFER\_DESCRIPTORS setting
  in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)). Note this macro is called by the network driver rather
  than the TCP/IP stack and may not be called at all by drivers provided by third parties.

+ iptraceSTACK\_TX\_EVENT\_LOST( xEvent )

  Called when a packet generated by the TCP/IP stack is dropped because there is insufficient space in the
  network event queue (see the ipconfigEVENT\_QUEUE\_LENGTH setting in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)).

+ iptraceNETWORK\_EVENT\_RECEIVED( eEvent )

  Called when the TCP/IP stack processes an event previously posted to the network event queue. eEvent will
  be one of the following values:

  * eNetworkDownEvent - The network interface has been lost and/or needs [re]connecting.

  * eNetworkRxEvent - The network interface has queued a received Ethernet frame.

  * eARPTimerEvent - The ARP timer expired.

  * eStackTxEvent - The software stack has queued a packet to transmit.

  * eDHCPEvent - Process the DHCP state machine. Note the events are defined by the private eIPEvent\_t
    type which is not generally accessible.

+ iptraceBIND\_FAILED( xSocket, usPort )

  A call to FreeRTOS\_bind() failed. usPort is the port number the socket xSocket was to be bound to.

+ iptraceDHCP\_REQUESTS\_FAILED\_USING\_DEFAULT\_IP\_ADDRESS( ulIPAddress )

  Called when the default IP address is used because an IP address could not be obtained from a DHCP.
  ulIPAddress is expressed as a 32-bit number in network byte order.

+ iptraceSENDING\_DHCP\_DISCOVER()

  Called when a DHCP discover packet is sent.

+ iptraceSENDING\_DHCP\_REQUEST()

  Called when a DHCP request packet is sent.

+ iptraceNETWORK\_INTERFACE\_TRANSMIT()

  Called when a packet is sent to the network by the network driver. Note this macro is called by the network
  driver rather than the TCP/IP stack and may not be called at all by drivers provided by third parties.

+ iptraceNETWORK\_INTERFACE\_RECEIVE()

  Called when a packet is received from the network by the network driver. Note this macro is called by
  the network driver rather than the TCP/IP stack and may not be called at all by drivers provided by third
  parties.

+ iptraceSENDING\_DNS\_REQUEST()

  Called when a DNS request is sent.

+ iptraceWAITING\_FOR\_TX\_DMA\_DESCRIPTOR()

  Called when a transmission at the network driver level cannot complete immediately because the driver is
  having to wait for a DMA descriptor to become free. Try increasing the configNUM\_TX\_ETHERNET\_DMA\_DESCRIPTORS
  setting in FreeRTOSConfig.h (if it exists for the network driver being used).

+ iptraceDHCP\_SUCCEDEED( ulOfferedIPAddress )

  Called when DHCP negotiation is complete and the IP address in ulOfferedIPAddress is offered to the device.

+ iptraceDROPPED\_INVALID\_ARP\_PACKET( pxARPHeader )

  Called when an ARP packet is dropped due to invalid protocol and hardware fields in the header at address pxARPHeader.

+ iptraceFAILED\_TO\_CREATE\_EVENT\_GROUP()

  Called when an event group could not be created, possibly due to insufficient heap space, during new socket creation.

+ iptraceMEM\_STATS\_CLOSE()

  Should be called by the application when the collection of memory statistics should be stopped.

+ iptraceMEM\_STATS\_CREATE( xMemType, pxObject, uxSize )

  Called when an object at address pxObject of type xMemType and size uxSize has been allocated from the heap.

+ iptraceMEM\_STATS\_DELETE( pxObject )

  Called when an object at address pxObject has been deallocated and the memory has been returned to the heap.

+ iptraceNETWORK\_INTERFACE\_INPUT( uxDataLength, pucEthernetBuffer )

  Called when a packet of length uxDataLength and with the contents at address pucEthernetBuffer has been received.

+ iptraceNETWORK\_INTERFACE\_OUTPUT( uxDataLength, pucEthernetBuffer )

  Called when a packet of length uxDataLength and with the contents at address pucEthernetBuffer has been sent.

+ iptraceNO\_BUFFER\_FOR\_SENDTO()

  Called when a call to FreeRTOS\_sendto() tries to allocate a buffer, but a buffer was not available even
  after any defined block period.

+ iptraceRECVFROM\_INTERRUPTED()

  Called when a blocking call to FreeRTOS\_recvfrom() is interrupted through a call to FreeRTOS\_SignalSocket().

+ iptraceRECVFROM\_TIMEOUT()

  Called when FreeRTOS\_recvfrom() gets no data on the given socket even after any defined block period.

+ iptraceSENDTO\_DATA\_TOO\_LONG()

  Called when the data requested to be sent using a call to FreeRTOS\_sendto() is too long and could not be sent.

+ iptraceSENDTO\_SOCKET\_NOT\_BOUND()

  Called when the socket used in the call to FreeRTOS\_sendto() is not already bound to a port.
