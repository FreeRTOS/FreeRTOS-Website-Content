---
title: "OPC-UA over TSN with FreeRTOS"
date: 1 Nov 2023
feature: blog
authors:
  - stanmoy
---
At Smart Production Solutions (SPS) fair in Nuremberg in November 2022 a group of 8 partners - Analog
Devices, Arm, Amazon Web Services (AWS), B&R Industrial Automation, Lattice Semiconductor, Schneider
Electric, Texas Instruments and NXP - [announced](https://opcconnect.opcfoundation.org/2022/12/enabling-opc-ua-and-tsn-for-field-devices/) a working group to create a permissive and open
source Open Platform Communications United Architecture (OPC UA) over Time Sensitive Networking (TSN)
software package with FreeRTOS. Today, we make public the development project that aims to enable applications
to have consistent access to TSN capabilities offered in hardware. This project focuses first on supporting
customers using OPC UA at the industrial field level and follows the OPC UA Field eXchange (UAFX)
specifications.


For context, OPC UA is a machine-to-machine communication protocol used for industrial automation and
developed by the [OPC Foundation](https://opcfoundation.org/). TSN is a standard technology to provide deterministic communication on Ethernet, and is
managed by the Time-Sensitive Networking task group for [IEEE 802.1](https://en.wikipedia.org/wiki/IEEE_802.1). Although Ethernet is the most wide-spread
networking technology employed, it inherently operates on a best effort basis to deliver packets across
a network. TSN is a set of OSI layer 2 standards that make Ethernet deterministic. Ethernet headers are
used for routing decisions, therefore the Ethernet payload can be anything, not just IP packets. This
means that TSN can be used in any environment and can carry the payload of any industrial application.


It is estimated that more than 200 million industrial field devices will run OPC-UA/TSN by 2030,
growing from 3 million in 2025. These devices are part of smart sensors, actuators, and IOs and communicate
to similar devices, controllers, programmable logic controllers (PLCs) and SCADA systems. OPC-UA/TSN also
enables raw data to be sent directly or via edge appliances to the cloud for further processing, insights,
or higher level AI based services such as predictive maintenance.


Currently, the sensor data collection mechanisms and formats in industrial systems are fragmented. The
industrial data communication protocols such as Profibus, Modbus, EtherCat, etc. lack a common data format
and interoperability. The bespoke formats are not human-readable and need custom coding/decoding to extract
intelligence from machines and manufacturing facilities. The lack of interoperability locks customers into
vendor-specific solutions, with limited ability for their machines to communicate or synchronize with other
systems. In a multi-vendor plant, the lack of interoperability and common format makes it challenging for
the developer to implement high-level applications such as condition monitoring, line balancing, and predictive
maintenance. Secondly, developers have limited access to unfiltered (raw) data from sensors and actuators.
This unfiltered data is needed to create resilient machines and IIoT applications with high levels of accuracy.


Traditionally, these sensors and actuators are connected to microprocessor-based PLCs and controllers that
filter out the raw data and use the vendor-specific field-bus formats (e.g. Profinet, EtherCat, CCLink).
According to B&R, "PLCs share a fraction of the data available because source raw data is manipulated, omitted
or only alarms are retained." Field device data helps manufacturers provide basic services such as analytics
to their customers. However, since the unfiltered semantic sensor data is not easily accessible and never
reaches the cloud, customers find it challenging to create higher level services like predictive maintenance,
condition monitoring, and asset performance monitoring, or to use it for digital twin representation and
continuous insights.


Finally, to mitigate interoperability issues, customers and industrial vendors are moving to a common
communication framework such as OPC UA over TSN. OPC UA provides a standardized way to structure data, so
it provides semantics for any kind of asset. And TSN defines the common connectivity layer that provides
deterministic real-time communication across control and field devices. OPC-UA over TSN is designed as a real-time
Ethernet communication standard that provides open, deterministic, real-time communication between automation
systems.


In order for OPC UA to be adopted at field level at the same scale as existing industrial protocols,
the price of devices supporting OPC-UA and TSN needs to be on par with existing solutions. This requires the
availability of low-cost MCU and low-power FPGA SoC based devices that support OPC-UA/TSN. To that end,
silicon vendors such as TI, NXP, ADI, Lattice Semiconductor, Renesas, Hilscher, etc have started manufacturing
silicon chips embedding TSN capabilities to reduce the BOM cost by at least 50% for industrial field devices.
What is missing, however, is the software to make the development for field devices that incorporate TSN cost
competitive. Lack of an RTOS that abstracts the various silicon providers' hardware implementation of TSN
blocks medium and small industrial device manufacturers from focusing on bringing smart sensors and actuators
with OPC UA/TSN to market.


Project design objectives
-------------------------


Our goals for this phase of the project are to:


* Define the standard APIs in FreeRTOS-plus-TCP library to support TSN and best effort traffic.
* Design a multi-priority queue software architecture in the FreeRTOS-plus-TCP library to support TSN.
* Define a clear boundary between the FreeRTOS-plus-TCP stack and the TSN portable layer, which
 will be vendor specific and will be contributed by our Chip Vendor Partners.


FreeRTOS-plus-TCP Software Architecture
---------------------------------------


### Existing Architecture


Repo: [https://github.com/FreeRTOS/FreeRTOS-Plus-TCP](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP)

Latest Version: V4.0.0


In the existing design of the FreeRTOS+TCP stack, the IP task is designed as an event driven task. It
blocks (pends) with a timeout on a FreeRTOS queue, to which the application(s) and the network interface
post events. When an event is received (event posted in the queue), the IP-task unblocks and processes
those events. These events include:


* Transmit/Receive events from and to socket APIs
* IP stack timer events
* Other network events (such as network up and down events)


All events received in the queue are currently processed with the same priority (as there is only
one SW queue), regardless of the traffic type, socket configuration, protocol, etc.


[![](/media/2023/TSNExistingDesign.png)](/media/2023/TSNExistingDesign.png)

**Click to enlarge**

### Limitations in Current Architecture to support TSN


* There is no option in the existing stack to handle multi-priority traffic data.
* Three context switches (Application task to IP task and IP task to Network Driver task) may
make the transmit and receive latency non-deterministic for TSN operation.
* The FreeRTOS-plus-TCP idle task `PrvIPTask` currently has higher priority than the
application tasks. This will pose a problem as the TSN higher throughput may require application
tasks to be of higher priority than the idle task.
* Using the same Ethernet Driver task for both Transmit and Receive will pose a challenge for
high speed TSN throughput.


### Moving forward


We are working on advancing the FreeRTOS+TCP stack based on the following design principles:


1. **API**:
	1. Common APIs for both Best effort and TSN traffic.
	2. A new *"**xDomain**"* called *"**FREERTOS\_AF\_TSN***
	 to be introduced for "FreeRTOS\_socket" API for TSN traffic type.
2. **Traffic Separation layer**:
	1. A decode layer after the socket layer differentiates between Best Effort TCP traffic
	 and TSN traffic.
	2. The same layer also differentiates among various priority TSN traffic.
3. **Traffic priority and Multi Priority Queues**:
	1. Multi priority support to have deterministic traffic in layer 2.
	2. Support for traffic processing based on its priority.
	3. The stack can work in 2 modes:
		1. Only Best effort Traffic : Here the stack will work as a single queue system.
		2. Best Effort and TSN traffic : Here the required number of queues will be active
		 based on the number supported by the underlying hardware.
4. **Traffic Scheduling**:
	1. **Transmit**:
		1. The FreeRTOS-plus-TCP Stack will use a simple round-robin mechanism to flush the
		 queues to Hardware.
		2. The Hardware will be deciding the transmit and receive rates and FreeRTOS-plus-TCP
		 stack will maintain the hardware rate.
	2. Every queue will have a threshold value and whenever this value is reached the DMA will
	 transfer the data to the TSN MAC.
5. **Receive**:
	1. The TSN hardware will take care of prioritizing the packets based on the traffic priority.
### Block Diagram for transmit + receive


[![](/media/2023/FreeRTOS-Plus-TCP-MQ-TSN-Design.jpg)](/media/2023/FreeRTOS-Plus-TCP-MQ-TSN-Design.jpg)

**Click to enlarge**
#### Feedback from our partners


We are excited that this project can reduce the complexity of providing synchronized, scheduled, and
prioritized traffic with Ethernet TSN implemented on hardware by a diverse set of silicon. This makes
the software interoperable and easy to re-use, and lets device makers focus on their customer applications.
Our partners are equally excited.


> *"We are happy to see the upcoming solutions for OPC UA FX and TSN on FreeRTOS as it will help
> develop our products even more robust, real-time capable and at the same time IoT-enabled based on an
> industry-proven stack. Sharing R&D resources through this open source approach also lowers our initial
> investment and reduces time-to-market." - Stefan Schoenegger, Global Product Group Manager, Controls
> at B&R Industrial Automation.*


> *"At Schneider Electric, we aim for an open, unified, standards-based communication ecosystem that
> will bring consistency and interoperability across Industrial Automation. We are happy to support our
> partners in making this new solution based on FreeRTOS following the OPC UA FX and TSN standards. This
> will help develop the ecosystem and bring OPC UA FX and TSN down to the field level and to the small
> and medium end devices." – Florian FOUILLET, Industrial Communication Program director.*


In addition, Arm added features to X.509 certificate handling in MBed TLS in support for 802.1AR
specification. This effort was released as part of the MBedTLS 3.5.0. The code repository can be found [here](https://github.com/Mbed-TLS/mbedtls/tree/v3.5.0).


### Getting started and code contributions


You can get started and find more information in the FreeRTOS-plus-TCP
[GitHub repo's](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP) **tsn** branch. There will be separate repositories for partners for their
TSN-enabled chipset drivers.


We're looking forward to your continued feedback and contributions. One area for contributions is
regarding applications for configuring TSN devices. Netconf has been identified as the companion application
that can fulfill this need. Today Netconf could be utilized on Linux based devices but not on compute
and memory constrained devices such as microcontrollers and low-power FPGA based SoCs.


Visit the [FreeRTOS forums](https://forums.freertos.org/) if you have comments or requests!
