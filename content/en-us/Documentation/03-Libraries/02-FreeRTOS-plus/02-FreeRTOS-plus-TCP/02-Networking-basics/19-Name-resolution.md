---
title: Network Name Resolution
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


Addressing remote nodes using a 
raw [IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address)
is not always practical because:

* IP addresses can change.
* The IP address of a remote computer might not be known.
* IP addresses are not very memorable.

It is more convenient to address a remote node using a human readable name. The process of converting 
a human readable name into an IP address is called Name Resolution. FreeRTOS-Plus-TCP 
includes [DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/20-DNS), [LLMNR](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/22-LLMNR)
and [NBNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/23-NetBIOS) 
implementations for this purpose.

