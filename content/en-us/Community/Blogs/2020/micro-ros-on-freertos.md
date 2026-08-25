---
title: micro-ROS on FreeRTOS
created: 2020-09-02
feature: blog
categories:
  - Long term support
authors:
  - francesca-finocchiaro
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

Authors: [Francesca Finocchiaro](https://www.linkedin.com/in/francesca-finocchiaro-44b27b14b/) (eProsima), [Pablo Garrido-Sanchez](https://www.linkedin.com/in/pgarridosan/) (eProsima), [José Antonio Moral Parras](https://www.linkedin.com/in/joseamoral/) (eProsima) on 02 Sep 2020


## Introduction

The [Robot Operating System](https://www.ros.org/) (ROS) is an open source software framework for robotics
applications development. ROS 2 is the second generation of ROS, designed with a layered architecture
that separates the ROS client layers (RCL and RCLCPP/RCLCPY) from the ROS middleware layer (RMW). The
client layers provide the developer interface, whereas the RMW enables compatibility with different
interchangeable low-level communication protocols. The RMW is built on top of
the [Data Distribution Service](https://www.dds-foundation.org/) (DDS), a real-time publish/subscribe
protocol designed for safety critical systems. The layered approach allows developers to focus on their
application, rather than on the underlying details. [Foxy Fitzroy](https://index.ros.org/doc/ros2/Releases/Release-Foxy-Fitzroy/)
is the latest version available of ROS 2 at the time of writing.

[micro-ROS](https://micro-ros.github.io/) is [ROS 2](https://index.ros.org/doc/ros2/)’s younger sibling,
that is, a Robot Operating System that offers most of the appealing tools and functionalities of the fully
deployed ROS 2 ecosystem, combined with the remarkable capability of fitting into embedded and low-resource
devices. Traditionally, ROS has stopped at the microcontroller boundary, even though robots contain many
of them. They are usually integrated through serial protocols with tools like ROS-serial in older ROS
versions.

Wouldn’t it be nice to have all the power of ROS2 and the same API within a microcontroller? That is exactly
what micro-ROS provides –a ROS development ecosystem inside of the embedded parts of robotics systems.
micro-ROS allows developers to have a ROS 2 node running near the hardware level. This renders all hardware
peripherals to be available to the application, which enables it to directly interact with low-level
buses such as SPI or I²C to interface with sensors and actuators.

micro-ROS is a set of layered libraries that either directly reuse those of ROS 2 or adapt them to the
capabilities and needs of resource-constrained devices. Specifically, if we turn to the ROS 2 architecture,
the layers maintained by micro-ROS are the ROS Client Library (RCL), and the ROS Middleware Interface (RMW).
Also, the RCLCPP, which is a C++ abstraction layer on top of the RCL, is usable by micro-ROS application
components, even though most are interfaced directly with the RCL. This layer offers additional functionalities
with respect to that of ROS 2 in what is called the RCLC, a library written in C99 where features similar
to those provided by the RCLCPP, such as convenience functions or executors, are specifically designed
and developed to fit into microcontrollers.

![](/media/2020/eprosima_microros_stack-300x169.png)

This allows micro-ROS to be compliant with most embedded platforms, both at the hardware and at the
software levels.

However, what ultimately shapes the micro-ROS architecture is the RMW implementation, which is based
on a middleware library called [Micro XRCE-DDS](https://micro-xrce-dds.docs.eprosima.com/en/latest/).
Micro XRCE-DDS is a C/C++ implementation of the [DDS-XRCE](https://www.omg.org/spec/DDS-XRCE/1.0/Beta1/PDF)
(DDS for eXtremely Resource Constrained Environments) protocol as defined and maintained by
the [Object Management Group](https://www.omg.org/) (OMG).

As suggested by its name, DDS-XRCE is a wire protocol that allows bringing the Data-Centric
Publisher-Subscriber [DDS model](https://www.dds-foundation.org/) to the embedded world. DDS-XRCE relies
on a client-server architecture in which the clients are lightweight entities written in C99 that run
into low resource devices while the agents (a C++ 11 application) act as a bridge between the clients
and the DDS world. The DDS-XRCE protocol is in charge of passing requests and messages between these
two entities. The agent, in turn, is able to communicate with the DDS global data space by means of
the standard DDS wire protocol. In the DDS world, the agent acts on behalf of the clients by putting
them into communication with the rest of the DDS participants. This communication is mediated by client
proxies, mock DDS applications able to interact with DDS by means of all the standard DDS entities.
The agent keeps the clients’ state in its memory, such that the proxies stay alive even if the latter
get disconnected. The communication between agent and clients follows a request-response pattern, that
is, bidirectional and based upon operations and responses.

![](/media/2020/eprosima_microros_dds_topology-300x106.png)


## Why use FreeRTOS?

Thanks to their lightness, both the XRCE-DDS client library and micro-ROS are apt to run on top of Real-Time
Operating Systems, what allows them to comply with the time-critical requirements imposed by their typical
target applications, involving tasks that demand time-deadlines or deterministic responses.

Specifically, FreeRTOS has been one of the first [RTOSes](https://micro-ros.github.io/docs/concepts/rtos/)
to be supported by the micro-ROS project, and is therefore integrated into its software stack. This allows
reusing all the tools and implementations provided by the FreeRTOS community and partners. As the micro-ROS
software stack is modular, the exchange of software entities is expected and desired.

FreeRTOS is an ideal choice to develop micro-ROS and Micro XRCE-DDS applications.
First of all, it provides an independent solution for many different architectures and development tools,
it is written in a very clear and transparent way and has an already very large user-base, which ensures
that a large pool of FreeRTOS users will be able to integrate their applications with micro-ROS applications.
Also, it is an RTOS well known to be highly reliable. Crucially, FreeRTOS has minimal ROM, RAM and processing
overhead. Typically an RTOS kernel binary image will be in the region of 6K to 12K bytes. These memory
figures are ideal when it comes to minimizing the memory footprint of a micro-ROS application on an
MCU, because of resources competition with the RTOS.

In the following, we discuss several features offered by FreeRTOS and how micro-ROS makes profitable
use of them in order to optimize the desired functionalities of the different libraries composed in
its stack.


### Tasks and scheduler

FreeRTOS offers a minimum set of [task entities](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines) that, together
with the use of the scheduler, provide the necessary tools to implement determinism in the applications.
The micro-ROS client libraries (RCL, RCLC and RCLCPP) access the RTOS’ resources to have control over
the scheduling and power management mechanisms, thus offering the developer the possibility to optimize
the application.

The tasks offered by FreeRTOS are of two kinds: standard and idle tasks. The former are created by the
user and can be considered as applications on the RTOS. Crucially, a micro-ROS application is integrated
into the RTOS as one such task with a given [priority](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities).
[Idle tasks](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task),
on the other hand, are the tasks with lower priority and enter into run mode only when there is no other
task running. As micro-ROS primarily targets low consumption and IoT devices, these idle tasks and related
idle hooks are perfectly suitable for enabling deep-sleep states in MCUs. Thanks to the state-less XRCE-DDS
client implemented as micro-ROS middleware, these deep-sleep states can be memory volatile, that is,
deep-sleep modes with no RAM persistence are usable thanks to the connection oriented middleware wire
protocol.

Using the FreeRTOS scheduler, micro-ROS is able to manage its main task and the priorities of the tasks
in charge of the transport layers. Usually, tasks in charge of networking stack or serial interfaces
have to be preempted over the micro-ROS app.


### Memory management

Among the most desirable features offered by FreeRTOS, and very interesting for micro-ROS developers
and users, are [stack management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking)
and [static stacks creation](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) capabilities.
When dealing with micro-ROS’ tasks creation, usually stack allocation is a critical design decision.
FreeRTOS allows a fine-grain stack size management, which in turn allows the programmer to know how
much stack memory is being used during the execution of a program, or for example to decide if stack
memory allocation is present in static or dynamic memory and thus helping in the correct memory usage
of the MCU, a valuable resource in embedded systems. Crucially, a heavy stack consumer task as micro-ROS
can be provided with a static allocated stack, preventing future issues with heap and other tasks initialization.

In this regard, it is worthwhile mentioning that these memory management tools offer an ideal framework
for benchmarking micro-ROS’ and XRCE-DDS’ memory footprint. Concretely, a thorough stack consumption
analysis has been performed to assess the XRCE-DDS client memory consumption. The stack is the chunk
of memory unknown to the programmer before running an application. In order to measure it, the
FreeRTOS [uxTaskGetStackHighWaterMark()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)
function can be used, which returns the amount of stack that remains unused, during execution, when
the XRCE-DDS task stack is at its greatest value. By subtracting this value to the total stack one thus
obtains the stack peak used by the XRCE-DDS app. The results obtained with this methodology are summarized
in a report published here.

We also notice that, thanks to the pluggable [dynamic memory management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
approach used in FreeRTOS, micro-ROS has been able to complete the required interface for managing memory.
In this way, functions such as calloc() or realloc() have been implemented
using [heap\_4](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management/#heap_4c)
as reference. These functions have been wrapped before being fed to the micro-ROS memory management API in
order to profile the dynamic memory consumption.

Similar to the static memory case, FreeRTOS’ swappable dynamic memory management approach makes it especially
easy to perform dynamic memory profiling analysis in embedded systems. Indeed, while in other RTOSes the
dynamic (de)allocation functions are hidden deep inside of the RTOS or standard libraries, in FreeRTOS
they are exposed to the user and prone to customization, therefore easing the process of handling and
controlling dynamic memory usage.


### Transport resources

In the same way in which the client support libraries have access to FreeRTOS’ specific primitives and
functions such as scheduling mechanisms, the middleware implementation, Micro XRCE-DDS, requires accessing
the transport and time resources of the RTOS to operate properly. Regarding IP transports, in the specific
case of FreeRTOS, Micro XRCE-DDS makes use of an add-on that implements lwIP over this
RTOS. [lwIP](https://savannah.nongnu.org/projects/lwip/) (lightweight IP) is a widely used open-source
TCP/IP stack designed for embedded systems, aimed at cutting on resource usage, while still providing
a full-scale TCP stack. This makes the use of lwIP especially apt for the embedded systems and
resource-constrained environments targeted by micro-ROS.

Aside from the TCP/IP stack, lwIP has several other important parts, such as a network interface, an
operating system emulation layer, buffers and a memory management section. The operating system emulation
layer and the network interface allow the network stack to be transplanted into an operating system,
as it provides a common interface between lwIP code and the operating system kernel.

The [integration of FreeRTOS with lwIP](https://docs.aws.amazon.com/freertos/latest/portingguide/porting-lwip.html)
is designed from the ground up to have a standard and familiar interface – Berkeley sockets – and to
be thread-safe, which is intended to make it as easy to use as possible. Also, it keeps buffer management
in the portable layer.

Notice that the XRCE-DDS client also supports
the [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) network
stack. FreeRTOS-Plus-TCP is the official FreeRTOS extension library for TCP/IP stack protocol support.

Efforts have also been made to make FreeRTOS-Plus-TCP compatible with micro-ROS. This includes both support
for TCP and UDP connections, relying on the FreeRTOS-Plus-TCP API to implement the abstraction layer
required by the micro XRCE-DDS Client API to be able to communicate with an Agent using these protocols.

Also, it exists the possibility of using
FreeRTOS’ [time measurement functionalities](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers),
thus giving the XRCE-DDS library the ability to perform time-based tasks hiding the implementation from
the user.


### Posix extension

Another notable reason that allowed seamless and profitable integration of FreeRTOS into micro-ROS,
is the availability of a [POSIX extension](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX).
The Portable Operating System Interface (POSIX) is a family of standards specified by the IEEE Computer
Society for maintaining compatibility between operating systems. The FreeRTOS-Plus-POSIX layer provided
by FreeRTOS Labs implements a subset of the POSIX API.

Indeed, although the micro-ROS middleware has a low POSIX dependency (just clock\_gettime() function),
the whole micro-ROS stack has a higher dependency related to functionality and type definitions. Also,
since one of the principles underlying the micro-ROS project has been to port or reuse code of ROS 2
that is natively coded in Linux (a mostly POSIX-compliant OS), making use of an RTOS that offers compliance
at some degree with POSIX is manifestly beneficial, as the porting effort of the code is minimal.

To this end, functions such as [sleep()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/sleep.html)
and [usleep()](https://pubs.opengroup.org/onlinepubs/000095399/functions/usleep.html) are used. The
POSIX type definition dependencies of micro-ROS relies on some structs such as struct timeval or struct
timespec which are not defined in the FreeRTOS kernel. Files like types.h, signal.h or unistd.h are
also required in order to define some standard type definitions and structures.

In the case of errno.h, micro-ROS has to include some non-available definitions for the sake of the
compilation although they are not implemented in FreeRTOS-Plus-POSIX layer.

These definitions should be refactored inside the micro-ROS stack for giving FreeRTOS-Plus-POSIX full
compatibility, by making use of the [FreeRTOS-Plus-FAT](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT)
library. This way, advanced micro-ROS features which depend on filesystem support, such as logging mechanisms,
could be fully supported.


## Conclusion

In conclusion, FreeRTOS makes a lightweight and ideal RTOS over which running a micro-ROS application,
as it offers a wide range of desired features that are used at different levels by virtually all the
modular layers composing the micro-ROS stack.

As the users base of both micro-ROS and FreeRTOS is rapidly expanding and compelling use-cases pop up,
further integration of micro-ROS with the libraries offered by FreeRTOS and FreeRTOS-Plus is foreseen
in the very near future.

Among them, the exploitation of the [FreeRTOS-Plus-FAT](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT)
library appears especially desirable in order to add a virtual filesystem component that allows visualizing
and managing logging operations as in a fully deployed ROS 2 ecosystem.

Further leverage of the memory management tools described in the dedicated section is also envisioned
to extend the [memory profiling of the XRCE-DDS client](https://www.eprosima.com/index.php/resources-all/performance/micro-xrce-dds-memory-profiling)
to provide a similar analysis for the micro-ROS client.

Another future action planned by the micro-ROS project is that of adopting the certified version of
FreeRTOS, [SAFERTOS](https://www.highintegritysystems.com/safertos/).

Last but not least, it seems worthy to mention two highly successful cases of integration of FreeRTOS
with hardware relevant for micro-ROS’ tytpical target applications, namely that of the
capable [Crazyflie 2.1 drone](https://www.bitcraze.io/products/crazyflie-2-1/) and of
the [ESP32 MCU](https://www.espressif.com/en/products/socs/esp32). Indeed, the Crazyflie software makes
profitable use of several FreeRTOS’ tools and functions. A demo example of a micro-ROS application
working with FreeRTOS on this MAV can be appreciated [here](https://www.youtube.com/watch?v=UDnSpWhkfZQ&t=14s).
As for the second hardware, natively integrated with FreeRTOS and offering a ready-to-use Wi-Fi antenna
and Bluetooth function, a very recent [port of micro-ROS on this system](https://discourse.ros.org/t/micro-ros-porting-to-esp32/16101)
has been carried out.

Finally, a very complete guide of how to create and run your first micro-ROS application on FreeRTOS,
making use of an [Olimex STM32-E407](https://www.olimex.com/Products/ARM/ST/STM32-E407/open-source-hardware)
evaluation board, can be found [here](https://micro-ros.github.io/docs/tutorials/core/first_application_rtos/freertos/).


## About eProsima

[eProsima](http://www.eprosima.com/) is a company focused on network middleware with special attention
to the [OMG](http://www.omg.org/) (Object Management Group) standard
called [Data Distribution Service for Real-time systems (DDS)](https://www.eprosima.com/index.php/resources-all/dds-all).

eProsima main product is eProsima [Fast DDS](https://www.eprosima.com/index.php/products-all/eprosima-fast-dds),
a lightweight DDS open Source implementation, exposing direct access to the underlying protocol, the Real
Time Publish Subscribe (RTPS) Protocol.

eProsima is a key contributor of the Robotic Operating System (ROS) being **eProsima Fast DDS included
as the default middleware for [ROS 2](https://index.ros.org/doc/ros2/)**. Because of this and other
important contributions, eProsima has been selected to be a member of the **ROS2 Technical Steering
committee**, to drive the roadmap of this de facto standard robotic framework.

eProsima also leads the **[Micro-ROS project](https://micro-ros.github.io/)** to extend ROS2 to Microcontrollers
based on a new eProsima middleware product,
eProsima [Micro XRCE-DDS](https://eprosima.com/index.php/products-all/eprosima-micro-xrce-dds)
(eXtremely Resource Constrained Environments DDS), already adopted by the ROS community.


## About the author

![](https://secure.gravatar.com/avatar/ef089a655d66d85a31cc1c1a7e01a4ac?s=200&d=mm&r=g)
Francesca Finocchiaro, physicist by formation, holds a project manager role within eProsima. At present,
she is leading the micro-ROS team and coordinating the EU project at OFERA (http://www.ofera.eu/), which
developed and actively maintains micro-ROS.
[View articles by this author](../author/francesca-finocchiaro)

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
