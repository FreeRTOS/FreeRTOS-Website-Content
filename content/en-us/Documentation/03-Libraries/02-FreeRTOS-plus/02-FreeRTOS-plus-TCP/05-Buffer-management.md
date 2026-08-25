---
title: TCP/IP Stack Network Buffers Allocation Schemes and their implication on simplicity, CPU load, and throughput performance
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Network Data Buffers

Data being sent to the network or received from the network is placed in network buffers. Network buffer 
descriptors hold information about network buffers. The descriptors are pre-allocated, whereas the network 
buffers themselves are allocated as they are needed.

The total number of descriptors is set by 
the [ipconfigNUM\_NETWORK\_BUFFER\_DESCRIPTORS](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/03-Configuration#ipconfignum_network_buffer_descriptors)
constant in FreeRTOSIPConfig.h. Pre-allocating the descriptors allows the application writer to limit 
the maximum number of network buffers that can exist at any one time in order to prevent memory exhaustion.

Different buffer allocation schemes suite different embedded applications, so FreeRTOS-Plus-TCP keeps 
the buffer allocation schemes as part of the TCP/IP stack's portable layer. At the time of writing, 
two example buffer allocation schemes are provided - each with different trade offs between simplicity, 
RAM usage efficiency, and performance. The two schemes are described on this page.

The C source files that implement the buffer allocation schemes are located in the 
FreeRTOS-Plus/FreeRTOS\_Plus\_TCP/portable/BufferManagement directory. Only one scheme can be used at a time.


## Buffer Allocation Schemes

### Scheme 1: Implemented by BufferAllocation\_1.c

**Description**

+ Ethernet buffers are statically allocated by the embedded Ethernet peripheral driver (at compile time). 
  This ensures the buffers can be aligned as required by the specific Ethernet hardware.

  BufferAllocation\_1.c calls vNetworkInterfaceAllocateRAMToBuffers(), which must be provided by the peripheral 
  driver. Information detailing the requirements of this function are provided in 
  the [Functions That Must Be Provided By The Port Layer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#vNetworkInterfaceAllocateRAMToBuffers) 
  section of the Embedded Ethernet Driver Porting documentation page.


**Attributes**

+ Fast run time performance.
+ Ethernet buffers can be allocated and freed from interrupts, allowing for more efficient embedded 
  Ethernet peripheral drivers.
+ Inefficient use of RAM - all the buffers are the same size making BufferAllocation\_1.c unsuitable 
  for some RAM constrained embedded systems.
+ More complex to configure and tune than the scheme implemented by BufferAllocation\_2.
+ Simpler to achieve any special buffer alignment requirements imposed by the embedded Ethernet peripheral DMA.
+ Requires support from the network interface driver (see the description bullet points above).


**Usage**

+ The ipconfigNUM\_NETWORK\_BUFFER\_DESCRIPTORS constant in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration) defines both the total number of descriptors and the total number of buffers.
+ The ipconfigNETWORK\_MTU constant (defined in 
[FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)) defines the size of each Ethernet buffer (the total size being the defined MTU size plus the number of bytes needed by the Ethernet header).


### Scheme 2: Implemented by BufferAllocation\_2.c

**Description**

+ Ethernet buffers of exactly the required size are dynamically allocated and freed as required. This 
  requires a fast memory allocation scheme that does not suffer from fragmentation - at the time of 
  writing it is recommended that [heap\_4.c or heap\_5.c](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) is used.


**Attributes**

+ Extremely easy to use.
+ Dynamic allocation results in slower run time performance when compared with the scheme implemented 
  by BufferAllocation\_1.c.
+ Ethernet buffers cannot be allocated and freed from interrupts, necessitating the use of deferred interrupt 
  handling tasks in embedded Ethernet peripheral drivers.
+ Very efficient RAM usage - only the exact amount of RAM required is allocated making BufferAllocation\_2.c 
  particularly suited for RAM constrained small embedded systems.


**Usage**

+ Ethernet buffers are allocated from the [FreeRTOS heap](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management). To avoid memory fragmentation 
  problems, BufferAllocation\_2.c can only be used reliably with a memory allocation scheme that combines 
  adjacent free blocks of heap memory (a coalescence algorithm). The FreeRTOS memory allocation schemes 
  implemented in heap\_4.c and heap\_5.c 
  are suitable. The memory allocation scheme implemented in heap\_3.c can also be used if the implementations 
  of the standard library's malloc() and free() handle fragmentation.
+ The TCP/IP stack will recover from a failed attempt to allocate a network buffer, however, as the standard 
  heap implementation is used such a failure will result in the malloc failed hook being called (if 
  configUSE\_MALLOC\_FAILED\_HOOK is set to 1 in FreeRTOSConfig.h).


--------

![](/media/2019/warning_icon.png)
FreeRTOS+UDP was removed from the FreeRTOS kernel download from FreeRTOS V10.1.0. See
the [FreeRTOS+TCP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), which can be configured for UDP only use, as
an alternative.


### Summary Bullet Points

- FreeRTOS-Plus-UDP has a very efficient zero copy architecture. Depending on the implementation of
  the [embedded Ethernet peripheral driver](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#creating_a_zero_copy_network_port_layer),
  and the user's choice of API calling semantics, Ethernet packets can be passed by reference from the
  receiving DMA buffer, through the stack, all the way back to the transmitting DMA buffer.

- Performance limiting factors:

  1. **Reentrancy**

     FreeRTOS-Plus-UDP is fully reentrant and thread aware, meaning the IP stack can be safely used by
     all the RTOS tasks simultaneously. The flexibility does however come with the small time penalty
     introduced by the message passing and context switching that is necessary to ensure accesses to
     the IP stack are serialised (happen in a controlled manner so as not to cause corruption).

  2. **Buffer Allocation**

     Data that is received by the embedded Ethernet (or other embedded networking) peripheral is placed
     into buffers that are pre-allocated by the IP stack. When the user sends a message the message contents
     are placed in a buffer that is allocated by the IP stack. Different buffer allocation schemes suite
     different embedded applications. FreeRTOS-Plus-UDP currently includes two buffer allocation schemes -
     each with different trade offs between simplicity, RAM usage efficiency, and performance. The two
     schemes are described on this page.


### Buffer Allocation Schemes

The C source files that implement the buffer allocation schemes are located in the
FreeRTOS-Plus/FreeRTOS-Plus-UDP/portable/BufferManagement directory. Only one scheme can be used at a time.


#### Scheme 1: Implemented by BufferAllocation\_1.c

+ *Description*

  + [Ethernet buffer descriptors](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#network_buffers_and_Ethernet_buffers) are
    statically allocated by the IP stack (at compile time).

  + Ethernet buffers are statically allocated by the embedded Ethernet peripheral driver (at compile time).
    This ensures the buffers can be aligned as required by the specific Ethernet hardware.

+ *Attributes*

  + Fast run time performance.
  + Ethernet buffers can be allocated and freed from interrupts, allowing for more efficient embedded
    Ethernet peripheral drivers.
  + Inefficient use of RAM - all the buffers are the same size making BufferAllocation\_1.c unsuitable for
    some RAM constrained embedded systems.
  + More complex to configure and tune than the scheme implemented by BufferAllocation\_2.
  + Simpler to achieve any special buffer alignment requirements imposed by the embedded Ethernet
    peripheral DMA.
  + Requires support from the network interface driver (see the *description* bullet points above).

+ *Usage*

  + The ipconfigNUM\_NETWORK\_BUFFERS constant (defined in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration))
    defines the total number of available buffers.
  + The ipconfigNETWORK\_MTU constant (defined in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)) defines
    the size of each Ethernet frame (the total size being the defined MTU size plus the number of bytes
    needed by the Ethernet header).


#### Scheme 2: Implemented by BufferAllocation\_2.c

+ *Description*

  + [Ethernet buffer descriptors](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#network_buffers_and_Ethernet_buffers) are
    statically allocated by the IP stack (at compile time). This allows the user to limit the total number
    of Ethernet frames that can exist at any time to prevent memory exhaustion.
  + Ethernet buffers of exactly the required size are dynamically allocated and freed as required.

+ *Attributes*

  + Dynamic allocation results in slower run time performance when compared with the scheme implemented
    by BufferAllocation\_1.c.
  + Ethernet buffers cannot be allocated and freed from interrupts, necessitating the use of deferred interrupt
    handling tasks in embedded Ethernet peripheral drivers.
  + Very efficient RAM usage - only the exact amount of RAM required is allocated making BufferAllocation\_2.c
    particularly suited for RAM constrained small embedded systems.
  + Easier to configure and tune than the scheme implemented by BufferAllocation\_1.


+ *Usage*

  + The ipconfigNUM\_NETWORK\_BUFFERS constant (defined in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)) defines
    the total number of available network buffer descriptors. The descriptors contain pointers to Ethernet
    buffers, but do not actually contain buffers themselves. Buffers are allocated as required.
  + Ethernet buffers are allocated from the [FreeRTOS heap](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management). To avoid memory fragmentation
    problems, BufferAllocation_2.c can only be used reliably with a memory allocation scheme that combines
    free blocks of heap memory (a coalescence algorithm). The FreeRTOS memory allocation scheme implemented
    in heap\_4.c is suitable.
  + The IP stack will recover from an attempt to allocate a network buffer failing because there is too little
    heap memory. Such a failure will however result in the malloc failed hook function being called (if
    configUSE\_MALLOC\_FAILED\_HOOK is set to 1 in FreeRTOSConfig.h).
