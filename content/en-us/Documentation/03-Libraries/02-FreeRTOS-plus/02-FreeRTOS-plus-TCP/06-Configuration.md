---
title: FreeRTOS-Plus-TCP Configuration
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

The FreeRTOSIPConfig.h header file

FreeRTOS-Plus-TCP applications must provide a FreeRTOSIPConfig.h header file - in which the parameters
described on this page can be defined.

The [Configuration Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/07-Configuration-examples) page demonstrates how to set key configuration
parameters for systems that need to minimise RAM consumption and systems that need to maximise throughput.


* Constants Affecting the TCP/IP Stack Task Execution Behaviour
  + [ipconfigEVENT\_QUEUE\_LENGTH](#ipconfigevent_queue_length)
  + [ipconfigIP\_TASK\_PRIORITY](#ipconfigip_task_priority)
  + [ipconfigIP\_TASK\_STACK\_SIZE\_WORDS](#ipconfigip_task_stack_size_words)
  + [ipconfigPROCESS\_CUSTOM\_ETHERNET\_FRAMES](#ipconfig_process_custom_ethernet_frames)
  + [ipconfigUSE\_NETWORK\_EVENT\_HOOK](#ipconfiguse_network_event_hook)

* Debug, Trace and Logging Settings
  See also [TCP/IP Trace Macros](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/08-Trace-macros).
  + [ipconfigCHECK\_IP\_QUEUE\_SPACE](#ipconfigcheck_ip_queue_space)
  + [ipconfigHAS\_DEBUG\_PRINTF](#ipconfighas_debug_printf-and-freertos_debug_printf) and FreeRTOS\_debug\_printf
  + [ipconfigHAS\_PRINTF](#ipconfighas_printf-and-freertos_printf) and FreeRTOS\_printf
  + [ipconfigINCLUDE\_EXAMPLE\_FREERTOS\_PLUS\_TRACE\_CALLS()](#ipconfiginclude_example_freertos_plus_trace_calls)
  + [ipconfigTCP\_IP\_SANITY()](#ipconfigtcp_ip_sanity)
  + [ipconfigTCP\_MAY\_LOG\_PORT](#ipconfigtcp_may_log_port-x-)
  + [ipconfigWATCHDOG\_TIMER()](#ipconfigwatchdog_timer)
  + [ipconfigHAS_ROUTING_STATISTICS](#ipconfighas_routing_statistics)

* Hardware and Driver Specific Settings
  + [ipconfigBUFFER\_PADDING and ipconfigPACKET\_FILLER\_SIZE](#ipconfigbuffer_padding-and-ipconfigpacket_filler_size)
  + [ipconfigBYTE\_ORDER](#ipconfigbyte_order)
  + [ipconfigDRIVER\_INCLUDED\_RX\_IP\_CHECKSUM](#ipconfigdriver_included_rx_ip_checksum)
  + [ipconfigDRIVER\_INCLUDED\_TX\_IP\_CHECKSUM](#ipconfigdriver_included_tx_ip_checksum)
  + [ipconfigETHERNET\_DRIVER\_FILTERS\_FRAME\_TYPES](#ipconfigethernet_driver_filters_frame_types)
  + [ipconfigETHERNET\_DRIVER\_FILTERS\_PACKETS](#ipconfigethernet_driver_filters_packets)
  + [ipconfigETHERNET\_MINIMUM\_PACKET\_BYTES](#ipconfigethernet_minimum_packet_bytes)
  + [ipconfigFILTER\_OUT\_NON\_ETHERNET\_II\_FRAMES](#ipconfigfilter_out_non_ethernet_ii_frames)
  + [ipconfigNETWORK\_MTU](#ipconfignetwork_mtu)
  + [ipconfigNUM\_NETWORK\_BUFFER\_DESCRIPTORS](#ipconfignum_network_buffer_descriptors)
  + [ipconfigUSE\_LINKED\_RX\_MESSAGES](#ipconfiguse_linked_rx_messages)
  + [ipconfigZERO\_COPY\_RX\_DRIVER](#ipconfigzero_copy_rx_driver)
  + [ipconfigZERO\_COPY\_TX\_DRIVER](#ipconfigzero_copy_tx_driver)
  + [ipconfigSUPPORT_NETWORK_DOWN_EVENT](#ipconfigsupport_network_down_event)

* TCP Specific Constants
  + [ipconfigIGNORE\_UNKNOWN\_PACKETS](#ipconfigignore_unknown_packets)
  + [ipconfigTCP\_HANG\_PROTECTION](#ipconfigtcp_hang_protection)
  + [ipconfigTCP\_HANG\_PROTECTION\_TIME](#ipconfigtcp_hang_protection_time)
  + [ipconfigTCP\_KEEP\_ALIVE](#ipconfigtcp_keep_alive)
  + [ipconfigTCP\_KEEP\_ALIVE\_INTERVAL](#ipconfigtcp_keep_alive_interval)
  + [ipconfigTCP\_MSS](#ipconfigtcp_mss)
  + [ipconfigTCP\_RX\_BUFFER\_LENGTH and ipconfigTCP\_TX\_BUFFER\_LENGTH](#ipconfigtcp_rx_buffer_length-and-ipconfigtcp_tx_buffer_length)
  + [ipconfigTCP\_TIME\_TO\_LIVE](#ipconfigtcp_time_to_live)
  + [ipconfigTCP\_WIN\_SEG\_COUNT](#ipconfigtcp_win_seg_count)
  + [ipconfigUSE\_TCP](#ipconfiguse_tcp)
  + [ipconfigUSE\_TCP\_TIMESTAMPS](#ipconfiguse_tcp_timestamps)
  + [ipconfigUSE\_TCP\_WIN](#ipconfiguse_tcp_win)
  + [ipconfigTCP\_SRTT\_MINIMUM\_VALUE\_MS](#ipconfigtcp_srtt_minimum_value_ms)

* UDP Specific Constants
  + [ipconfigUDP\_MAX\_RX\_PACKETS](#ipconfigudp_max_rx_packets)
  + [ipconfigUDP\_MAX\_SEND\_BLOCK\_TIME\_TICKS](#ipconfigudp_max_send_block_time_ticks)
  + [ipconfigUDP\_PASS\_ZERO\_CHECKSUM\_PACKETS](#ipconfigudp_pass_zero_checksum_packets)
  + [ipconfigUDP\_TIME\_TO\_LIVE](#ipconfigudp_time_to_live)

* Other Constants Effecting Socket Behaviour
  + [ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND](#ipconfigallow_socket_send_without_bind)
  + [ipconfigINCLUDE\_FULL\_INET\_ADDR](#ipconfiginclude_full_inet_addr)
  + [ipconfigSELECT\_USES\_NOTIFY](#ipconfigselect_uses_notify)
  + [ipconfigSOCK\_DEFAULT\_RECEIVE\_BLOCK\_TIME](#ipconfigsock_default_receive_block_time)
  + [ipconfigSOCK\_DEFAULT\_SEND\_BLOCK\_TIME](#ipconfigsock_default_send_block_time)
  + [ipconfigSOCKET\_HAS\_USER\_SEMAPHORE](#ipconfigsocket_has_user_semaphore)
  + [ipconfigSOCKET\_HAS\_USER\_WAKE\_CALLBACK](#ipconfigsocket_has_user_wake_callback)
  + [ipconfigSUPPORT\_SELECT\_FUNCTION](#ipconfigsupport_select_function)
  + [ipconfigSUPPORT\_SIGNALS](#ipconfigsupport_signals)
  + [ipconfigUSE\_CALLBACKS](#ipconfiguse_callbacks)

* Constants Affecting the ARP Behaviour
  + [ipconfigARP\_CACHE\_ENTRIES](#ipconfigarp_cache_entries)
  + [ipconfigARP\_STORES\_REMOTE\_ADDRESSES](#ipconfigarp_stores_remote_addresses)
  + [ipconfigARP\_USE\_CLASH\_DETECTION](#ipconfigarp_use_clash_detection)
  + [ipconfigMAX\_ARP\_AGE](#ipconfigmax_arp_age)
  + [ipconfigMAX\_ARP\_RETRANSMISSIONS](#ipconfigmax_arp_retransmissions)
  + [ipconfigUSE\_ARP\_REMOVE\_ENTRY](#ipconfiguse_arp_remove_entry)
  + [ipconfigUSE\_ARP\_REVERSED\_LOOKUP](#ipconfiguse_arp_reversed_lookup)

* Constants Affecting DHCP and Name Service Behaviour
  + [ipconfigDHCP\_FALL\_BACK\_AUTO\_IP](#ipconfigdhcp_fall_back_auto_ip)
  + [ipconfigDHCP\_REGISTER\_HOSTNAME](#ipconfigdhcp_register_hostname)
  + [ipconfigDNS\_CACHE\_ADDRESSES\_PER\_ENTRY](#ipconfigdns_cache_addresses_per_entry)
  + [ipconfigDNS\_CACHE\_ENTRIES](#ipconfigdns_cache_entries)
  + [ipconfigDNS\_CACHE\_NAME\_LENGTH](#ipconfigdns_cache_name_length)
  + [ipconfigDNS\_REQUEST\_ATTEMPTS](#ipconfigdns_request_attempts)
  + [ipconfigDNS\_USE\_CALLBACKS](#ipconfigdns_use_callbacks)
  + [ipconfigMAXIMUM\_DISCOVER\_TX\_PERIOD](#ipconfigmaximum_discover_tx_period)
  + [ipconfigUSE\_DHCP](#ipconfiguse_dhcp)
  + [ipconfigUSE\_DHCPv6](#ipconfiguse_dhcpv6)
  + [ipconfigUSE\_DHCP\_HOOK](#ipconfiguse_dhcp_hook)
  + [ipconfigUSE\_DNS](#ipconfiguse_dns)
  + [ipconfigUSE\_DNS\_CACHE](#ipconfiguse_dns_cache)
  + [ipconfigUSE\_LLMNR](#ipconfiguse_llmnr)
  + [ipconfigUSE\_NBNS](#ipconfiguse_nbns)
  + [ipconfigUSE\_MDNS](#ipconfiguse_mdns)

* Constants Affecting IP and ICMP Behaviour
  + [ipconfigUSE\_IPv4](#ipconfiguse_ipv4)
  + [ipconfigUSE\_IPv6](#ipconfiguse_ipv6)
  + [ipconfigFORCE\_IP\_DONT\_FRAGMENT](#ipconfigforce_ip_dont_fragment)
  + [ipconfigICMP\_TIME\_TO\_LIVE](#ipconfigicmp_time_to_live)
  + [ipconfigIP\_PASS\_PACKETS\_WITH\_IP\_OPTIONS](#ipconfigip_pass_packets_with_ip_options)
  + [ipconfigREPLY\_TO\_INCOMING\_PINGS](#ipconfigreply_to_incoming_pings)
  + [ipconfigSUPPORT\_OUTGOING\_PINGS](#ipconfigsupport_outgoing_pings)

* Constants Affecting ND Behaviour
  + [ipconfigND\_CACHE\_ENTRIES](#ipconfignd_cache_entries)

* Constants Affecting RA Behaviour
  + [ipconfigUSE\_RA](#ipconfiguse_ra)
  + [ipconfigRA_SEARCH_COUNT AND ipconfigRA_IP_TEST_COUNT](#ipconfigra_search_count-and-ipconfigra_ip_test_count)

* Constants Providing Target Support
  + [ipconfigHAS\_INLINE\_FUNCTIONS](#ipconfighas_inline_functions)
  + [ipconfigRAND32](#ipconfigrand32)
  + [ipconfigIS\_VALID\_PROG\_ADDRESS](#ipconfigis_valid_prog_address)
  + [ipconfigPORT\_SUPPRESS\_WARNING](#ipconfigport_suppress_warning)


* Backward Compatibility
  + [ipconfigCOMPATIBLE\_WITH\_SINGLE](#ipconfigcompatible_with_single)
  + [ipconfigIPv4\_BACKWARD\_COMPATIBLE](#ipconfigipv4_backward_compatible)


### Constants Affecting the TCP/IP Stack Task Execution Behaviour

#### ipconfigEVENT\_QUEUE\_LENGTH

A FreeRTOS queue is used to send events from application tasks to the IP stack. `ipconfigEVENT_QUEUE_LENGTH`
sets the maximum number of events that can be queued for processing at any one time. The event queue must
be a minimum of 5 greater than the total number of network buffers.


#### ipconfigIP\_TASK\_PRIORITY

The TCP/IP stack executes it its own RTOS task (although **any** application RTOS task can make use of
its services through the published sockets API). `ipconfigIP_TASK_PRIORITY` sets the priority of the RTOS
task that executes the TCP/IP stack.

The priority is a [standard FreeRTOS task priority](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities) so it can take any value
from 0 (the lowest priority) to (`configMAX_PRIORITIES - 1`) (the highest priority). `configMAX_PRIORITIES` is
a standard FreeRTOS configuration parameter defined in FreeRTOSConfig.h, not FreeRTOSIPConfig.h.

Consideration needs to be given as to the priority assigned to the RTOS task
executing the TCP/IP stack relative to the priority assigned to tasks that use the TCP/IP stack.


#### ipconfigIP\_TASK\_STACK\_SIZE\_WORDS

The size, in words (not bytes), of the stack allocated to the FreeRTOS-Plus-TCP RTOS task. FreeRTOS
includes [optional stack overflow detection](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking).


#### ipconfig\_PROCESS\_CUSTOM\_ETHERNET\_FRAMES

If ipconfigPROCESS\_CUSTOM\_ETHERNET\_FRAMES is set to 1, then the TCP/IP stack will
call [eApplicationProcessCustomFrameHook](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/55-eApplicationProcessCustomFrameHook) to process any
unknown frame, that is, any frame that expects ARP or IP.


#### ipconfigUSE\_NETWORK\_EVENT\_HOOK

If `ipconfigUSE_NETWORK_EVENT_HOOK` is set to 1 then FreeRTOS-Plus-TCP will call
the [network event hook](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/57-vApplicationIPNetworkEventHook) at the appropriate times.
If `ipconfigUSE_NETWORK_EVENT_HOOK` is not set to 1 then the network event hook will never be called.


### Debug, Trace and Logging Settings

#### Trace Macros

Information on the available TCP/IP stack trace macros is provided on a [separate page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/08-Trace-macros).


#### ipconfigCHECK\_IP\_QUEUE\_SPACE

A FreeRTOS queue is used to send events from application tasks to the IP
stack.  [ipconfigEVENT\_QUEUE\_LENGTH](#ipconfigevent_queue_length) sets the maximum number of events
that can be queued for processing at any one time. If `ipconfigCHECK_IP_QUEUE_SPACE` is set to 1 then
the `uxGetMinimumIPQueueSpace()` function can be used to query the minimum amount of free space that
has existed in the queue since the system booted.

```c
UBaseType_t uxGetMinimumIPQueueSpace( void );
```
*uxGetMinimumIPQueueSpace() function prototype*


#### ipconfigHAS\_DEBUG\_PRINTF and FreeRTOS\_debug\_printf

The TCP/IP stack outputs debugging messages by calling the FreeRTOS\_debug\_printf macro. To obtain
debugging messages set `ipconfigHAS_DEBUG_PRINTF` to 1, then define `FreeRTOS_debug_printf()` to a
function that takes a `printf()` style format string and variable number of inputs, and sends the formatted
messages to an output of your choice.

Do not define `FreeRTOS_debug_printf` if `ipconfigHAS_DEBUG_PRINTF` is set to 0.

The following code is taken from the [FreeRTOS-Plus-TCP example for the RTOS's Win32 simulator](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator),
which has the ability to output debugging messages to a UDP port, standard out, and to a disk file:


```c
/* Prototype for the function function that actually performs the output. */
extern void vLoggingPrintf( const char *pcFormatString, ... );


/* Set to 1 to print out debug messages. If ipconfigHAS_DEBUG_PRINTF is set to
   1 then FreeRTOS_debug_printf should be defined to the function used to print
   out the debugging messages. */
#define ipconfigHAS_DEBUG_PRINTF    0
#if( ipconfigHAS_DEBUG_PRINTF == 1 )
    #define FreeRTOS_debug_printf(X)    vLoggingPrintf X
#endif
```

Defining ipconfigHAS\_DEBUG\_PRINTF and FreeRTOS\_debug\_printf in FreeRTOSIPConfig.h

The function that performs the output (`vLoggingPrintf()` in the code above) must be reentrant.


#### ipconfigHAS\_PRINTF and FreeRTOS\_printf

Some of the TCP/IP stack demo applications generate output messages. The TCP/IP stack outputs these
messages by calling the FreeRTOS\_printf macro. To obtain the demo application messages set `ipconfigHAS_PRINTF`
to 1, then define `FreeRTOS_printf()` to a function that takes a `printf()` style format string and
variable number of inputs, and sends the formatted messages to an output of your choice.

Do not define `FreeRTOS_printf` if `ipconfigHAS_PRINTF` is set to 0.

The following code is taken from
the [FreeRTOS-Plus-TCP example for the RTOS's Win32 simulator](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator), which has
the ability to output application messages to a UDP port, standard out, and to a disk file:


```c
/* Prototype for the function function that actually performs the output. */
extern void vLoggingPrintf( const char *pcFormatString, ... );

/* Set to 1 to print out application messages. If ipconfigHAS_PRINTF is set to
   1 then FreeRTOS_printf should be defined to the function used to print
out the application messages. */
#define ipconfigHAS_PRINTF  0
#if( ipconfigHAS_PRINTF == 1 )
    #define FreeRTOS_printf(X)  vLoggingPrintf X
#endif
```
*Defining ipconfigHAS\_PRINTF and FreeRTOS\_printf in FreeRTOSIPConfig.h*

The function that performs the output (`vLoggingPrintf()` in the code above) must be reentrant.


#### ipconfigINCLUDE\_EXAMPLE\_FREERTOS\_PLUS\_TRACE\_CALLS

The macro `configINCLUDE_TRACE_RELATED_CLI_COMMANDS` can be defined in FreeRTOSConfig.h. When defined,
it will be assigned to `ipconfigINCLUDE_EXAMPLE_FREERTOS_PLUS_TRACE_CALLS`. It allows the inclusion of
a CLI for tracing purposes.


#### ipconfigTCP\_IP\_SANITY

The name of this macro is a bit misleading: it only checks the behaviour of the module BufferAllocation\_1.c.
It issues warnings when irregularities are detected.


#### ipconfigTCP\_MAY\_LOG\_PORT( x )

`ipconfigTCP_MAY_LOG_PORT( x )` can be defined to specify which port numbers should or should not be logged
by `FreeRTOS_lprintf()`. For example, the following definition will not generate log messages for ports 23 or 2402:

```c
#define ipconfigTCP_MAY_LOG_PORT(xPort) ( ( ( xPort ) != 23 ) && ( ( xPort ) != 2402 ) )
```
*Filtering Log Messages*


#### ipconfigWATCHDOG\_TIMER()

`ipconfigWATCHDOG_TIMER()` is a macro that is called on each iteration of the
IP task and may be useful if the application included watchdog type functionality
that needs to know the IP task is still cycling (although the fact that the IP
task is cycling does not necessarily indicate it is functioning correctly).

`ipconfigWATCHDOG_TIMER()` can be defined to perform any action desired by the
application writer. If `ipconfigWATCHDOG_TIMER()` is left undefined then it will be removed
completely by the pre-processor (it will default to an empty macro).


#### ipconfigHAS\_ROUTING\_STATISTICS

ipconfigHAS\_ROUTING\_STATISTICS enables the stack to do statistics in FreeRTOS\_Routing.c when it’s 
set to 1. It helps record the end-point matching status in memory at runtime. 


### Hardware and Driver Specific Settings

#### ipconfigBUFFER\_PADDING and ipconfigPACKET\_FILLER\_SIZE

Advanced driver implementation use only.

When the application requests a network buffer, the size of the network buffer is specified by the application
writer, but the size of the network buffer actually obtained is increased by `ipconfigBUFFER_PADDING` bytes.
The first `ipconfigBUFFER_PADDING` bytes of the buffer is then used to hold metadata about the buffer, and
the area that actually stores the data follows the metadata. This mechanism is transparent to the user as
the user only see a pointer to the area within the buffer actually used to hold network data.

Some network hardware has very specific byte alignment requirements, so `ipconfigBUFFER_PADDING` is provided
as a configurable parameter to allow the writer of the network driver to influence the alignment of the start
of the data that follows the metadata.


#### ipconfigBYTE\_ORDER

If the microcontroller on which FreeRTOS-Plus-TCP is running is big endian then `ipconfigBYTE_ORDER` must
be set to `pdFREERTOS_BIG_ENDIAN`. If the microcontroller is little endian then `ipconfigBYTE_ORDER` must
be set to `pdFREERTOS_LITTLE_ENDIAN`. The [Byte Order and Endian](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/25-Endian) section of the Embedded Networking
Basics and Glossary page provides an explanation of byte order considerations in IP networks.


#### ipconfigDRIVER\_INCLUDED\_RX\_IP\_CHECKSUM

If the network driver or network hardware is calculating the IP, TCP and UDP checksums of incoming packets,
and discarding packets that are found to contain invalid checksums, then set `ipconfigDRIVER_INCLUDED_RX_IP_CHECKSUM`
to 1, otherwise set `ipconfigDRIVER_INCLUDED_RX_IP_CHECKSUM` to 0.

Throughput and processor load are greatly improved by implementing drivers that make use of hardware checksum
calculations.

**Note:** From FreeRTOS-Plus-TCP V2.3.0, the length is checked in software even when it has already been
checked in hardware.

**Note:** If hardware supports checking TCP checksum only, the network interface layer should handle 
the same for other protocols, such as IP/UDP/ICMP/etc, and give the checksum verified packets to the 
FreeRTOS-plus-TCP stack.


#### ipconfigDRIVER\_INCLUDED\_TX\_IP\_CHECKSUM

If the network driver or network hardware is calculating the IP, TCP and UDP checksums of outgoing packets
then set `ipconfigDRIVER_INCLUDED_TX_IP_CHECKSUM` to 1, otherwise set `ipconfigDRIVER_INCLUDED_TX_IP_CHECKSUM`
to 0.

Throughput and processor load are greatly improved by implementing drivers that make use of hardware checksum
calculations.


#### ipconfigETHERNET\_DRIVER\_FILTERS\_FRAME\_TYPES

[Ethernet/hardware MAC addresses](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing) are used to address Ethernet frames.
If the network driver or hardware is discarding packets that do not contain a MAC address of interest then
set `ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES` to 1. Otherwise set `ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES`
to 0.

Throughput and processor load are greatly improved by implementing network address filtering in hardware.
Most network interfaces allow multiple MAC addresses to be defined so filtering can allow through the unique
hardware address of the node, the broadcast address, and various multicast addresses.


#### ipconfigETHERNET\_DRIVER\_FILTERS\_PACKETS

For expert users only.

Whereas `ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES` is used to specify whether or not the network driver or
hardware filters Ethernet frames, `ipconfigETHERNET_DRIVER_FILTERS_PACKETS` is used to specify whether or not
the network driver filters the IP, UDP or TCP data within the Ethernet frame.

The TCP/IP stack is only interested in receiving data that is either addresses to a socket (IP address and port
number) on the local node, or is a broadcast or multicast packet. Throughput and process load can be greatly
improved by preventing packets that do not meet these criteria from being sent to the TCP/IP stack. FreeRTOS
provides some features that allow such filtering to take place in the network driver. For
example, `xPortHasUDPSocket()` can be used as follows:

```c
if( ( xPortHasUdpSocket( xUDPHeader->usDestinationPort ) )
    #if( ipconfigUSE_DNS == 1 )/* DNS is also UDP. */
        || ( xUDPHeader->usSourcePort == FreeRTOS_ntohs( ipDNS_PORT ) )
    #endif
    #if( ipconfigUSE_LLMNR == 1 ) /* LLMNR is also UDP. */
        || ( xUDPHeader->usDestinationPort == FreeRTOS_ntohs( ipLLMNR_PORT ) )
    #endif
    #if( ipconfigUSE_NBNS == 1 ) /* NBNS is also UDP. */
        || ( xUDPHeader->usDestinationPort == FreeRTOS_ntohs( ipNBNS_PORT ) )
    #endif
   )
{
    /* Forward packet to the IP-stack. */
}
else
{
    /* Discard the UDP packet. */
}
```
*Example of filtering UDP packets*


#### ipconfigETHERNET\_MINIMUM\_PACKET\_BYTES

When the device is connected to a LAN, it is strongly recommended to give each outgoing packet a minimum
length of 60 bytes (plus 4 bytes CRC). The macro `ipconfigETHERNET_MINIMUM_PACKET_BYTES` determines the
minimum length. By default, it is defined as zero, meaning that packets will be sent as they are.


#### ipconfigFILTER\_OUT\_NON\_ETHERNET\_II\_FRAMES

If `ipconfigFILTER_OUT_NON_ETHERNET_II_FRAMES` is set to 1 then Ethernet frames that are not in Ethernet II
format will be dropped. This option is included for potential future IP stack developments.


#### ipconfigNETWORK\_MTU

The [MTU](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/03-MTU) is the maximum number of bytes the payload of a network frame can contain. For normal
Ethernet V2 frames the maximum MTU is 1500 (although a lower number may be required for Internet routing).
Setting a lower value can save RAM, depending on the buffer management scheme used.

If `ipconfigNETWORK_MTU` is not defined then the following defaults will be applied:

```c
#ifndef ipconfigNETWORK_MTU
    #ifdef( ipconfigUSE_TCP_WIN == 1 )
        #define ipconfigNETWORK_MTU      ( 1526 )
    #else
        #define ipconfigNETWORK_MTU      ( 1514 )
    #endif
#endif
```


#### ipconfigNUM\_NETWORK\_BUFFER\_DESCRIPTORS

`ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS` defines the total number of network buffer that
are available to the TCP/IP stack. The total number of network buffers is limited
to ensure the total amount of RAM that can be consumed by the TCP/IP stack is capped
to a pre-determinable value. How the storage area is actually allocated to the
network buffer structures is not fixed, but part of the portable layer. The simplest
scheme simply allocates the exact amount of storage as it is required.

More information on network buffers and network buffer descriptors is provided on the pages that
describe [porting FreeRTOS-Plus-TCP to other hardware](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) and
the [pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor) porting specific
API function.


#### ipconfigUSE\_LINKED\_RX\_MESSAGES

Advanced users only.

When `pconfigUSE_LINKED_RX_MESSAGES` is set to 1 it is possible to reduce CPU load during periods of
heavy network traffic by linking multiple received packets together, then passing all the linked packets
to the IP RTOS task in one go.


#### ipconfigZERO\_COPY\_RX\_DRIVER

Advanced users only.

If `ipconfigZERO_COPY_RX_DRIVER` is set to 1 then the network interface will assign network
buffers `NetworkBufferDescriptor_t::pucEthernetBuffer` to the DMA of the EMAC. When a packet is received, no
data is copied. Instead, the buffer is sent directly to the IP-task.  If the TX zero-copy option is disabled,
every received packet will be copied from the DMA buffer to the network buffer of type `NetworkBufferDescriptor_t`.


#### ipconfigZERO\_COPY\_TX\_DRIVER

Advanced users only.

If `ipconfigZERO_COPY_TX_DRIVER` is set to 1 then the driver
function [xNetworkInterfaceOutput()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#xNetworkInterfaceOutput) will always be
called with its `bReleaseAfterSend` parameter set to `pdTRUE` - meaning it is always the driver that is
responsible for freeing the network buffer and network buffer descriptor.

This is useful if the driver implements a zero-copy scheme whereby the packet data is sent directly from
within the network buffer (for example by pointing a DMA descriptor at the data within the network buffer),
instead of copying the data out of the network buffer before the data is sent (for example by copying the
data into a separate pre-allocated DMA descriptor). In such cases the driver needs to take ownership of the
network buffer because the network buffer can only be freed after the data has actually been transmitted -
which might be some time after the `xNetworkInterfaceOutput()` function returns. See the examples on
the [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) documentation page for
worked examples.


#### ipconfigSUPPORT\_NETWORK\_DOWN\_EVENT

Set to 1 if you want to receive eNetworkDown notification via the `vApplicationIPNetworkEventHook_Multi()` callback.

**Note:** Not all drivers support this feature. 


### TCP Specific Constants

#### ipconfigIGNORE\_UNKNOWN\_PACKETS

Normally TCP packets that have a bad or unknown destination will result in a RESET
being sent back to the remote host. If `ipconfigIGNORE_UNKNOWN_PACKETS` is set to
1 then such resets will be suppressed (not sent).


#### ipconfigTCP\_HANG\_PROTECTION

If `ipconfigTCP_HANG_PROTECTION` is set to 1 then FreeRTOS-Plus-TCP will mark a socket
as closed if there is no status change on the socket within the period of time
specified by `ipconfigTCP_HANG_PROTECTION_TIME`.


#### ipconfigTCP\_HANG\_PROTECTION\_TIME

If `ipconfigTCP_HANG_PROTECTION` is set to 1 then `ipconfigTCP_HANG_PROTECTION_TIME` sets
the interval in seconds between the status of a socket last changing and the
anti-hang mechanism marking the socket as closed.


#### ipconfigTCP\_KEEP\_ALIVE

Sockets that are connected but do not transmit any data for an extended period
can be disconnected by routers or firewalls that time out. This can be avoided
at the application level by ensuring the application periodically sends a packet.
Alternatively FreeRTOS-Plus-TCP can be configured to automatically send keep alive
messages when it detects that a connection is dormant. Note that, while having
FreeRTOS-Plus-TCP automatically send keep alive messages is the more convenient method,
it is also the least reliable method because some routers will discard keep alive
messages.

Set `ipconfigTCP_KEEP_ALIVE` to 1 to have FreeRTOS-Plus-TCP periodically send keep
alive messages on connected but dormant sockets. Set `ipconfigTCP_KEEP_ALIVE` to
0 to prevent the automatic transmission of keep alive messages.

If FreeRTOS-Plus-TCP does not receive a reply to a keep alive message then the
connection will be broken and the socket will be marked as closed. Subsequent
`FreeRTOS_recv()` calls on the socket will return `-pdFREERTOS_ERRNO_ENOTCONN`.


#### ipconfigTCP\_KEEP\_ALIVE\_INTERVAL

If `ipconfigTCP_KEEP_ALIVE` is set to 1 then `ipconfigTCP_KEEP_ALIVE_INTERVAL` sets
the interval in seconds between successive keep alive messages. Keep alive messages
are not sent at all unless `ipconfigTCP_KEEP_ALIVE_INTERVAL` seconds have passed
since the last packet was sent or received.


#### ipconfigTCP\_MSS

Sets the [MSS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/11-MSS) 
value (in bytes) for all TCP packets.

Note that FreeRTOS-Plus-TCP contains checks that the defined `ipconfigNETWORK_MTU` and `ipconfigTCP_MSS`
values are consistent with each other.


#### ipconfigTCP\_RX\_BUFFER\_LENGTH and ipconfigTCP\_TX\_BUFFER\_LENGTH

Each TCP socket has a buffer for reception and a separate buffer for transmission.

The default buffer size is (4 * ipconfigTCP\_MSS).

`FreeRTOS_setsockopt()` can be used with the `FREERTOS_SO_RCVBUF` and `FREERTOS_SO_SNDBUF`
parameters to set the receive and send buffer sizes respectively - but this must
be done between the time that the socket is created and the buffers used by the socket are
created. The receive buffer is not created until data is actually received, and the transmit buffer
is not created until data is actually sent to the socket for transmission.
Once the buffers have been created their sizes cannot be changed.

If a [listening socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
creates a new socket in response to an incoming connect
request then the new socket will inherit the buffers sizes of the listening socket.


#### ipconfigTCP\_TIME\_TO\_LIVE

Defines the [Time To Live](http://en.wikipedia.org/wiki/Time_to_live) TTL) values used in outgoing TCP packets.


#### ipconfigTCP\_WIN\_SEG\_COUNT

If `ipconfigUSE_TCP_WIN` is set to 1 then each socket will use a sliding window.
Sliding windows allow messages to arrive out-of order, and FreeRTOS-Plus-TCP uses
window descriptors to track information about the packets in a window.

A pool of descriptors is allocated when the first TCP connection is made. The
descriptors are shared between all the sockets. `ipconfigTCP_WIN_SEG_COUNT` sets
the number of descriptors in the pool, and each descriptor is approximately
64 bytes.

As an example: If a system will have at most 16 simultaneous TCP connections,
and each connection will have an Rx and Tx window of at most 8 segments, then
the worst case maximum number of descriptors that will be required is 256 ( 16 * 2 * 8 ).
However, the practical worst case is normally much lower than this as most
packets will arrive in order.


#### ipconfigUSE\_TCP

Set `ipconfigUSE_TCP` to 1 to 
enable [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP). 
If `ipconfigUSE_TCP` is set to 0 then 
only [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP)
is available.


#### ipconfigUSE\_TCP\_TIMESTAMPS

TCP time stamp functionality is available, but its usage is quite limited.
Time-stamps can only be used if the initial SYN packet contains the time-stamp
option. In most cases, the incoming connection won't have the time-stamp option set.

Set `ipconfigUSE_TCP_TIMESTAMPS` to 1 to include TCP time stamp functionality.
Set `ipconfigUSE_TCP_TIMESTAMPS` to 0 to exclude TCP time stamp functionality.


#### ipconfigUSE\_TCP\_WIN

Sliding Windows allows messages to arrive out-of-order.

Set `ipconfigUSE_TCP_WIN` to 1 to include [sliding window](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
behaviour in TCP sockets. Set `ipconfigUSE_TCP_WIN` to 0 to exclude sliding window behaviour in TCP sockets.

Sliding windows can increase throughput while minimising network traffic at the
expense of consuming more RAM.

The size of the sliding window can be changed from its default using the
`FREERTOS_SO_WIN_PROPERTIES` parameter to `FreeRTOS_setsockopt()`. The sliding window
size is specified in units of MSS (so if the MSS is set to 200 bytes then a
sliding window size of 2 is equal to 400 bytes) and must always be smaller than
or equal to the size of the internal buffers in both directions.

If a [listening socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
creates a new socket in response to an incoming connect
request then the new socket will inherit the sliding window sizes of the listening
socket.


#### ipconfigTCP\_SRTT\_MINIMUM\_VALUE\_MS

The minimum value of TCP Smoothed Round Trip Time (SRTT).

When measuring the Smoothed Round Trip Time (SRTT), the result will be rounded up to a minimum value. 
The default has always been 50 ms, but a value of 1000 ms is recommended (see RFC6298) because hosts 
often delay the sending of ACK packets with 200 ms. 


### UDP Specific Constants

#### ipconfigUDP\_MAX\_RX\_PACKETS

`ipconfigUDP_MAX_RX_PACKETS` defines the maximum number of packets that can exist
in the Rx queue of a UDP socket. For example, if `ipconfigUDP_MAX_RX_PACKETS` is
set to 5 and there are already 5 packets queued on the UDP socket then subsequent
packets received on that socket will be dropped until the queue length is less
than 5 again.


#### ipconfigUDP\_MAX\_SEND\_BLOCK\_TIME\_TICKS

Sockets have a send block time attribute. If `FreeRTOS_sendto()` is called but
a network buffer cannot be obtained, then the calling RTOS task is held in the Blocked
state (so other tasks can continue to executed) until either a network buffer
becomes available or the send block time expires. If the send block time expires
then the send operation is aborted.

The maximum allowable send block time is
capped to the value set by `ipconfigUDP_MAX_SEND_BLOCK_TIME_TICKS`. Capping the
maximum allowable send block time prevents a deadlock occurring when
all the network buffers are in use and the tasks that process (and subsequently
free) the network buffers are themselves blocked waiting for a network buffer.

`ipconfigUDP_MAX_SEND_BLOCK_TIME_TICKS` is specified in RTOS ticks. A time in
milliseconds can be converted to a time in ticks by dividing the time in
milliseconds by `portTICK_PERIOD_MS`.


#### ipconfigUDP\_PASS\_ZERO\_CHECKSUM\_PACKETS

If `ipconfigUDP_PASS_ZERO_CHECKSUM_PACKETS` is set to 1 then FreeRTOS-Plus-TCP will accept UDP packets
that have their checksum value set to 0, which is in compliance with the UDP specification.

If `ipconfigUDP_PASS_ZERO_CHECKSUM_PACKETS` is set to 0 then FreeRTOS-Plus-TCP will drop UDP packets
that have their checksum value set to 0, which deviates from the UDP specification, but is safer.

**Note:** This configuration parameter defaults to 0.


#### ipconfigUDP\_TIME\_TO\_LIVE

Defines the [Time To Live](http://en.wikipedia.org/wiki/Time_to_live) (TTL) values used in outgoing UDP packets.


### Other Constants Effecting Socket Behaviour

#### ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND

The address of a socket is the combination of its IP address and its port number. [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind)
is used to manually allocate a port number to a socket (to 'bind' the socket to a port), but manual binding
is not normally necessary for client sockets (those sockets that initiate outgoing connections rather than
wait for incoming connections on a known port number). If `ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND` is set to 1
then calling `FreeRTOS_sendto()` on a socket that has not yet been bound will result in the IP stack automatically
binding the socket to a port number from the range `socketAUTO_PORT_ALLOCATION_START_NUMBER` to 0xffff.
If `ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND` is set to 0 then calling `FreeRTOS_sendto()` on a socket that has
not yet been bound will result in the send operation being aborted.


#### ipconfigINCLUDE\_FULL\_INET\_ADDR

Implementing [FreeRTOS\_inet\_addr()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/22-inet_addr) necessitates the use of string handling
routines, which are relatively large. To save code space, the full `FreeRTOS_inet_addr()`
implementation is made optional, and a smaller and faster alternative called
`FreeRTOS_inet_addr_quick()` is provided. `FreeRTOS_inet_addr()` takes an IP in
decimal dot format (for example, "192.168.0.1") as its parameter.
`FreeRTOS_inet_addr_quick()` takes an IP address as four separate numerical octets
(for example, 192, 168, 0, 1) as its parameters. If
`ipconfigINCLUDE_FULL_INET_ADDR` is set to 1, then both `FreeRTOS_inet_addr()` and
`FreeRTOS_indet_addr_quick()` are available. If `ipconfigINCLUDE_FULL_INET_ADDR` is
not set to 1, then only `FreeRTOS_indet_addr_quick()` is available.


#### ipconfigSELECT\_USES\_NOTIFY

This option is only used in case the socket-select functions are activated (when `ipconfigSUPPORT_SELECT_FUNCTION` is
non-zero). When calling `select()` for a given socket from the same task, this macro is not required. Only when there
are multiple tasks using select on the same sockets, this option *may* prevent a dead-lock. The problem is that the
event bit `eSELECT_CALL_IP` is waited for and cleared by multiple tasks. The macro `ipconfigSELECT_USES_NOTIFY`
defaults to zero, meaning not active.


#### ipconfigSOCK\_DEFAULT\_RECEIVE\_BLOCK\_TIME

API functions used to read data from a socket can block to wait for data to become
available. `ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` sets the default block time
defined in RTOS ticks. If `ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` is not defined
then the default block time will be set to `portMAX_DELAY` - meaning an RTOS task that
is blocked on a socket read will not leave the Blocked state until data is available.
Note that tasks in the Blocked state do not consume any CPU time.

`ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` is specified in ticks. The macros `pdMS_TO_TICKS()`
and `portTICK_PERIOD_MS` can both be used to convert a time specified in milliseconds to a time specified
in ticks.

The timeout time can be changed at any time using the `FREERTOS_SO_RCVTIMEO` parameter
with `FreeRTOS_setsockopt()`. **Note:** Infinite block times should be used
with extreme care in order to avoid a situation where all tasks are blocked
indefinitely to wait for another RTOS task (which is also blocked indefinitely) to
free a network buffer.

A socket can be set to non-blocking mode by setting both the send and receive
block time to 0. This might be desirable when an RTOS task is using more than one
socket - in which case blocking can instead by performed on all the sockets at
once using `FreeRTOS_select()`, or the RTOS task can set `ipconfigSOCKET_HAS_USER_SEMAPHORE`
to one, then block on its own semaphore.


#### ipconfigSOCK\_DEFAULT\_SEND\_BLOCK\_TIME

When writing to a socket, the write may not be able to proceed immediately. For
example, depending on the configuration, a write might have to wait for a network
buffer to become available. API functions used to write data to a socket can
block to wait for the write to succeed. `ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME` sets the default block time
(defined in RTOS ticks). If `ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME` is not defined,
then the default block time will be set to `portMAX_DELAY` - meaning an RTOS task that
is blocked on a socket read will not leave the Blocked state until data is available.
Note that tasks in the Blocked state do not consume any CPU time.

`ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` is specified in ticks. The macros `pdMS_TO_TICKS()`
and `portTICK_PERIOD_MS` can both be used to convert a time specified in milliseconds to a time specified
in ticks.

The timeout time can be changed at any time using the `FREERTOS_SO_SNDTIMEO` parameter
with `FreeRTOS_setsockopt()`. **Note:** Infinite block times should be used
with extreme care in order to avoid a situation where all tasks are blocked
indefinitely to wait for another RTOS task (which is also blocked indefinitely) to
free a network buffer.

A socket can be set to non-blocking mode by setting both the send and receive
block time to 0. This might be desirable when an RTOS task is using more than one
socket - in which case blocking can instead by performed on all the sockets at
once using `FreeRTOS_select()`, or the RTOS task can set `ipconfigSOCKET_HAS_USER_SEMAPHORE`
to one, then block on its own semaphore.

A socket can be set to non-blocking mode by setting both the send and receive
block time to 0.


#### ipconfigSOCKET\_HAS\_USER\_SEMAPHORE

By default, sockets will block on a send or receive that cannot complete
immediately. See the description of the `ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME`
and `ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME` parameters.

If an RTOS task is using multiple sockets and cannot block on one socket at a time, then
the sockets can be set into non-blocking mode, and the RTOS task can block on all the
sockets at once by either using the `FreeRTOS_select()` function or by setting
`ipconfigSOCKET_HAS_USER_SEMAPHORE` to 1, using the `FREERTOS_SO_SET_SEMAPHORE`
parameter with `FreeRTOS_setsockopt()` to provide a semaphore to the socket, and
then blocking on the semaphore. The semaphore will be given when any of the
sockets are able to proceed - at which time the RTOS task can inspect all the sockets
individually using non blocking API calls to determine which socket caused it to
unblock.


#### ipconfigSOCKET\_HAS\_USER\_WAKE\_CALLBACK

It is possible to install an application hook that will be called after every essential socket event. The hook has
one parameter: the socket, and it has no return value: `typedef void (* SocketWakeupCallback_t)( Socket_t pxSocket );`

The reason for calling the hook can be one or more of these events:

```c
        eSOCKET_RECEIVE = 0x0001, /* Reception of new data. */
        eSOCKET_SEND    = 0x0002, /* Some data has been sent. */
        eSOCKET_ACCEPT  = 0x0004, /* A new TCP client was detected, please call accept(). */
        eSOCKET_CONNECT = 0x0008, /* A TCP connect has succeeded or timed-out. */
        eSOCKET_BOUND   = 0x0010, /* A socket got bound. */
        eSOCKET_CLOSED  = 0x0020, /* A TCP connection got closed. */
        eSOCKET_INTR    = 0x0040, /* A blocking API call got interrupted, because
                                   * the function FreeRTOS\_SignalSocket() was called. */
```

Normally the hook will only notify the task that owns the socket so that the socket gets immediate attention.


#### ipconfigSUPPORT\_SELECT\_FUNCTION

Set `ipconfigSUPPORT_SELECT_FUNCTION` to 1 to include support for the [FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select)
and associated API functions, or 0 to exclude `FreeRTOS_select()` and associated
API functions from the build.


#### ipconfigSUPPORT\_SIGNALS

If `ipconfigSUPPORT_SIGNALS` is set to 1 then the `FreeRTOS_SignalSocket()` API
function is included in the build. [FreeRTOS\_SignalSocket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
can be used to send a signal to a socket, so that any task
blocked on a read from the socket will leave the Blocked state (abort the blocking read operation).


#### ipconfigUSE\_CALLBACKS

When this macro is defined as non-zero, it is possible to bind specific application hooks (callbacks)
to a socket. There is a different application hook for every type of event:

```c
    FREERTOS_SO_TCP_CONN_HANDLER /* Callback for (dis) connection events.
                                  * Supply pointer to 'F_TCP_UDP_Handler_t' */

    FREERTOS_SO_TCP_RECV_HANDLER /* Callback for receiving TCP data.
                                  * Supply pointer to 'F_TCP_UDP_Handler_t' */

    FREERTOS_SO_TCP_SENT_HANDLER /* Callback for sending TCP data.
                                  * Supply pointer to 'F_TCP_UDP_Handler_t' */

    FREERTOS_SO_UDP_RECV_HANDLER /* Callback for receiving UDP data.
                                  * Supply pointer to 'F_TCP_UDP_Handler_t' */

    FREERTOS_SO_UDP_SENT_HANDLER /* Callback for sending UDP data.
                                  * Supply pointer to 'F_TCP_UDP_Handler_t' */
```

### Constants Affecting the ARP Behaviour

#### ipconfigARP\_CACHE\_ENTRIES

The ARP cache is a table that maps IP addresses to MAC addresses.

The IP stack can only send a UDP message to a remove IP address if it knowns the MAC
address associated with the IP address, or the MAC address of the router used to
contact the remote IP address. When a UDP message is received from a remote IP
address, the MAC address and IP address are added to the ARP cache. When a UDP
message is sent to a remote IP address that does not already appear in the ARP
cache, then the UDP message is replaced by a ARP message that solicits the
required MAC address information.

`ipconfigARP_CACHE_ENTRIES` defines the maximum number of entries that can exist in the ARP table at any one time.


#### ipconfigARP\_STORES\_REMOTE\_ADDRESSES

Advanced users only.

`ipconfigARP_STORES_REMOTE_ADDRESSES` is provided for the case when a message that
requires a reply arrives from the Internet, but from a computer attached to a
LAN rather than via the defined gateway. Before replying to the message, the
TCP/IP stack RTOS task will loop up the message's IP address in the ARP table - but if
`ipconfigARP_STORES_REMOTE_ADDRESSES` is set to 0, then ARP
will return the MAC address of the defined gateway, because the destination address
is outside of the netmask. That might prevent the reply reaching its intended
destination.

If `ipconfigARP_STORES_REMOTE_ADDRESSES` is set to 1, then remote addresses
will also be stored in the ARP table, along with the MAC address from which the
message was received. This can allow the message in the scenario above to be
routed and delivered correctly.


#### ipconfigARP\_USE\_CLASH\_DETECTION

When a link-layer address is assigned, the driver will test if it is already taken by a different device by sending ARP
requests. Therefore, `ipconfigARP_USE_CLASH_DETECTION` must be defined as non-zero.


#### ipconfigMAX\_ARP\_AGE

`ipconfigMAX_ARP_AGE` defines the maximum time between an entry in the ARP
table being created or refreshed and the entry being removed because it is stale.
New ARP requests are sent for ARP cache entries that are nearing their maximum
age.

`ipconfigMAX_ARP_AGE` is specified in tens of seconds, so a value of 150 is equal
to 1500 seconds (or 25 minutes).


#### ipconfigMAX\_ARP\_RETRANSMISSIONS

ARP requests that do not result in an ARP response will be re-transmitted a
maximum of `ipconfigMAX_ARP_RETRANSMISSIONS` times before the ARP request is
aborted.


#### ipconfigUSE\_ARP\_REMOVE\_ENTRY

Advanced users only.

If `ipconfigUSE_ARP_REMOVE_ENTRY` is set to 1 then `ulARPRemoveCacheEntryByMac()`
is included in the build. `ulARPRemoveCacheEntryByMac()` uses a MAC address to
look up, and then remove, an entry from the ARP cache. If the MAC address is
found in the ARP cache, then the IP address associated with the MAC address is
returned. If the MAC address is not found in the ARP cache, then 0 is returned.

```c
uint32_t ulARPRemoveCacheEntryByMac( const MACAddress_t * pxMACAddress );

ulARPRemoveCacheEntryByMac() function prototype
```


#### ipconfigUSE\_ARP\_REVERSED\_LOOKUP

Advanced users only.

Normally ARP will look up an IP address from a MAC address. If `ipconfigUSE_ARP_REVERSED_LOOKUP`
is set to 1 then a function that does the reverse is also available.
`eARPGetCacheEntryByMac()` looks up a MAC address from an IP address.

```c
eARPLookupResult_t eARPGetCacheEntryByMac( MACAddress_t * const pxMACAddress,
                                           uint32_t *pulIPAddress );
```
*eARPGetCacheEntryByMac() function prototype*


### Constants Affecting DHCP and Name Service Behaviour

#### ipconfigDHCP\_FALL\_BACK\_AUTO\_IP

Only applicable when DHCP is in use. If no DHCP server responds, use "Auto-IP"; the device will allocate a random LinkLayer
IP address, and test if it is still available.


#### ipconfigDHCP\_REGISTER\_HOSTNAME

Often DHCP servers can show the names of devices that have leased IP addresses.
When `ipconfigDHCP_REGISTER_HOSTNAME` is set to 1, the device running FreeRTOS-Plus-TCP
can identify itself to a DHCP server with a human readable name by returning
the name from an application provided hook (or 'callback') function called
`pcApplicationHostnameHook()`.

When `ipconfigDHCP_REGISTER_HOSTNAME` is set to 1 the application must provide a
hook (callback) function with the following name and prototype:

```c
const char *pcApplicationHostnameHook( void );
```
*The name and prototype of the application provided hook function that returns the devices name*


#### ipconfigDNS\_CACHE\_ADDRESSES\_PER\_ENTRY

When looking up a URL, multiple answers (IP-addresses) may be received. This macro determines how many
answers will be stored per URL.


#### ipconfigDNS\_CACHE\_ENTRIES

If `ipconfigUSE_DNS_CACHE` is set to 1 then `ipconfigDNS_CACHE_ENTRIES` defines the
number of entries in the DNS cache.


#### ipconfigDNS\_CACHE\_NAME\_LENGTH

The maximum number of characters a DNS host name can take, including the NULL
terminator.


#### ipconfigDNS\_REQUEST\_ATTEMPTS

When looking up a host, the library has to send a DNS request and wait for a result. This process will be repeated at most
`ipconfigDNS_REQUEST_ATTEMPTS` times. The macro `ipconfigDNS_SEND_BLOCK_TIME_TICKS` determines how
long the function `FreeRTOS_sendto()` may block.

When sending, by default, the function will block for at most 500 milliseconds. When waiting for a reply,
`FreeRTOS_recvfrom()` will wait for at most 5000 milliseconds.


#### ipconfigDNS\_USE\_CALLBACKS

When defined, the function `FreeRTOS_gethostbyname_a()` becomes available. This function will start a DNS-lookup
and set an application 'hook'. This user function (or 'hook') will be called when either the URL has been found, or when a
time-out has been reached. Note that the function `FreeRTOS_gethostbyname_a()` will not make use of the macros
`ipconfigDNS_SEND_BLOCK_TIME_TICKS` and `ipconfigDNS_RECEIVE_BLOCK_TIME_TICKS`.


#### ipconfigMAXIMUM\_DISCOVER\_TX\_PERIOD

When `ipconfigUSE_DHCP` is set to 1, DHCP requests will be sent out at
increasing time intervals until either a reply is received from a DHCP server
and accepted, or the interval between transmissions reaches
`ipconfigMAXIMUM_DISCOVER_TX_PERIOD`. The TCP/IP stack will revert to using the
static IP address passed as a parameter to [FreeRTOS\_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit) 
if the re-transmission time interval reaches `ipconfigMAXIMUM_DISCOVER_TX_PERIOD` without
a DHCP reply being received.


#### ipconfigUSE\_DHCP

If `ipconfigUSE_DHCP` is 1 then FreeRTOS-Plus-TCP will attempt to retrieve an IP
address, netmask, DNS server address and gateway address from a DHCP server - and
revert to using the defined static address if an IP address cannot be obtained.

If `ipconfigUSE_DHCP` is 0 then FreeRTOS-Plus-TCP will not attempt to obtain its address
information from a DHCP server. Instead, it will immediately use the defined static address
information.


####  ipconfigUSE\_DHCPv6

If `ipconfigUSE_DHCPv6` is 1 then FreeRTOS-Plus-TCP will attempt to retrieve an IPv6 address, netmask, 
DNS server address and gateway address from a DHCPv6 server - and revert to using the defined static 
address if an IPv6 address cannot be obtained when an end-point is set to enable DHCPv6 flow.

If `ipconfigUSE_DHCPv6` is 0 then FreeRTOS-Plus-TCP will not attempt to obtain its IPv6 address information 
from a DHCPv6 server. Instead, it will immediately use the defined static address information. 


#### ipconfigUSE\_DHCP\_HOOK

A normal [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) transaction involves the following sequence:

1. The client sends a DHCP discovery packet to request an IP address from the DHCP server.
2. The DHCP server responds with an offer packet that contains the offered IP address.
3. The client sends a DHCP request packet in order to claim the offered IP address
4. The DHCP server sends an acknowledgement packet to grant the client use of the offered IP address,
   and to send additional configuration information to the client. Additional configuration information
   typically includes the IP address of the [gateway](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router), the IP address of the [DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/20-DNS)
   server, and the IP address lease length.

If `ipconfigUSE_DHCP_HOOK` is set to 1 then FreeRTOS-Plus-TCP will call an
application provided hook (or 'callback') function called `xApplicationDHCPUserHook()`
both before the initial discovery packet is sent, and after a DHCP offer has
been received - the hook function can be used to terminate the DHCP process at
either one of these two phases in the DHCP sequence. For example, the application
writer can effectively disable DHCP, even when [ipconfigUSE\_DHCP](#ipconfiguse_dhcp)
is set to 1, by terminating the DHCP process before the initial discovery packet
is sent. As another example, the application writer can check a static IP address
is compatible with the network to which the device is connected by receiving an
IP address offer from a DHCP server, but then terminating the DHCP process without
sending a request packet to claim the offered IP address.

If `ipconfigUSE_DHCP_HOOK` is set to 1, then the application writer must
provide a hook (callback) function with the following name and prototype:

```c
eDHCPCallbackAnswer_t xApplicationDHCPHook( eDHCPCallbackPhase_t eDHCPPhase,
                                            uint32_t ulIPAddress );
```
*The name and prototype of the DHCP application hook function*


Where `eDHCPCallbackQuestion_t` and `eDHCPCallbackAnswer_t` are defined as follows

```c
typedef enum eDHCP_QUESTIONS
{
    /* About to send discover packet. */
    eDHCPPhasePreDiscover,
    /* About to send a request packet. */
    eDHCPPhasePreRequest,
} eDHCPCallbackQuestion_t;

typedef enum eDHCP_ANSWERS
{
    /* Continue the DHCP process as normal. */
    eDHCPContinue,
    /* Stop the DHCP process, and use the static defaults. */
    eDHCPUseDefaults,
    /* Stop the DHCP process, and continue with current settings. */
    eDHCPStopNoChanges,
} eDHCPCallbackAnswer_t;
```
*The eDHCPCallbackQuestion\_t and eDHCPCallbackAnswer\_t definitions*

For example purposes only, below is a reference `xApplicationDHCPHook` implementation
that allows the DHCP sequence to proceed up to the point where an IP address is
offered, at which point the offered IP address is compared to the statically
configured IP address. If the offered and statically configured IP addresses are
on the same subnet, then the statically configured IP address is used. If the
offered and statically configured IP addresses are not on the same subnet, then
the IP address offered by the DHCP server is used.

```c
eDHCPCallbackAnswer_t xApplicationDHCPHook( eDHCPCallbackPhase_t eDHCPPhase,
                                            uint32_t ulIPAddress )
{
eDHCPCallbackAnswer_t eReturn;
uint32_t ulStaticIPAddress, ulStaticNetMask;

  /* This hook is called in a couple of places during the DHCP process, as
     identified by the eDHCPPhase parameter. */
  switch( eDHCPPhase )
  {
    case eDHCPPhasePreDiscover  :
      /* A DHCP discovery is about to be sent out. eDHCPContinue is
         returned to allow the discovery to go out.

         If eDHCPUseDefaults had been returned instead then the DHCP process
         would be stopped and the statically configured IP address would be
         used.

         If eDHCPStopNoChanges had been returned instead then the DHCP
         process would be stopped and whatever the current network
         configuration was would continue to be used. */
      eReturn = eDHCPContinue;
      break;

    case eDHCPPhasePreRequest  :
      /* An offer has been received from the DHCP server, and the offered
         IP address is passed in the ulIPAddress parameter. Convert the
         offered and statically allocated IP addresses to 32-bit values. */
      ulStaticIPAddress = FreeRTOS_inet_addr_quick( configIP_ADDR0,
                                                    configIP_ADDR1,
                                                    configIP_ADDR2,
                                                    configIP_ADDR3 );

      ulStaticNetMask = FreeRTOS_inet_addr_quick( configNET_MASK0,
                                                  configNET_MASK1,
                                                  configNET_MASK2,
                                                  configNET_MASK3 );

      /* Mask the IP addresses to leave just the sub-domain octets. */
      ulStaticIPAddress &= ulStaticNetMask;
      ulIPAddress &= ulStaticNetMask;

      /* Are the sub-domains the same? */
      if( ulStaticIPAddress == ulIPAddress )
      {
        /* The sub-domains match, so the default IP address can be
           used. The DHCP process is stopped at this point. */
        eReturn = eDHCPUseDefaults;
      }
      else
      {
        /* The sub-domains don't match, so continue with the DHCP
           process so the offered IP address is used. */
        eReturn = eDHCPContinue;
      }

      break;

    default :
      /* Cannot be reached, but set eReturn to prevent compiler warnings
         where compilers are disposed to generating one. */
      eReturn = eDHCPContinue;
      break;
  }

  return eReturn;
}
```
*A reference xApplicationDHCPHook() implementation*

When the `eDHCPPhase` parameter is set to `eDHCPPhasePreDiscover`, the ulIPAddress
parameter is set to the IP address already in use. When the `eDHCPPhase` parameter is set
to `eDHCPPhasePreRequest`, the `ulIPAddress` parameter is set to the IP address offered by
the DHCP server.


#### ipconfigUSE\_DNS

Set `ipconfigUSE_DNS` to 1 to include a basic DNS client/resolver. DNS is used
through the [FreeRTOS\_gethostbyname()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/19-gethostbyname) 
API function.


#### ipconfigUSE\_DNS\_CACHE

If `ipconfigUSE_DNS_CACHE` is set to 1, then the DNS cache will be enabled. If `ipconfigUSE_DNS_CACHE`
is set to 0, then the DNS cache will be disabled.

Note that if DNS cache is enabled (`ipconfigUSE_DNS_CACHE`), then the maximum length of hostnames that can be
resolved is capped by `ipconfigDNS_CACHE_NAME_LENGTH` since all DNS queries are cached. 


#### ipconfigUSE\_LLMNR

Set `ipconfigUSE_LLMNR` to 1 to include [LLMNR](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/22-LLMNR).


#### ipconfigUSE\_NBNS

Set `ipconfigUSE_NBNS` to 1 to include [NBNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/23-NetBIOS).


####  ipconfigUSE\_MDNS

Set ipconfigUSE\_MDNS to 1 to include [Multicast DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/21-mDNS). 


### Constants Affecting IP and ICMP Behaviour

####  ipconfigUSE\_IPv4

This macro is about IPv4. The FreeRTOS-Plus-TCP stack supports handling IPv4 packets (including handling 
IPv4 header, ARP, DHCP, and so on) when it’s set to 1. Otherwise, the stack will drop all IPv4 packets 
on the RX side and be unable to transmit any IPv4 packets.


#### ipconfigUSE\_IPv6

This macro is about IPv6. The FreeRTOS-Plus-TCP stack supports handling IPv6 packets (including handling 
IPv6 header, ND, RA, and so on) when it’s set to 1. Otherwise, the stack will drop all IPv6 packets on 
the RX side and be unable to transmit any IPv6 packets. 


#### ipconfigFORCE\_IP\_DONT\_FRAGMENT

This macro is about IP-fragmentation. When sending an IP-packet over the Internet, a big packet may be split up into
smaller parts which are then combined by the receiver. The sender can determine if this fragmentation is allowed or
not. `ipconfigFORCE_IP_DONT_FRAGMENT` is zero by default, which means that fragmentation is allowed.

Note that the FreeRTOS-Plus-TCP stack does not accept received fragmented packets.


#### ipconfigICMP\_TIME\_TO\_LIVE

When replying to an ICMP packet, the TTL field will be set to the value of this macro. The default value is 64
(as recommended by RFC 1700). The minimum value is 1, the maximum value is 255.


#### ipconfigIP\_PASS\_PACKETS\_WITH\_IP\_OPTIONS

If `ipconfigIP_PASS_PACKETS_WITH_IP_OPTIONS` is set to 1, then FreeRTOS-Plus-TCP accepts IP packets
that contain IP options, but does not process the options (IP options are not supported).

If `ipconfigIP_PASS_PACKETS_WITH_IP_OPTIONS` is set to 0, then FreeRTOS-Plus-TCP will drop IP
packets that contain IP options.


#### ipconfigREPLY\_TO\_INCOMING\_PINGS

If `ipconfigREPLY_TO_INCOMING_PINGS` is set to 1, then the TCP/IP stack will
generate replies to incoming ICMP echo (ping) requests.


#### ipconfigSUPPORT\_OUTGOING\_PINGS

If `ipconfigSUPPORT_OUTGOING_PINGS` is set to 1 then the `FreeRTOS_SendPingRequest()`
API function is available.


### Constants Affecting ND Behaviour

#### ipconfigND\_CACHE\_ENTRIES

The ND cache is a table that maps IP addresses to MAC addresses.

The IP stack can only send a TCP/UDP message to a remote IPv6 address if it knows the MAC address associated 
with the IPv6 address, or the MAC address of the router used to contact the remote IPv6 address. When a 
message is received from a remote IPv6 address, the MAC address and IPv6 address are added to the ND cache. 
When a TCP/UDP message is sent to a remote IPv6 address that does not already appear in the ND cache, 
then the TCP/UDP message is replaced by a Neighbor Solicitation message that solicits the required MAC 
address information.

ipconfigND\_CACHE\_ENTRIES defines the maximum number of entries that can exist in the ND table at any one time.


### Constants Affecting RA Behaviour

#### ipconfigUSE\_RA

If ipconfigUSE\_RA is 1 then FreeRTOS-Plus-TCP will attempt to retrieve an IPv6 address, prefix address, 
and gateway address from a IPv6 router by SLAAC flow - and revert to using the defined static address if 
an IPv6 address cannot be obtained when an end-point is set to enable RA flow.

If ipconfigUSE\_RA is 0 then FreeRTOS-Plus-TCP will not attempt to obtain its address information from a 
DHCP server. Instead, it will immediately use the defined static address information.


#### ipconfigRA\_SEARCH\_COUNT and ipconfigRA\_IP\_TEST\_COUNT

RA or Router Advertisement/SLAAC: see end-point flag 'bWantRA'. A Router Solicitation will be sent. It 
will wait for ipconfigRA\_SEARCH\_TIME\_OUT\_MSEC ms. When there is no response, it will be repeated 
ipconfigRA\_SEARCH\_COUNT times. Then it will check if the chosen IP-address already exists, and repeat 
this ipconfigRA\_IP\_TEST\_COUNT times, each time with a timeout of ipconfigRA\_IP\_TEST\_TIME\_OUT\_MSEC 
ms. Finally, the end-point will enter the UP state. 


### Constants Providing Target Support

#### ipconfigHAS\_INLINE\_FUNCTIONS

If the compiler in use supports inline functions, and `portINLINE` is defined to
the correct inline keyword for the compiler, then set `ipconfigHAS_INLINE_FUNCTIONS`
to 1. Otherwise set `ipconfigHAS_INLINE_FUNCTIONS` to 0, which will result in
some inline functions using an alternative macro implementation.


#### ipconfigRAND32

`ipconfigRAND32()` is called by the TCP/IP stack to generate a random number that
is then used as a DHCP transaction number. Random number generation is performed
via this macro to allow applications to use their own random number generation
method. For example, it might be possible to generate a random number by
sampling noise on an analogue input.

**Note:**
The random number generator must be seeded before the TCP/IP stack is started,
that is, before [FreeRTOS\_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit) is called.


#### ipconfigIS\_VALID\_PROG\_ADDRESS

In cases where installable application hooks are used, this macro is called to check if a given address refers to
valid (instruction) memory. This is a small example taken from FreeRTOS\_TCP\_IP.c:

```c
   if( ipconfigIS_VALID_PROG_ADDRESS( pxSocket->u.xTCP.pxHandleSent ) )
    {
        pxSocket->u.xTCP.pxHandleSent( pxSocket, ulCount );
    }
```


#### ipconfigPORT\_SUPPRESS\_WARNING

For some use cases, users set the configurations that issue warning messages. This configuration is used 
to suppress warnings in portable layers to make compilation clean.


### Backward Compatibility

#### ipconfigCOMPATIBLE\_WITH\_SINGLE

If ipconfigCOMPATIBLE\_WITH\_SINGLE is set to 1, then FreeRTOS-Plus-TCP assumes there are no multiple 
end-points/interfaces in the program. Some routing functions can be simplified to return the first 
end-point/interface directly.

If ipconfigCOMPATIBLE\_WITH\_SINGLE is set to 0, which is the default value, then FreeRTOS-Plus-TCP 
assumes multiple end-points/interfaces are allowed in the program.


#### ipconfigIPv4\_BACKWARD\_COMPATIBLE

If ipconfigIPv4\_BACKWARD\_COMPATIBLE is set to 1, then FreeRTOS-Plus-TCP supports the original feature 
before V4.0.0, and the stack is not able to support IPv6. All functions prototypes are reset to original ones.

If ipconfigIPv4\_BACKWARD\_COMPATIBLE is set to 0, which is the default value, then FreeRTOS-Plus-TCP applies 
all new features introduced by V4.0.0. 

