---
title: Introducing the FreeRTOS Cellular Library
created: 2020-12-14
feature: blog
categories:
  - Long term support
authors: 
  - luciodj
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Lucio Di Jasio](../author/luciodj) on 14 Dec 2020

We are happy to introduce a preview of a new FreeRTOS library designed to simplify the development of 
IoT applications that connect to the cloud using [cellular LTE-M technology](https://en.wikipedia.org/wiki/LTE-M). 
LTE-M, also known as Cat-M1, is a low-cost LPWAN technology developed by [3GPP](http://www.3gpp.org/) 
as part of Release 13 of the LTE standard, a component of the 
broad [5G technology](https://en.wikipedia.org/wiki/5G) umbrella. It is also a complementary technology 
to [NB-IoT](https://en.wikipedia.org/wiki/Narrowband_IoT), but it's faster with 1Mbps upload and download 
speeds and has a lower latency which makes it ideal for many command and control applications. By default, 
all LTE-M cellular modems are also backward compatible with 4G technologies (such as CAT1) and will fall 
back to 3G and 2G as necessary to ensure connectivity. 


## Making Cellular IoT Applications Easier

Most cellular modules implement a standard (ASCII - AT command) interface, over a serial port, suitable for 
use with most microcontrollers and FreeRTOS applications. Each microcontroller vendor implements the serial 
interface (UART) slightly differently and each cellular module vendor has differentiated, if only slightly, 
the command set (originally defined by the 3GPP standard) to expose the best/unique capabilities of its 
product. As a result, there is no quick way for developers to adopt cellular technology without committing 
to a specific hardware implementation and a lot of effort goes wasted in re-implementing the serial interface 
for each microcontroller and module pair. 

The FreeRTOS Cellular library comes to the rescue by separating the repetitive, undifferentiated code 
required to serialize the modules’ commands and to parse their replies, offering a simple 
unified [Application Programming Interface (API)](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface). This common 
interface makes it possible for you, the developer, to focus exclusively on the application logic, expediting 
development and providing a clean and trusted foundation to build upon. Applications using the Cellular 
library API will be freely portable across a variety of cellular modem vendors and models. At present, 
the FreeRTOS cellular library provides support for the following popular cellular 
modems: [Quectel BG96](https://www.quectel.com/product/lpwa-bg96-cat-m1-nb1-egprs/), [Sierra Wireless HL7802](https://www.sierrawireless.com/products-and-solutions/embedded-solutions/products/hl7802/), 
and [U-Blox Sara-R4](https://www.u-blox.com/en/product/sara-r4-series).


## Building the IoT Stack

[FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) offers a networking stack designed for IoT applications. Common connectivity 
technologies such as Ethernet, Wi-Fi and BLE have already been integrated with this stack, and a wide 
selection of boards featuring popular microcontrollers and wireless modules are supported in 
the [FreeRTOS Reference Integrations](https://devices.amazonaws.com/search?page=1&sv=freerto). The new 
cellular library was designed to fit in this stack by providing the transport layer, so to be interchangeable 
with the other connectivity options built upon TCP sockets.

![Figure 1 - A freeRTOS IoT application stack using the cellular library](/media/2020/Figure-1-Cellular-Blog.png)


## Developing and Testing Cellular IoT Applications

Thanks to the common stack design and flexibility of the FreeRTOS IoT libraries (such as coreMQTT, coreHTTP, 
corePKCS11, ...) it is now possible to migrate IoT applications, originally designed for other wireless 
connectivity solutions, to the cellular technology quickly and with minimal effort. It is also possible 
to design and test brand new cellular IoT applications faster by 
using [FreeRTOS Windows simulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW) 
and [Linux (POSIX) simulator](https://freertos.org/FreeRTOS-simulator-for-Linux.html). In fact, we have 
created a new [FreeRTOS Lab repository](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo) 
containing three (Visual Studio) projects, based on the FreeRTOS Windows simulator, requiring only a laptop 
and an evaluation kit for any of the three modems initially supported. You will find more information on 
how to setup the modems and build the demos in the FreeRTOS Cellular Demo [Getting started Guide](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/03-Cellular-interface-demo).

Additionally, three new FreeRTOS reference integrations have been qualified based on the FreeRTOS release 
202011.00 libraries and using the following 
kits: [STM32L4+ Discovery board](https://devices.amazonaws.com/detail/a3G0h0000087pwWEAQ/STM32L4+-Discovery-Kit-IoT-Node) 
and [STMODLTE](https://www.st.com/content/st_com/en/products/evaluation-tools/solution-evaluation-tools/communication-and-connectivity-solution-eval-boards/steval-stmodlte.html), 
Sierra Wireless [Sensor Hub AWS Kit](https://www.richardsonrfpd.com/Products/Product/SENSORHUB-AWS#) 
(featuring the Sierra Wireless HL7802 module), 
Nuvoton - [NuMaker IoT M487 board](https://devices.amazonaws.com/detail/a3G0h000000Tg9cEAC/NuMaker-IoT-M487), 
and Quectel [RFBG96 adapter](https://www.nuvoton.com/board/rf-bg96a/). You will find them listed in 
the [AWS Partners Device Catalog](https://devices.amazonaws.com/search?conn=lte-m&kw=LTE&page=1). 


## FreeRTOS Cellular Library Response

We are excited about the response to the new FreeRTOS Cellular library, which we built with feedback from 
the FreeRTOS community of partners, customers, and embedded developers. Here is what our partners had to say … 

<blockquote>
  <span className="content">
  "Integrating u-blox LTE-M and NB-IoT modules with the FreeRTOS cellular libraries further extends our 
  commitment to our customers who develop secure IoT and edge devices that are connected to AWS Cloud services." 
  </span>
  <span className="attribution">
  Harald Kröll, Product Manager, u-blox
  </span>
</blockquote>

<blockquote>
  <span className="content">
  "We are delighted at the introduction of the FreeRTOS cellular library with STM32L4+ Discovery Kit IoT 
  Node and Quectel BG96’s STEVAL-STMODLTE support because our customers will benefit from the great saving 
  in time and effort when developing cellular enabled IoT applications." 
  </span>
  <span className="attribution">
  Andre Dostie, Director of IoT Applications – Microcontroller Division Americas, STMicroelectronics, Inc.
  </span>
</blockquote>

<blockquote>
  <span className="content">
  "We're delighted to continue our long collaboration with AWS. The BG96 cellular module, already AWS 
  IoT Core qualified, featured on the AWS Partner Device Catalog and now integrated in the FreeRTOS 
  cellular library, makes it even easier for our customers to quickly connect to AWS cloud."
  </span>
  <span className="attribution">
  Alexander Bufalino, VP Marketing, Quectel Wireless Solutions.
  </span>
</blockquote>

<blockquote>
  <span className="content">
  "We are glad to see AWS launching the FreeRTOS cellular library with ready support for our HL7802 
  modules to address the needs of our mutual customers and expedite development of innovative IoT applications 
  connected to AWS cloud." 
  </span>
  <span className="attribution">
  Ashish Syal, Chief Engineer, Sierra Wireless
  </span>
</blockquote>


## Summary

You can find more information about the FreeRTOS cellular library [here](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface). We’ll 
keep adding implementations of the cellular interface for new and popular modems, but we welcome your 
contributions to expand the catalog of modems and to improve the functionality of the library. Refer 
to the [Cellular Library Porting Guide](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/02-Porting-guide) for further details. Stay tuned...

FreeRTOS is an MIT licensed open source, real-time operating system for microcontrollers and small microprocessors
that makes small, low-power edge devices easy to program, deploy, secure, connect, and manage.

You can get started by downloading source code 
from [FreeRTOS.org](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) or [GitHub](https://github.com/freertos/freertos) () 
and can find more information about the FreeRTOS, its libraries and demos on 
the [FreeRTOS User Guide](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction).
 
 
## About the author

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)   
Lucio is a Product Manager at Amazon Web Services. He has held various technical and marketing roles 
in the semiconductor industry for the past 20 years. As an opinionated and prolific author he has published 
numerous articles and technical books on programming for embedded control applications. Following his 
passion for flying, he has achieved both FAA and EASA private pilot licenses.   
[View articles by this author](../author/luciodj) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
