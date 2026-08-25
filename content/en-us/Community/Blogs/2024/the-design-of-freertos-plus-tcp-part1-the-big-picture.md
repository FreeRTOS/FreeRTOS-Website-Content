---
title: "The Design of FreeRTOS-Plus-TCP: Part 1 - The Big Picture"
date: 24 Dec 2024
feature: blog
authors:
  - nnkamath
---

by [Nikhil Kamath](../author/nnkamath) on 24 Dec 2024


FreeRTOS-Plus-TCP has been a popular TCP/IP stack for embedded systems for many years. This blog series will provide a deep dive into FreeRTOS-Plus-TCP (v4.x.x), breaking down its architecture and inner workings into digestible pieces. While you can get your FreeRTOS-Plus-TCP application up and running without diving into these details, understanding how the stack interacts with your application code will provide valuable insights, especially when fine-tuning configuration options for better performance or customizing behavior for specific needs. This series assumes a basic understanding of networking concepts. If you need a refresher or are new to these concepts, we encourage you to check out our networking glossary:https://freertos.org/FreeRTOS-Plus/FreeRTOS_Plus_TCP/networking_basics.html. 

[ ![Figure1. FreeRTOS-Plus-TCP High Level Structure](/media/2024/FreeRTOS-Plus-TCP_High_Level_Structure.jpg)](/media/2024/FreeRTOS-Plus-TCP_High_Level_Structure.jpg)
*Figure1. FreeRTOS-Plus-TCP High Level Structure*


## Laying the Foundation


Before diving into the intricacies of TCP handshakes and packet journeys, let's establish a solid understanding of the fundamental building blocks. Imagine FreeRTOS-Plus-TCP as a well-organized team with specialized roles:


### The IP Task:

The leader of the team, coordinating all network activities. The IP task runs the TCP/IP stack. It:

* **Processes network events:**  Handles events from the NIC (Network Interface Card) driver (e.g., a new packet arrived) and the sockets API (e.g., an application wants to send data).
* **Manages timers:**  Keeps track of timeouts for various protocols (e.g., ARP cache entries, DHCP lease renewals, TCP retransmissions).
* **Handling Socket Requests:** The IP task receives socket requests from application tasks, made through the Sockets API. It processes these requests, managing the state of each socket, allocating and releasing network buffers, and ensuring thread-safe operation.


### The Sockets API:

The communication liaison between your application and the IP task. It offers functions like:

* **Create sockets:** Establish communication endpoints for sending and receiving data.
* **Send and receive data:** Transmit data to other devices or receive data from them.
* **Establish and manage TCP connections:** Connect to servers, listen for incoming connections, and accept connections from clients.

The Sockets API handles the low-level details of interacting with the IP task, allowing you to focus on your application logic.


### The Network Event Queue:

Imagine this as a well-organized queue outside the IP Task's office. Both the Network Interface (specifically, the Receive Task) and the Sockets API use this queue to deliver messages and requests to the IP Task. This ensures that the IP Task can handle all events in a structured, one-at-a-time manner, preventing any conflicts or mix-ups when multiple tasks want to use the network.


### FreeRTOS-Plus-TCP Protocol Suite:

The heart of the operation, containing the brains of the TCP/IP stack. It includes modules responsible for:

* **ARP (Address Resolution Protocol):**  Like a phone book, it translates IP addresses (logical addresses) to MAC addresses (physical addresses).
* **DHCP (Dynamic Host Configuration Protocol):** Automates IP configuration (getting your device's IP address, netmask, etc.) from a DHCP server.
* **ICMP (Internet Control Message Protocol):**  Manages error messages and the famous "ping" utility.
* **UDP (User Datagram Protocol):**  Handles connection-less datagram communication, where packets are sent without establishing a formal connection.
* **TCP (Transmission Control Protocol):** The workhorse for reliable, connection-oriented communication, employing:
    * **Sliding Window:**  Improves efficiency by allowing packets to arrive out-of-order and be reassembled in the correct sequence.
    * **Retransmissions:**  Ensures reliable delivery by resending lost or corrupted packets.
    * **Keep-Alive:**  Periodically checks if the connection is still alive. 
* **DNS (Domain Name System):** It translates human-readable domain names (like [www.freertos.org](http://www.freertos.org/)) to IP addresses.


### The Network Interface:

Think of this as the field agent, directly interacting with the physical network hardware (e.g., your Ethernet controller). Its tasks include:

* **The Network Interface Driver:** This software component acts as the translator between the FreeRTOS-Plus-TCP stack and the actual hardware (your Ethernet controller). It handles tasks like:
    * Sending and receiving Ethernet frames: The raw data packets that travel over the network.
    * Managing link status: Keeping track of whether the network cable is connected and the connection is active. 
    * Configuring hardware features: Initializing and configuring the network interface hardware, configuring and negotiating with PHY, setting up specific capabilities of your network hardware.
* **The Receive Task:** This dedicated task works tirelessly behind the scenes, constantly waiting for incoming network traffic:
    * Handling Network Interrupts: When a packet arrives, the hardware triggers an interrupt. This task jumps into action, grabbing the packet data to a network buffer and pushing it to the network event queue, which can be further processed by the IP task.  Additionally, the receive task analyzes the received packet's data to determine the most appropriate endpoint on the network interface to associate with the network buffer. During a transmit complete interrupt from hardware, the receive task releases the submitted network buffer to the pool of free buffers.
    * Periodic Network Check: If no interrupts occur for a certain period, the receive task performs a check to see if the network link is still up and running. It updates FreeRTOS+TCP's network status accordingly.
    * Preparing Data for the IP Task: The receive task neatly packages the data into a network buffer, a special container for holding network packets, and adds important metadata. It then sends this package to the IP task for further processing.


### Network Buffer Management: 

This is the logistics expert, efficiently managing the storage space for network packets. It provides:

* **A pool of network buffers:**  Think of these as containers for holding Ethernet frames. 
* **Functions for buffer allocation and release:** It ensures that buffers are readily available when needed and are recycled after use.


### Task Priorities and Thread Safety:

FreeRTOS-Plus-TCP is built with a focus on thread safety, meaning that it can handle multiple tasks using the network without things going haywire. The Network Event Queue is a key part of this, allowing the IP Task to process everything in order.

To keep things running smoothly, task priority recommended is:
**Highest Priority:** The Receive Task: This task gets top priority because it's responding directly to hardware interrupts. It needs to process incoming packets quickly so that the network interface is ready for the next packet.
**Medium Priority:** The IP Task: The IP Task is also crucial, but it handles more complex operations, so it runs at a slightly lower priority. This allows the Receive Task to do its job without interruption.
**Lowest Priority:** Application Tasks: Your application tasks, which use the Sockets API to send and receive data, run at the lowest priority. This prevents them from interfering with the time-sensitive network handling done by the higher-priority tasks.


## Following the Packet's Journey

Imagine you're sending a message from your FreeRTOS-Plus-TCP device:

1. Your application calls FreeRTOS_send() (for TCP) or FreeRTOS_sendto() (for UDP) to transmit data.
2. Sockets API Queues Request: The Sockets API packages the request, including the data and destination information, and sends it to the IP task via the network event queue. For TCP, the data is added to the socket's transmit buffer. For UDP (without zero-copy), the data is copied into a network buffer. With UDP zero-copy, the buffer is simply prepared for sending.
3. The IP task receives the request, examines the destination address, and potentially uses ARP to resolve the MAC address.
4. For TCP, the IP task retrieves a network buffer from the buffer management module and populates it with data from the TCP stream buffer. In the case of UDP, the network buffer is obtained directly through the socket API and is passed to the IP task, which utilizes it for further processing. 
5. The IP task passes the data and destination information to the appropriate protocol module (TCP or UDP).
6. The protocol module prepares the data for transmission:
    1. TCP: Divides the data into segments if it exceeds the Maximum Segment Size (MSS).
    2. UDP: Treats the data as a single datagram.
    3. Checksum Calculation: The protocol module (TCP or UDP) adds its header to the data. If checksum offloading is not enabled, the protocol module calculates and sets the checksum. If offloading is enabled, the NIC driver will handle checksum calculation. 
7. The IP task prepares the network buffer by adding the IP header, followed by the protocol data (TCP or UDP segment/datagram).
8. The network buffer is handed off to the NIC driver, which calculates the checksum (if enabled) and transmits the data as an Ethernet frame.

The receive process reverses these steps, with the NIC driver passing received frames to the IP task, which then decodes the data and delivers it to the application via the sockets API.


## Coming Up Next...


In the next post, we'll uncover how the IP task juggles events, timers, and keeps the entire FreeRTOS-Plus-TCP stack running smoothly.

Stay tuned!


## Acknowledgments

This blog would not have been possible without the support of my colleagues at AWS. I would like to especially thank Actory Ou and Tony Josi for their invaluable help with the diagrams and thorough reviews.
