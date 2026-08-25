---
title: FreeRTOS 202107.00 now includes the SNTP library for time information in IoT applications
created: 2021-07-23
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Tanmoy Sen](../author/stanmoy) on 23 Jul 2021

FreeRTOS [202107.00](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning##how-are-freertos-libraries-versioned) now includes the Simple 
Network Time Protocol (SNTP) client library to make it easier for developers to add support for time 
information in their FreeRTOS-based IoT applications. The SNTP client library, 
named [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP), is used to synchronize clocks between a device and the cloud.

You can use coreSNTP in IoT applications where devices need to display the time or use it in their business 
logic (e.g. control temperature and lighting). In addition, you can use the coreSNTP library to validate 
certificates during TLS handshakes with the cloud or, if required, generate signatures to authenticate cloud 
storage requests (e.g.  [SigV4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
signatures for HTTPs requests to Amazon Simple Storage Service). The SNTP functionality becomes especially 
important in IoT devices that cannot retain time and date information in the absence of external power (e.g. 
IoT devices that do not have real-time clock modules). For more details on the coreSNTP library, see 
the [readme](https://github.com/FreeRTOS/coreSNTP/blob/main/README.md).

Get started by downloading FreeRTOS source code from the [Downloads page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 
or [GitHub](https://github.com/FreeRTOS/FreeRTOS), and find more information on 
the [Libraries page](/Documentation/03-Libraries/01-Library-overview/Library-categories).


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers and 
embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
