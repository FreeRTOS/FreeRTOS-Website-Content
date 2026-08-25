---
title: MSS
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


MSS stands for [Maximum Segment Size](http://en.wikipedia.org/wiki/Maximum_Segment_Size). It
defines the maximum amount of data that can be sent or received in 
a [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP) 
or [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) 
packet. It differs from 
the [MTU](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/03-MTU) 
value in that its value only applies to the data size, not the frame size, so it excludes the Ethernet, 
IP, TCP or UDP protocol headers. The MSS is dependent on the MTU and the maximum number of options bytes.

The following is an [IPv4](https://en.wikipedia.org/wiki/Internet_Protocol_version_4) example MSS calculation 
starting from an MTU of 1526 bytes. The number of bytes consumed by the various headers contained within 
the frame are subtracted to get the MSS size:

```
1526  MTU size
 -14  Ethernet header size
 -20  IP protocol header size
 -20  TCP protocol header size
 -12  TCP options bytes
----
1460  MSS size
```

The following is an [IPv6](https://en.wikipedia.org/wiki/IPv6#Address_representation) example MSS calculation 
starting from an MTU of 1526 bytes. The number of bytes consumed by the various headers contained within 
the frame are subtracted to get the MSS size:

```
1526        MTU size
 -14        Ethernet header size
 -40        IPv6 protocol header size
 -${var}    IPv6 extension header size(optional)
 -20        TCP protocol header size
 -12        TCP options bytes
----
1440-${var} MSS size
```

In FreeRTOS-Plus-TCP the MSS value is set by the [ipconfigTCP\_MSS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigtcp_mss)
setting in FreeRTOSIPConfig.h. If ipconfigTCP\_MSS is not defined then it will be set to a default value 
of 1460.

In the above example the calculated MSS value of 1460 bytes is suitable for a local area network (LAN), 
but is probably too large for use across the Internet, where the MSS should be restricted to 1400 bytes 
for maximum reliability. Therefore if the IP address of a remote node is outside of the local network
(see [netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)),
then FreeRTOS-Plus-TCP will automatically set the MSS to the smallest of either 1400 or
the configured ipconfigTCP\_MSS value.

