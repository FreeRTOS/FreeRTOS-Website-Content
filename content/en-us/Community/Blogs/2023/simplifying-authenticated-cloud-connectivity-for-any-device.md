---
title: Simplifying Authenticated Cloud Connectivity for Any Device
date: 14 Dec 2023
feature: blog
authors:
  - ribarry
---
Introduction
------------


[Featured FreeRTOS IoT reference integrations](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations)
show how to integrate the [Long-Term Support (LTS) versions of FreeRTOS libraries](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)
with hardware enforced security to help create secure cloud connected devices. This blog describes how to use
Wi-Fi and Cellular connectivity modules that implement the
[AWS IoT ExpressLink
specification](https://aws.amazon.com/iot-expresslink/) (from here on, "ExpressLink") to achieve the same outcome even on microcontrollers (MCUs) too
small to run the software libraries.


ExpressLink simplifies connected device software, reducing RAM and ROM footprints. It also simplifies hardware
design, manufacturing, and device onboarding at scale. Onboarding refers to the process of connecting a device to
the correct cloud account when the device is first powered up.


IoT devices often use a host MCU to run application software, and a separate communication module to access Wi-Fi,
Bluetooth, or cellular networks. Some communication modules go further than just managing the wireless network and
provide higher level protocols, like a TCP/IP stack. More commonly, though, all the software needed for secure
authenticated cloud communication is linked with the application software, and runs on the host MCU. The orange
boxes in Figure 1 represent libraries typically used to create secure cloud connections.


[![Typical library set required for secure device-to-cloud IoT connectivity](/media/2023/typical-library-set.png)](/media/2023/typical-library-set.png)


**Figure 1 - Typical library set required for secure device-to-cloud
 IoT connectivity**

In Figure 1:


* MQTT is an application layer protocol often used to communicate with cloud hosted servers.
* TLS is the same Transport Layer Security protocol used to secure HTTPS connections.
* The key management and secure storage modules secure the private keys used for authentication
 and encryption.
* Provisioning is the mechanism used to allocate private keys and unique identities to devices,
 which is challenging when scaling production.


In Figure 2, you can see a host microcontroller executing this functionality, with the help of a Wi-Fi or
cellular module to connect to the network.


[![Executing security and connectivity software on a host microcontroller](/media/2023/executing-security-and-connectivity.png)](/media/2023/executing-security-and-connectivity.png)


**Figure 2 - Executing security and connectivity software on
 a host microcontroller**

Using an Operating System (OS) to encapsulate complex functionality into autonomous threads of execution,
called tasks, simplifies the interface between the libraries (orange) and application code (green). For
example, Figure 3 uses a real-time OS (RTOS) to encapsulate the MQTT protocol and the more complex over-the-air
(OTA) update state machine into their own tasks, which we refer to as agent (or daemon) tasks. Well-designed
agents are easily reusable and thread-safe. They make the application code simpler because the functionality
now running in the agents no longer needs to be designed into the application software's control flow. Agents
also hide low-level library dependencies, which Figure 3 just shows as "Middleware libraries".


[![Using multithreading to simplify interfaces](/media/2023/using-multithreading.png)](/media/2023/using-multithreading.png)


**Figure 3 - Using multithreading to simplify interfaces**

Agents are a helpful simplification, but ExpressLink goes much further by moving the security and connectivity
functionality from the host MCU to the connectivity module, which provides a further step change in simplicity.
The ExpressLink specification also mandates OTA update capabilities for both the ExpressLink module and the
host MCU.


Using ExpressLink removes the need for the application writer to configure or build the libraries, or learn
even the simplified agent API. Offloading all that functionality from the host MCU significantly decreases the
MCU's ROM and RAM requirements. ExpressLink also offloads cryptographic firmware validation, reducing the host
MCU's compute requirements.


ExpressLink simplifies hardware design further by mandating hardware backed secure storage for encryption
and authentication keys, offloading that requirement from the MCU hardware too.


[![Executing security and connectivity software on the communication module](/media/2023/executing-security-and-connectivity.2.png)](/media/2023/executing-security-and-connectivity.2.png)


**Figure 4 - Executing security and connectivity software on the
 communication module**

The ExpressLink specification defines an AT command set. To use the command set from the host MCU, you just
need a UART driver. With an automated onboarding process, all you have to do is write the string "AT+connect"
to the serial port to create a TLS encrypted and authenticated connection to the correct cloud account, even
when powering on for the first time, and without having supplied secrets to the device’s manufacturing supply
chain.


There is a [FreeRTOS IoT reference
integration that utilises ST's I-Cube-ExpressLink](/Documentation/03-Libraries/08-Featured-integrations/06-STM32-Expresslink) to connect both large and small MCUs to AWS. The smallest
MCU in this reference is the STM32G0, which has 32K of program space and 8K of RAM.
