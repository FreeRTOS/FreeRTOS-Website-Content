---
title: ICMPv6
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[ICMPv6](https://en.wikipedia.org/wiki/ICMPv6) stands for Internet Control Message Protocol version 6. 
It’s the IPv6 implementation of 
the [Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol) (ICMP). 
The ICMPv6 protocol defines various message types and formats which implement different IPv6 protocols 
such as [Neighbor Discovery Protocol](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol) (NDP).

FreeRTOS+TCP uses ICMPv6 messages as a framework to implement 
RA, [Neighbor Discovery Protocol](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol) (NDP) 
and ICMPv6 echo ping request/reply.

