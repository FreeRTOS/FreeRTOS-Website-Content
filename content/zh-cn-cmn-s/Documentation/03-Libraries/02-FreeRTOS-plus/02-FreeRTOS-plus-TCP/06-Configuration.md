---
title: FreeRTOS-Plus-TCP 配置
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOSIPConfig.h 头文件
  
FreeRTOS-Plus-TCP 应用程序必须提供一个 FreeRTOSIPConfig.h 头文件， 
用于定义此页面上描述的参数。

[配置示例](TCP_IP_Configuration_Examples.md)页面演示如何设置关键配置参数，适用于 
需要最大限度减少 RAM 消耗和需要最大限度增加吞吐量的系统。


* 影响 TCP/IP 堆栈任务执行行为的常量
  + [ipconfigEVENT_QUEUE_LENGTH](#ipconfigevent_queue_length)
  + [ipconfigIP_TASK_PRIORITY](#ipconfigip_task_priority)
  + [ipconfigIP_TASK_STACK_SIZE_WORDS](#ipconfigip_task_stack_size_words)
  + [ipconfigPROCESS_CUSTOM_ETHERNET_FRAMES](#ipconfig_process_custom_ethernet_frames)
  + [ipconfigUSE_NETWORK_EVENT_HOOK](#ipconfiguse_network_event_hook)

* 调试、跟踪和日志记录设置  
  另请参阅 [TCP/IP 跟踪宏](TCP_IP_Trace.md)。
  + [ipconfigCHECK_IP_QUEUE_SPACE](#ipconfigcheck_ip_queue_space)
  + [ipconfigHAS_DEBUG_PRINTF](#ipconfighas_debug_printf-和-freertos_debug_printf) 和 FreeRTOS_debug_printf
  + [ipconfigHAS_PRINTF](#ipconfighas_printf-和-freertos_printf) 和 FreeRTOS_printf
  + [ipconfigINCLUDE_EXAMPLE_FREERTOS_PLUS_TRACE_CALLS()](#ipconfiginclude_example_freertos_plus_trace_calls)
  + [ipconfigTCP_IP_SANITY()](#ipconfigtcp_ip_sanity)
  + [ipconfigTCP_MAY_LOG_PORT](#ipconfigtcp_may_log_port-x-)
  + [ipconfigWATCHDOG_TIMER()](#ipconfigwatchdog_timer)

* 硬件和驱动器特定设置
  + [ipconfigBUFFER_PADDING 和 ipconfigPACKET_FILLER_SIZE](#ipconfigbuffer_padding-和-ipconfigpacket_filler_size)
  + [ipconfigBYTE_ORDER](#ipconfigbyte_order)
  + [ipconfigDRIVER_INCLUDED_RX_IP_CHECKSUM](#ipconfigdriver_included_rx_ip_checksum)
  + [ipconfigDRIVER_INCLUDED_TX_IP_CHECKSUM](#ipconfigdriver_included_tx_ip_checksum)
  + [ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES](#ipconfigethernet_driver_filters_frame_types)
  + [ipconfigETHERNET_DRIVER_FILTERS_PACKETS](#ipconfigethernet_driver_filters_packets)
  + [ipconfigETHERNET_MINIMUM_PACKET_BYTES](#ipconfigethernet_minimum_packet_bytes)
  + [ipconfigFILTER_OUT_NON_ETHERNET_II_FRAMES](#ipconfigfilter_out_non_ethernet_ii_frames)
  + [ipconfigNETWORK_MTU](#ipconfignetwork_mtu)
  + [ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS](#ipconfignum_network_buffer_descriptors)
  + [ipconfigUSE_LINKED_RX_MESSAGES](#ipconfiguse_linked_rx_messages)
  + [ipconfigZERO_COPY_RX_DRIVER](#ipconfigzero_copy_rx_driver)
  + [ipconfigZERO_COPY_TX_DRIVER](#ipconfigzero_copy_tx_driver)

* TCP 相关常量
  + [ipconfigIGNORE_UNKNOWN_PACKETS](#ipconfigignore_unknown_packets)
  + [ipconfigTCP_HANG_PROTECTION](#ipconfigtcp_hang_protection)
  + [ipconfigTCP_HANG_PROTECTION_TIME](#ipconfigtcp_hang_protection_time)
  + [ipconfigTCP_KEEP_ALIVE](#ipconfigtcp_keep_alive)
  + [ipconfigTCP_KEEP_ALIVE_INTERVAL](#ipconfigtcp_keep_alive_interval)
  + [ipconfigTCP_MSS](#ipconfigtcp_mss)
  + [ipconfigTCP_RX_BUFFER_LENGTH 和 ipconfigTCP_TX_BUFFER_LENGTH](#ipconfigtcp_rx_buffer_length-and-ipconfigtcp_tx_buffer_length)
  + [ipconfigTCP_TIME_TO_LIVE](#ipconfigtcp_time_to_live)
  + [ipconfigTCP_WIN_SEG_COUNT](#ipconfigtcp_win_seg_count)
  + [ipconfigUSE_TCP](#ipconfiguse_tcp)
  + [ipconfigUSE_TCP_TIMESTAMPS](#ipconfiguse_tcp_timestamps)
  + [ipconfigUSE_TCP_WIN](#ipconfiguse_tcp_win)

* UDP 相关常量
  + [ipconfigUDP_MAX_RX_PACKETS](#ipconfigudp_max_rx_packets)
  + [ipconfigUDP_MAX_SEND_BLOCK_TIME_TICKS](#ipconfigudp_max_send_block_time_ticks)
  + [ipconfigUDP_PASS_ZERO_CHECKSUM_PACKETS](#ipconfigudp_pass_zero_checksum_packets)
  + [ipconfigUDP_TIME_TO_LIVE](#ipconfigudp_time_to_live)

* 影响套接字行为的其他常量
  + [ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND](#ipconfigallow_socket_send_without_bind)
  + [ipconfigINCLUDE_FULL_INET_ADDR](#ipconfiginclude_full_inet_addr)
  + [ipconfigSELECT_USES_NOTIFY](#ipconfigselect_uses_notify)
  + [ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME](#ipconfigsock_default_receive_block_time)
  + [ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME](#ipconfigsock_default_send_block_time)
  + [ipconfigSOCKET_HAS_USER_SEMAPHORE](#ipconfigsocket_has_user_semaphore)
  + [ipconfigSOCKET_HAS_USER_WAKE_CALLBACK](#ipconfigsocket_has_user_wake_callback)
  + [ipconfigSUPPORT_SELECT_FUNCTION](#ipconfigsupport_select_function)
  + [ipconfigSUPPORT_SIGNALS](#ipconfigsupport_signals)
  + [ipconfigUSE_CALLBACKS](#ipconfiguse_callbacks)

* 影响 ARP 行为的常量
  + [ipconfigARP_CACHE_ENTRIES](#ipconfigarp_cache_entries)
  + [ipconfigARP_STORES_REMOTE_ADDRESSES](#ipconfigarp_stores_remote_addresses)
  + [ipconfigARP_USE_CLASH_DETECTION](#ipconfigarp_use_clash_detection)
  + [ipconfigMAX_ARP_AGE](#ipconfigmax_arp_age)
  + [ipconfigMAX_ARP_RETRANSMISSIONS](#ipconfigmax_arp_retransmissions)
  + [ipconfigUSE_ARP_REMOVE_ENTRY](#ipconfiguse_arp_remove_entry)
  + [ipconfigUSE_ARP_REVERSED_LOOKUP](#ipconfiguse_arp_reversed_lookup)

* 影响 DHCP 和名称服务行为的常量
  + [ipconfigDHCP_FALL_BACK_AUTO_IP](#ipconfigdhcp_fall_back_auto_ip)
  + [ipconfigDHCP_REGISTER_HOSTNAME](#ipconfigdhcp_register_hostname)
  + [ipconfigDNS_CACHE_ADDRESSES_PER_ENTRY](#ipconfigdns_cache_address_per_entry)
  + [ipconfigDNS_CACHE_ENTRIES](#ipconfigdns_cache_entries)
  + [ipconfigDNS_CACHE_NAME_LENGTH](#ipconfigdns_cache_name_length)
  + [ipconfigDNS_REQUEST_ATTEMPTS](#ipconfigdns_request_attempts)
  + [ipconfigDNS_USE_CALLBACKS](#ipconfigdns_use_callbacks)
  + [ipconfigMAXIMUM_DISCOVER_TX_PERIOD](#ipconfigmaximum_discover_tx_period)
  + [ipconfigUSE_DHCP](#ipconfiguse_dhcp)
  + [ipconfigUSE_DHCP_HOOK](#ipconfiguse_dhcp)
  + [ipconfigUSE_DNS](#ipconfiguse_dns)
  + [ipconfigUSE_DNS_CACHE](#ipconfiguse_dns_cache)
  + [ipconfigUSE_LLMNR](#ipconfiguse_llmnr)
  + [ipconfigUSE_NBNS](#ipconfiguse_nbns)

* 影响 IP 和 ICMP 行为的常量
  + [ipconfigFORCE_IP_DONT_FRAGMENT](#ipconfigforce_ip_dont_fragment)
  + [ipconfigICMP_TIME_TO_LIVE](#ipconfigicmp_time_to_live)
  + [ipconfigIP_PASS_PACKETS_WITH_IP_OPTIONS](#ipconfigip_pass_packets_with_ip_options)
  + [ipconfigREPLY_TO_INCOMING_PINGS](#ipconfigreply_to_incoming_pings)
  + [ipconfigSUPPORT_OUTGOING_PINGS](#ipconfigsupport_outgoing_pings)

* 提供目标支持的常量
  + [ipconfigHAS_INLINE_FUNCTIONS](#ipconfighas_inline_functions)
  + [ipconfigRAND32](#ipconfigrand32)
  + [ipconfigIS_VALID_PROG_ADDRESS](#ipconfigis_valid_prog_address-x-)



### 影响 TCP/IP 堆栈任务执行行为的常量

#### ipconfigEVENT_QUEUE_LENGTH

使用 FreeRTOS 队列将事件从应用程序任务发送到 IP 堆栈。 `ipconfigEVENT_QUEUE_LENGTH` 
设置可同时排队等待处理的最大事件数。事件队列最小必须 
比网络缓冲区的总数大 5。


#### ipconfigIP_TASK_PRIORITY

TCP/IP 堆栈执行自己的 RTOS 任务（但**任何**应用程序 RTOS 任务都可以 
通过公布的套接字 API 使用其服务）。`ipconfigIP_TASK_PRIORITY` 设置 RTOS 任务的优先级， 
此任务执行 TCP/IP 堆栈。

优先级是[标准的 FreeRTOS 任务优先级](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities)，因此可以取任何值， 
从 0（最低优先级）到 (`configMAX_PRIORITIES - 1`)（最高优先级）均可。`configMAX_PRIORITIES` 是
在 FreeRTOSConfig.h（而非 FreeRTOSIPConfig.h）中定义的标准 FreeRTOS 配置参数。

需要考虑 RTOS 任务
（执行 TCP/IP 堆栈）所分配的优先级与使用 TCP/IP 堆栈的任务所分配的优先级之间的相对关系。


#### ipconfigIP_TASK_STACK_SIZE_WORDS

分配给 FreeRTOS-Plus-TCP RTOS 任务的堆栈大小（按字数而非字节数）。 FreeRTOS 
包括 [可选堆栈溢出检测](../../Stacks-and-stack-overflow-checking.md)。

  
#### ipconfig_PROCESS_CUSTOM_ETHERNET_FRAMES

如果 ipconfigPROCESS_CUSTOM_ETHERNET_FRAMES 设为 1 ，则 TCP/IP 堆栈将 
调用 [eApplicationProcessCustomFrameHook](API/eApplicationProcessCustomFrameHook.md) 处理任何 
未知帧，即任何需要 ARP 或 IP 的帧。

  
#### ipconfigUSE_NETWORK_EVENT_HOOK

如果 `ipconfigUSE_NETWORK_EVENT_HOOK` 设为 1，则 FreeRTOS-Plus-TCP 将在适当时候调用 
[网络事件钩子](API/vApplicationIPNetworkEventHook.md)。 
如果 `ipconfigUSE_NETWORK_EVENT_HOOK` 未设为 1 ，则永远不会调用网络事件钩子。
  

### 调试、跟踪和日志记录设置

#### 跟踪宏

有关可用 TCP/IP 堆栈跟踪宏的信息，请参阅[另外的页面](TCP_IP_Trace.md)。

  
#### ipconfigCHECK_IP_QUEUE_SPACE

使用 FreeRTOS 队列将事件从应用程序任务发送到 IP 堆栈 
。  [ipconfigEVENT_QUEUE_LENGTH](#ipconfigevent_queue_length) 设置可以 
同时排队等待处理的最大事件数。如果 `ipconfigCHECK_IP_QUEUE_SPACE` 设为 1， 
则 `uxGetMinimumIPQueueSpace()` 函数可用于查询系统启动以来队列中存在的 
可用空间最小值。

```c
UBaseType_t uxGetMinimumIPQueueSpace( void );  

```
*uxGetMinimumIPQueueSpace() function prototype*


#### ipconfigHAS_DEBUG_PRINTF 和 FreeRTOS_debug_printf

TCP/IP 堆栈通过调用 FreeRTOS_debug_printf 宏输出调试消息。为获取 
调试消息，将 `ipconfigHAS_DEBUG_PRINTF` 设为 1，然后将 `FreeRTOS_debug_printf()` 定义为 
以下函数：获取 `printf()` 样式的格式字符串和可变数量的输入，然后发送格式化 
消息至您选择的一个输出的函数。

如果 `ipconfigHAS_DEBUG_PRINTF` 设为 0，则请勿定义 `FreeRTOS_debug_printf`。

下列代码取自用于 RTOS Win32 模拟器[(examples_FreeRTOS_simulator.md)的 ]FreeRTOS-Plus-TCP 示例，
它能够将调试消息输出到 UDP 移植、标准输出和磁盘文件：


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

在 FreeRTOSIPConfig.h  
 中定义 ipconfigHAS_DEBUG_PRINTF 和 FreeRTOS_debug_printf
执行输出的函数（上面的代码中的 `vLoggingPrintf()`）必须是可重入函数。


#### ipconfigHAS_PRINTF 和 FreeRTOS_printf

一些 TCP/IP 堆栈演示应用程序生成输出消息。TCP/IP 堆栈调用 
FreeRTOS_printf 宏来输出这些消息。若要获取演示应用程序消息，请将 `ipconfigHAS_PRINTF` 设 
为 1，然后将 `FreeRTOS_printf()` 定义为以下函数：获取 `printf()` 样式的格式字符串和 
可变数量的输入，然后发送格式化消息至您选择的一个输出的函数。

如果 `ipconfigHAS_PRINTF` 设为 0，则请勿定义 `FreeRTOS_printf`。

以下代码取自 
用于 RTOS Win32 模拟器[(examples_FreeRTOS_simulator.md)的 ]FreeRTOS-Plus-TCP 示例， 
它能够将应用程序消息输出到 UDP 移植、标准输出和磁盘文件：


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

在 FreeRTOSIPConfig.h  
 中定义 ipconfigHAS_PRINTF 和 FreeRTOS_printf
执行输出的函数（上面的代码中的 `vLoggingPrintf()`）必须是可重入函数。


#### ipconfigINCLUDE_EXAMPLE_FREERTOS_PLUS_TRACE_CALLS

宏 `configINCLUDE_TRACE_RELATED_CLI_COMMANDS` 可以在 FreeRTOSConfig.h 中定义。定义后， 
此宏将分配给 `ipconfigINCLUDE_EXAMPLE_FREERTOS_PLUS_TRACE_CALLS`。它允许纳入 
CLI 用于跟踪。


#### ipconfigTCP_IP_SANITY

此宏的名称稍有误导性：它只检查模块 BufferAllocation_1.c 的行为。 
当发现异常行为时，它会发出警告。


#### ipconfigTCP_MAY_LOG_PORT( x )

`ipconfigTCP_MAY_LOG_PORT( x )` 可以定义为指定哪个移植号应该或不应该 
被 `FreeRTOS_lprintf()` 记录。例如，下列定义将不会为移植 23 或 2402 生成日志消息：

```c
#define ipconfigTCP_MAY_LOG_PORT(xPort) ( ( ( xPort ) != 23 ) && ( ( xPort ) != 2402 ) )  

```
*筛选日志消息*


#### ipconfigWATCHDOG_TIMER()

`ipconfigWATCHDOG_TIMER()` 是在每次遍历 IP 任务时
调用的宏，如果应用程序包含看门狗类型功能，需要知道 IP 任务
仍在循环时（虽然 IP 任务正在循环这一事实
并不一定表明它正在正常运行），该宏可以起到作用。

`ipconfigWATCHDOG_TIMER()` 可以被定义为执行应用程序编写者期望的
任何操作。如果未定义 `ipconfigWATCHDOG_TIMER()`，则它将由预处理器
彻底移除（它将被默认为空宏）。



### 硬件和驱动器相关设置

#### ipconfigBUFFER_PADDING 和 ipconfigPACKET_FILLER_SIZE

仅用于高级驱动器实现。

当应用程序请求网络缓冲区时，虽然应用程序编写者指定了 
网络缓冲区的大小，但实际获取的大小会增加 `ipconfigBUFFER_PADDING` 个字节。 
接着利用缓冲区的首个 `ipconfigBUFFER_PADDING` 字节保存缓冲区的元数据， 
而实际存储元数据的区域跟随在元数据之后。此机制对用户是透明的，因为 
用户只看到指向缓冲区内实际用于保存网络数据的区域的指针。

一些网络硬件具有非常特定的字节对齐要求，因此提供 `ipconfigBUFFER_PADDING`  
作为可配置参数，以便网络驱动器的编写者能够影响元数据后面数据开头的对齐 
。


#### ipconfigBYTE_ORDER

如果运行 FreeRTOS-Plus-TCP 的微控制器是大 Endian，则 `ipconfigBYTE_ORDER` 必须 
设为 `pdFREERTOS_BIG_ENDIAN`。如果微控制器为小 Endian，则 `ipconfigBYTE_ORDER` 必须 
设为 `pdFREERTOS_LITTLE_ENDIAN`。“嵌入式网络基础知识和术语表”页面的[字节顺序和 Endian](endian.md) 章节 
解释了 IP 网络中的字节顺序注意事项。


#### ipconfigDRIVER_INCLUDED_RX_IP_CHECKSUM

如果网络驱动器或网络硬件正在计算传入数据包的 IP、TCP 和 UDP 校验和， 
并丢弃发现包含无效校验和的数据包，则将 `ipconfigDRIVER_INCLUDED_RX_IP_CHECKSUM`  
设为 1，否则将 `ipconfigDRIVER_INCLUDED_RX_IP_CHECKSUM` 设为 0。

通过实现利用硬件校验和计算的驱动器，吞吐量和处理器负载得到大大提升 
。

**注意：**自 FreeRTOS-Plus-TCP V2.3.0 起，即使在硬件中已检查过长度，还要在软件中检查长度 
。


#### ipconfigDRIVER_INCLUDED_TX_IP_CHECKSUM

如果网络驱动器或网络硬件正在计算传出数据包的 IP、TCP 和 UDP 校验和， 
则将 `ipconfigDRIVER_INCLUDED_TX_IP_CHECKSUM` 设为 1，否则将 `ipconfigDRIVER_INCLUDED_TX_IP_CHECKSUM` 设为 0 
。

通过实现利用硬件校验和计算的驱动器，吞吐量和处理器负载得到大大提升 
。


#### ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES

[以太网/硬件 MAC 地址](ethernet_networking_and_addressing.md)用于以太网帧寻址。 
如果网络驱动器或硬件正在丢弃不包含相关 MAC 地址的数据包， 
则将 `ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES` 设为 1，否则将 `ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES` 设为 0 
。

通过在硬件中实现网络地址筛选，吞吐量和处理器负载得以大大提升。 
大多数网络接口允许定义多个 MAC 地址，因此可以通过 
节点的唯一硬件地址、广播地址和各种多播地址进行筛选。


#### ipconfigETHERNET_DRIVER_FILTERS_PACKETS

仅适用于专家用户。

`ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES` 用于指定网络驱动器或硬件是否 
筛选以太网帧，而 `ipconfigETHERNET_DRIVER_FILTERS_PACKETS` 用于指定网络驱动器 
是否筛选以太网帧内的 IP、UDP 或 TCP 数据。

TCP/IP 堆栈仅有兴趣接收发送至本地节点上的套接字 
（IP 地址和移植号）的数据或者广播或多播的数据包。通过阻止不符合这些标准的数据包 
被发送到 TCP/IP 堆栈，吞吐量和处理负载得以大大提升。 FreeRTOS 
 提供了一些功能，允许在网络驱动器中进行此类筛选。例如， 
`xPortHasUDPSocket()` 可以按照下列方式使用：

```c
if( ( xPortHasUdpSocket( xUDPHeader->usDestinationPort ) )  
    #if( ipconfigUSE_DNS == 1 )/* [DNS](DNS.md) is also UDP. */  
        || ( xUDPHeader->usSourcePort == FreeRTOS_ntohs( ipDNS_PORT ) )  
    #endif  
    #if( ipconfigUSE_LLMNR == 1 ) /* [LLMNR](LLMNR.md) is also UDP. */  
        || ( xUDPHeader->usDestinationPort == FreeRTOS_ntohs( ipLLMNR_PORT ) )  
    #endif  
    #if( ipconfigUSE_NBNS == 1 ) /* [NBNS](NetBIOS.md) is also UDP. */  
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
*筛选 UDP 数据包的示例*


#### ipconfigETHERNET_MINIMUM_PACKET_BYTES

当设备连接到局域网时，强烈建议给每个传出数据包 60 字节的最小长度 
（加上 4 字节 CRC）。宏 `ipconfigETHERNET_MINIMUM_PACKET_BYTES` 决定了 
最小长度。默认情况下，它被定义为 0，这意味着数据包将按原样发送。


#### ipconfigFILTER_OUT_NON_ETHERNET_II_FRAMES

如果 `ipconfigFILTER_OUT_NON_ETHERNET_II_FRAMES` 设为 1，则将丢弃非以太网 II 格式的以太网帧 
。此选项包含在未来潜在的 IP 堆栈开发中。

  
#### ipconfigNETWORK_MTU

[MTU](MTU.md) 是网络帧的有效负载可以包含的最大字节数。对于正常 
以太网 V2 帧，最大 MTU 为 1500（但互联网路由可能需要更低的字节数）。 
设置较低值可以节省 RAM，这取决于所使用的缓冲区管理方案。 

如果未定义 `ipconfigNETWORK_MTU`，则将应用以下默认值：

```c
#ifndef ipconfigNETWORK_MTU  
    #ifdef( ipconfigUSE_TCP_WIN == 1 )  
        #define ipconfigNETWORK_MTU      ( 1526 )  
    #else  
        #define ipconfigNETWORK_MTU      ( 1514 )  
    #endif  
#endif  

```


#### ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS

`ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS` 定义了
 TCP/IP 堆栈可用的网络缓冲区总数。网络缓冲区的总数是有限的，
以确保可由 TCP/IP 栈消耗的 RAM 总量限制在
预定值以内。实际给网络缓冲区结构体分配存储区域的方式
不是固定的，而是可移植层的一部分。最简单的
方案仅准确分配所需的精确存储量。

有关网络缓冲区和网络缓冲区描述符的更多信息，请参阅 
介绍如何[将 FreeRTOS-Plus-TCP 移植到其他硬件](Embedded_Ethernet_Porting.md)和 
[pxGetNetworkBufferWithDescriptor()](API/pxGetNetworkBufferWithDescriptor.md) 移植特定 
API 函数的页面。


#### ipconfigUSE_LINKED_RX_MESSAGES

仅限高级用户。

当 `pconfigUSE_LINKED_RX_MESSAGES` 设置为 1 时，将多个接收到的数据包链接在一起， 
然后将链接的数据包一次性传递至 
IP RTOS 任务，从而在网络流量高峰期降低 CPU 负载。


#### ipconfigZERO_COPY_RX_DRIVER

仅限高级用户。

如果 `ipconfigZERO_COPY_RX_DRIVER` 设为 1 ，则网络接口会将网络 
缓冲区 `NetworkBufferDescriptor_t::pucEthernetBuffer` 分配给 EMAC 的 DMA。在收到数据包时不复制 
任何数据。相反，缓冲区直接发送到 IP 任务。  如果 TX 零拷贝选项被禁用， 
则每个接收的数据包都将从 DMA 缓冲区复制到 `NetworkBufferDescriptor_t` 类型的网络缓冲区。


#### ipconfigZERO_COPY_TX_DRIVER

仅限高级用户。

如果 `ipconfigZERO_COPY_TX_DRIVER` 设为 1，则驱动器 
函数 [xNetworkInterfaceOutput()](Embedded_Ethernet_Porting.md#xNetworkInterfaceOutput) 调用时， 
其 `bReleaseAfterSend` 参数将始终设为 `pdTRUE`，这意味着此驱动器 
将始终负责释放网络缓冲区和网络缓冲区描述符。

如果驱动器实现零拷贝方案，数据包直接从 
网络缓冲区内部发送（例如通过指向网络缓冲区内部数据的 DMA 描述符）, 
而非在发送数据前将数据复制出网络缓冲区（例如通过将数据复制到 
单独的预分配 DMA 描述符），则这将很有用。在这种情况下，驱动器需要获取 
网络缓冲区的所有权，因为网络缓冲区只能在数据实际传输后才能释放， 
此时距离 `xNetworkInterfaceOutput()` 函数返回已经过了一段时间。请参阅 
[将 FreeRTOS 移植到不同微控制器](Embedded_Ethernet_Porting.md)文档页面，获取
工作示例。


### TCP 相关常量

#### ipconfigIGNORE_UNKNOWN_PACKETS

通常，具有错误或未知目标的 TCP 数据包将导致 RESET
被发送回远程主机。如果 `ipconfigIGNORE_UNKNOWN_PACKETS` 设为 1，
则此类重置将被抑制（不发送）。

  
#### ipconfigTCP_HANG_PROTECTION

如果 `ipconfigTCP_HANG_PROTECTION` 设为 1，则 FreeRTOS-Plus-TCP 会将一个套接字
标记为关闭（如果套接字在
 `ipconfigTCP_HANG_PROTECTION_TIME` 指定的周期内没有发生状态变化）。

  
#### ipconfigTCP_HANG_PROTECTION_TIME

如果 `ipconfigTCP_HANG_PROTECTION` 设为 1，则 `ipconfigTCP_HANG_PROTECTION_TIME` 会设置
上次更改套接字状态与防挂机制将套接字标记为关闭之间
的间隔（以秒为单位）。

  
#### ipconfigTCP_KEEP_ALIVE

已连接但长时间不传输任何数据的套接字
可以由超时的路由器或防火墙断开连接。通过确保应用程序定期发送数据包
可以避免在应用程序级出现该情况。
或者，可以将 FreeRTOS-Plus-TCP 配置为当它检测到连接处于休眠状态时，
自动发送保活消息。请注意，尽管
有 FreeRTOS-Plus-TCP 自动发送保活消息是更方便的方法，
但这也是最不可靠的方法，因为一些路由器会丢弃保活
消息。

将 `ipconfigTCP_KEEP_ALIVE` 设为 1，以使 FreeRTOS-Plus-TCP 在已连接
但处于休眠状态的套接字上定期发送保活消息。将 `ipconfigTCP_KEEP_ALIVE` 设为
0，以防止保活消息的自动传输。

如果 FreeRTOS-Plus-TCP 未收到对保活消息的回复，则
将断开连接并将套接字标记为已关闭。随后
在套接字上调用 `FreeRTOS_recv()` 将返回 `-pdFREERTOS_ERRNO_ENOTCONN`。



#### ipconfigTCP_KEEP_ALIVE_INTERVAL

如果 `ipconfigTCP_KEEP_ALIVE` 设为 1，则 `ipconfigTCP_KEEP_ALIVE_INTERVAL` 会设置
连续保活消息之间的间隔（以秒为单位）。除非自上次发送或接收数据包以来已过去 
`ipconfigTCP_KEEP_ALIVE_INTERVAL` 秒，否则不会发送保活消息
。

  
#### ipconfigTCP_MSS

为所有 TCP 数据包设置 [MSS](MSS.md) 值（以字节为单位）。

请注意，FreeRTOS-Plus-TCP 包含若干检查，以确定定义的 `ipconfigNETWORK_MTU` 和 `ipconfigTCP_MSS`  
数值相互之间保持一致。


#### ipconfigTCP_RX_BUFFER_LENGTH and ipconfigTCP_TX_BUFFER_LENGTH

每个 TCP 套接字具有用于接收的缓冲区和用于传输的单独缓冲区。

默认缓冲区大小为 (4*ipconfigTCP_MSS)。

`FreeRTOS_setsockopt()` 可用于 `FREERTOS_SO_RCVBUF` 和 `FREERTOS_SO_SNDBUF` 参数，
以分别接收和发送缓冲区大小，但这必须
在创建套接字的时间和创建套接字所使用缓冲区的时间。
之间完成。在实际接收数据之前不会创建接收缓冲区，
在数据实际发送到套接字进行传输之前不会创建传输缓冲区。
创建缓冲区后，无法更改其大小。

如果[监听套接字](TCP_Networking_Tutorial_TCP_Client_and_Server.md)
为响应传入的连接请求创建一个新的套接字，
则新套接字将继承监听套接字的缓冲区大小。


#### ipconfigTCP_TIME_TO_LIVE

定义传出 TCP 数据包中使用的[生存时间](http://en.wikipedia.org/wiki/Time_to_live) TTL) 值。

  
#### ipconfigTCP_WIN_SEG_COUNT

如果 `ipconfigUSE_TCP_WIN` 设为 1，则每个套接字将使用一个滑动窗口。
滑动窗口允许消息乱序到达，且 FreeRTOS-Plus-TCP 使用
窗口描述符以跟踪窗口中关于所述数据包的信息。

在建立第一个 TCP 连接时分配一个描述符池。描述符
在所有套接字之间共享。`ipconfigTCP_WIN_SEG_COUNT` 设置
池中描述符的数量，每个描述符约为
64 字节。

例如，如果系统将同时拥有最多 16 个 TCP 连接，
且每个连接将有最多 8 个段的 Rx 和 Tx 窗口，
则最坏的情况下，需要的最大描述符数为 256 (16 * 2 * 8)。
然而，实际上最坏的情况通常比上述情况要低得多，因为大多数
数据包将按顺序到达。


#### ipconfigUSE_TCP

将 `ipconfigUSE_TCP` 设为 1，以启用 [TCP](TCP.md)。如果 `ipconfigUSE_TCP` 设为 0，则仅 [UDP](UDP.md) 
可用。
 
  
#### ipconfigUSE_TCP_TIMESTAMPS

TCP 时间戳功能可用，但其用途非常有限。
时间戳只能在初始 SYN 数据包包含时间戳选项的情况下使用
。在大多数情况下，传入连接不会设置时间戳选项。

将 `ipconfigUSE_TCP_TIMESTAMPS` 设为 1，以包括 TCP 时间戳功能。
将 `ipconfigUSE_TCP_TIMESTAMPS`  设为 0 以排除 TCP 时间戳功能。


#### ipconfigUSE_TCP_WIN

滑动窗口使消息可以乱序到达。

将 `ipconfigUSE_TCP_WIN` 设为 1，以将[滑动窗口](TCP_Networking_Tutorial_TCP_Client_and_Server.md) 
行为纳入 TCP 套接字中。将 `ipconfigUSE_TCP_WIN` 设为 0，以排除 TCP 套接字中的滑动窗口行为。

滑动窗口可以增加吞吐量，同时最大限度地减少网络流量，
其代价是消耗更多 RAM。

通过 
`FREERTOS_SO_WIN_PROPERTIES` 参数可以将滑动窗口大小的默认值改为 `FreeRTOS_setsockopt()`。滑动窗口
大小以 MSS 为单位（因此，如果 MSS 设为 200 字节，则
大小为 2 的滑动窗口等于 400 字节)，并且必须始终小于
或等于两个方向上的内部缓冲区的大小。

如果[监听套接字](TCP_Networking_Tutorial_TCP_Client_and_Server.md)
为响应传入的请求创建一个新的套接字，
则新套接字将继承监听套接字的滑动窗口
大小。


### UDP 特定常量

#### ipconfigUDP_MAX_RX_PACKETS

`ipconfigUDP_MAX_RX_PACKETS` 定义了
 UDP 套接字的 Rx 队列中可以存在的最大数据包数量。例如，如果 `ipconfigUDP_MAX_RX_PACKETS` 
设为 5，并且 UDP 套接字上已经有 5 个数据包排队，
则随后在该套接字上接收的数据包将被丢弃，直到队列长度
再次小于 5。


#### ipconfigUDP_MAX_SEND_BLOCK_TIME_TICKS

套接字有发送阻塞时间的属性。如果调用了 `FreeRTOS_sendto()` 但
无法获取网络缓冲区，则调用 RTOS 的任务将保留在阻塞状态
（以便其他任务可以继续执行），直到网络缓冲区
变为可用或发送阻塞时间到期。如果发送阻塞时间过期，
则发送操作中止。

允许的最大发送阻塞时间
为 `ipconfigUDP_MAX_SEND_BLOCK_TIME_TICKS` 设置的值。为
最大可允许发送阻塞时间设置上限可防止
所有网络缓冲区正在使用，而且处理（并随后释放）
网络缓冲区的任务本身进入阻塞状态以等待使用网络缓冲区时发生死锁。

`ipconfigUDP_MAX_SEND_BLOCK_TIME_TICKS` 以 RTOS 滴答为单位。通过将以毫秒
为单位的时间除以
`portTICK_PERIOD_MS` 可以得到以滴答为单位的时间。


#### ipconfigUDP_PASS_ZERO_CHECKSUM_PACKETS

如果 `ipconfigUDP_PASS_ZERO_CHECKSUM_PACKETS` 设为 1，则 FreeRTOS-Plus-TCP 将接收 UDP 数据包，
这些数据包将校验和值设为 0，符合 UDP 规范。

如果 `ipconfigUDP_PASS_ZERO_CHECKSUM_PACKETS` 设为 0 ，则 FreeRTOS-Plus-TCP 将丢弃 UDP 数据包，
这些数据包将校验和值设为 0，偏离了 UDP 规范，但更安全。

**注意：**此配置参数默认为 0。


#### ipconfigUDP_TIME_TO_LIVE

定义传出 UDP 数据包中使用的[生存时间](http://en.wikipedia.org/wiki/Time_to_live) (TTL) 值。

  
### 影响套接字行为的其他常量

#### ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND

套接字的地址是其 IP 地址和移植号的组合。 [FreeRTOS_bind()](API/bind.md)
用于手动分配移植号至套接字（以将套接字‘绑定’至移植），但客户端套接字 
通常不需要手动绑定（那些启动传出连接而不是
等待已知移植号上的传入连接的套接字）。如果 `ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND` 设为 1， 
则在尚未绑定的套接字上调用 `FreeRTOS_sendto()` 将导致 IP 堆栈自动 
将套接字绑定到移植号（范围：`socketAUTO_PORT_ALLOCATION_START_NUMBER` 到 0xffff）。 
如果 `ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND` 设为 0，则在套接字上调用未绑定的 `FreeRTOS_sendto()`  
将导致中止发送操作。


#### ipconfigINCLUDE_FULL_INET_ADDR

实现 [FreeRTOS_inet_addr()](API/inet_addr.md) 需要使用相对较大的字符串处理例程
。为节省代码空间，完整的 `FreeRTOS_inet_addr()` 实现
定位可选，并提供了一个更小、更快的替代方案，称为
`FreeRTOS_inet_addr_quick()`。`FreeRTOS_inet_addr()` 获取
十进制点格式的 IP（例如 “192.168.0.1”）作为其参数。
`FreeRTOS_inet_addr_quick()` 采用四个分隔开的数字组成的八进制数 IP 地址
（例如，192, 168, 0, 1）作为其参数。如果
`ipconfigINCLUDE_FULL_INET_ADDR` 设为 1，则 `FreeRTOS_inet_addr()` 和
`FreeRTOS_indet_addr_quick()` 都可用。如果 `ipconfigINCLUDE_FULL_INET_ADDR` 
未设为 1，则仅 `FreeRTOS_indet_addr_quick()` 可用。


#### ipconfigSELECT_USES_NOTIFY

此选项仅在套接字选择函数被激活时使用（`ipconfigSUPPORT_SELECT_FUNCTION`  
非 0 时）。从同一任务为给定套接字调用 `select()` 时，不需要此宏。只有 
当相同套接字上有多个任务在使用选择函数时，此选项*可以*防止死锁。问题是 
有多个任务会等待并清除事件位 `eSELECT_CALL_IP`。宏 `ipconfigSELECT_USES_NOTIFY`  
默认为 0，表示未激活。


#### ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME

用于从套接字读取数据的 API 函数可以进入阻塞状态以等待数据
变得可用。`ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` 设置默认阻塞时间
以 RTOS 滴答为单位。如果 `ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` 未定义，
则默认阻塞时间将被设置为 `portMAX_DELAY`，意味着读取套接字时进入阻塞状态的 RTOS 任务
将不会退出阻塞状态，直至数据可用。
请注意， 阻塞状态下的任务不会占用任何 CPU 时间。

`ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` 以滴答为单位。宏 `pdMS_TO_TICKS()`  
和 `portTICK_PERIOD_MS` 可以用来将以毫秒为单位的时间转换成以滴答为单位的时间 
。

超时时间可以随时更改，只需使用 `FREERTOS_SO_RCVTIMEO` 参数
和 `FreeRTOS_setsockopt()` 即可。**请注意：**使用无限阻塞时间
应十分谨慎，以避免出现所有任务被无限阻塞
以等待另一个 RTOS 任务（该任务也被无限阻塞）
来释放网络缓冲区的情况。

通过将发送和接收阻塞时间都设置为 0 可以将套接字设置为非阻塞模式。
当 RTOS 任务使用多个套接字时可能需要该模式：
在这种情况下，可以通过 
`FreeRTOS_select()` 在所有套接字上执行阻塞操作，或者 RTOS 任务可以将 `ipconfigSOCKET_HAS_USER_SEMAPHORE` 设为 1，
然后在自己的信号量上阻塞。


#### ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME

写入套接字时，写入操作可能无法立即进行。例如，
取决于配置，写入可能需要等待网络
缓冲区变成可用。用于将数据写入套接字的 API 函数
可进入阻塞状态等待写入成功。`ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME` 设置默认阻塞时间
（以 RTOS 滴答为单位）。如果 `ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME` 未定义，
则默认阻塞时间将被设置为 `portMAX_DELAY`，意味着读取套接字时进入阻塞状态的 RTOS 任务
将不会退出阻塞状态，直至数据可用。
请注意， 阻塞状态下的任务不会占用任何 CPU 时间。

`ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` 以滴答为单位。宏 `pdMS_TO_TICKS()`  
和 `portTICK_PERIOD_MS` 可以用来将以毫秒为单位的时间转换成以滴答为单位的时间 
。

超时时间可以随时更改，只需使用 `FREERTOS_SO_SNDTIMEO` 参数
和 `FreeRTOS_setsockopt()` 即可。**请注意：**使用无限阻塞时间
应十分谨慎，以避免出现所有任务被无限阻塞
以等待另一个 RTOS 任务（该任务也被无限阻塞）
来释放网络缓冲区的情况。

通过将发送和接收阻塞时间都设置为 0 可以将套接字设置为非阻塞模式。
当 RTOS 任务使用多个套接字时可能需要该模式：
在这种情况下，可以通过
`FreeRTOS_select()` 在所有套接字上执行阻塞操作，或者 RTOS 任务可以将 `ipconfigSOCKET_HAS_USER_SEMAPHORE` 设为 1，
然后在自己的信号量上阻塞。

通过将发送和接收阻塞时间都设置为 0 可以将套接字设置为
非阻塞模式。


#### ipconfigSOCKET_HAS_USER_SEMAPHORE

在默认情况下，套接字将阻塞无法立即完成的发送
或接收操作。请参阅 `ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME` 
和 `ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME` 参数的描述。

如果 RTOS 任务正在使用多个套接字，且在一个套接字上无法一次性进入阻塞状态，则
可以将套接字设置为非阻塞模式，并且 RTOS 任务可以在所有套接字上一次性进入阻塞状态，
方法是使用 `FreeRTOS_select()` 函数，或者
将 `ipconfigSOCKET_HAS_USER_SEMAPHORE` 设为 1，使用 `FREERTOS_SO_SET_SEMAPHORE` 
参数和 `FreeRTOS_setsockopt()` 向套接字提供信号量，
然后在信号量上进入阻塞状态。当任何套接字能够进行处理时会提供信号量——
此时 RTOS 任务可以通过调用非阻塞 API 单独检查所有套接字，
确定是哪个套接字使任务
不被阻塞。


#### ipconfigSOCKET_HAS_USER_WAKE_CALLBACK

可以安装应用程序钩子，该钩子将在每个重要套接字事件后被调用。该钩子 
有一个参数：socket，并且它没有返回值：`typedef void (* SocketWakeupCallback_t)( Socket_t pxSocket );`

调用钩子的原因可能是以下一个或多个事件：

```c
        eSOCKET_RECEIVE = 0x0001, /* Reception of new data. */  
        eSOCKET_SEND    = 0x0002, /* Some data has been sent. */  
        eSOCKET_ACCEPT  = 0x0004, /* A new TCP client was detected, please call accept(). */  
        eSOCKET_CONNECT = 0x0008, /* A TCP connect has succeeded or timed-out. */  
        eSOCKET_BOUND   = 0x0010, /* A socket got bound. */  
        eSOCKET_CLOSED  = 0x0020, /* A TCP connection got closed. */  
        eSOCKET_INTR    = 0x0040, /* A blocking API call got interrupted, because  
                                   * the function FreeRTOS_SignalSocket() was called. */  

```

通常，钩子只会通知拥有套接字的任务，以便套接字立即得到关注。

  
#### ipconfigSUPPORT_SELECT_FUNCTION

将 `ipconfigSUPPORT_SELECT_FUNCTION` 设为 1，以纳入对 [FreeRTOS_select()](API/select.md) 
和关联 API 函数的支持，或者将其设为 0，以将 `FreeRTOS_select()` 和
关联 API 函数排除出构建。

  
#### ipconfigSUPPORT_SIGNALS

如果 `ipconfigSUPPORT_SIGNALS` 设为 1，则 `FreeRTOS_SignalSocket()` API
函数包含在构建中。 [FreeRTOS_SignalSocket()](API/FreeRTOS_SignalSocket.md)
可用于向套接字发送信号，以使任何在读取套接字时
进入阻塞状态的任务退出阻塞状态（中止读取操作阻塞）。

  
#### ipconfigUSE_CALLBACKS

当此宏被定义为非 0 时，可以将特定的应用程序钩子（回调函数） 
绑定到套接字。每个类型的事件都有不同的应用程序钩子：

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

### 影响 ARP 行为的常量

#### ipconfigARP_CACHE_ENTRIES

ARP 缓存是一个将 IP 地址映射到 MAC 地址的表。

IP 堆栈只能向与 IP 地址关联的已知 MAC 地址或者用于联系远程 IP 地址的路由器 MAC 地址发送 UDP 消息
以移除 IP
地址。当从远程 IP 地址接收到 UDP 消息时，
MAC 地址和 IP 地址被添加到 ARP 缓存。当 UDP 消息
被发送到尚未出现在 ARP 缓存中的远程 IP 地址时，
UDP 消息会被请求所需 MAC 地址信息的 ARP 消息
替换掉。

`ipconfigARP_CACHE_ENTRIES` 定义了可在 ARP 表中同时存在的条目的最大数量。


#### ipconfigARP_STORES_REMOTE_ADDRESSES

仅限高级用户。

在下述情况提供 `ipconfigARP_STORES_REMOTE_ADDRESSES`：
一个需要回复的消息从互联网而来，但此消息来自连接到局域网
的计算机，而非通过定义的网关送达。在回复消息之前，
TCP/IP 堆栈 RTOS 任务将查询 ARP 表中消息的 IP 地址，但如果
`ipconfigARP_STORES_REMOTE_ADDRESSES` 设为 0，则 ARP 
将返回定义网关的 MAC 地址，因为目标地址
不在网络掩码中。这可能妨碍答复达到其预期目的地
。

如果 `ipconfigARP_STORES_REMOTE_ADDRESSES` 设为 1，则远程地址
也将存储在 ARP 表中，一同存储的还有发送消息的
MAC 地址。这可以让上述场景中的消息
正确进行路由和传送。



#### ipconfigARP_USE_CLASH_DETECTION

当分配链接层地址时，驱动器将通过发送 ARP 请求来测试该地址是否已被其他设备
使用。因此，`ipconfigARP_USE_CLASH_DETECTION` 必须被定义为非零。


#### ipconfigMAX_ARP_AGE

`ipconfigMAX_ARP_AGE` 定义了在 ARP 表中创建或刷新条目
与由于过时而移除该条目之间的最大时间间隔。
已为接近最大存在时间的 ARP 缓存条目发送新的 ARP 请求
。

`ipconfigMAX_ARP_AGE` 以十秒为单位，因此 150 的值等于
1500 秒（或 25 分钟）。


#### ipconfigMAX_ARP_RETRANSMISSIONS

未引起 ARP 响应的 ARP 请求将被重新传输，
在中止 ARP 请求之前，会重新传输 `ipconfigMAX_ARP_RETRANSMISSIONS` 次
。

  
#### ipconfigUSE_ARP_REMOVE_ENTRY

仅限高级用户。

如果 `ipconfigUSE_ARP_REMOVE_ENTRY` 设为 1，则 `ulARPRemoveCacheEntryByMac()` 
将包含于构建中。`ulARPRemoveCacheEntryByMac()` 使用 MAC 地址
查找 ARP 缓存中的条目，然后将其移除。如果 MAC 地址是
在 ARP 缓存中找到的，则返回与 MAC 地址关联的 IP 地址
。如果在 ARP 缓存中找不到 MAC 地址，则返回 0。

```c
uint32_t ulARPRemoveCacheEntryByMac( const MACAddress_t * pxMACAddress );  

ulARPRemoveCacheEntryByMac() function prototype  

```


#### ipconfigUSE_ARP_REVERSED_LOOKUP

仅限高级用户。

通常 ARP 会在 MAC 地址中查找 IP 地址。如果 `ipconfigUSE_ARP_REVERSED_LOOKUP`
设为 1，则相反的函数也可用。
`eARPGetCacheEntryByMac()` 在 IP 地址中查找 MAC 地址。

```c
eARPLookupResult_t eARPGetCacheEntryByMac( MACAddress_t * const pxMACAddress,  
                                           uint32_t *pulIPAddress );  
  
eARPGetCacheEntryByMac() function prototype  

```


### 影响 DHCP 和名称服务行为的常量

#### ipconfigDHCP_FALL_BACK_AUTO_IP

仅在使用 DHCP 时可用。如果没有 DHCP 服务器响应，请使用“自动 IP” ；设备将分配一个随机链接层 
IP 地址，并测试它是否仍然可用。


#### ipconfigDHCP_REGISTER_HOSTNAME

通常， DHCP 服务器可以显示具有租用 IP 地址的设备的名称。
当 `ipconfigDHCP_REGISTER_HOSTNAME` 设为 1 时，运行 FreeRTOS-Plus-TCP 的设备
会从应用程序提供的钩子（或‘回调’）函数中返回一个人类可读的名称，
让 DHCP 服务器通过此名称来识别自己。
上述钩子函数名为 `pcApplicationHostnameHook()`。

`ipconfigDHCP_REGISTER_HOSTNAME` 设为 1 时，应用程序必须提供
具有以下名称和原型的钩子（回调）函数：

```c
const char *pcApplicationHostnameHook( void );  

```

应用程序所提供钩子函数的名称和原型，该函数返回设备名称   


#### ipconfigDNS_CACHE_address_PER_ENTRY

查找 URL 时，可能会收到多个答案（IP 地址）。此宏决定 
每个 URL 将存储多少个答案。


#### ipconfigDNS_CACHE_ENTRIES

如果 `ipconfigUSE_DNS_CACHE` 设为 1，则 `ipconfigDNS_CACHE_ENTRIES` 定义
DNS 缓存中的条目数。

  
#### ipconfigDNS_CACHE_NAME_LENGTH

DNS 主机名可以使用的最大字符数，包括 NULL
终止符。

  
#### ipconfigDNS_REQUEST_ATTEMPTS

查找主机时，库必须发送 DNS 请求并等待结果。此过程最多将重复 
 `ipconfigDNS_REQUEST_ATTEMPTS` 次。宏 `ipconfigDNS_SEND_BLOCK_TIME_TICKS` 决定了 
函数 `FreeRTOS_sendto()` 可能阻塞多久。

在发送时，默认情况下，函数将阻塞最多 500 毫秒。在等待回复时， 
`FreeRTOS_recvfrom()` 最多等待 5000 毫秒。


#### ipconfigDNS_USE_CALLBACKS

定义后，函数 `FreeRTOS_gethostbyname_a()` 变成可用。此函数将启动 DNS 查找 
并设置应用程序钩子。当找到 URL 时，或当达到超时时间时，将调用 
此用户函数（或钩子）。请注意，函数 `FreeRTOS_gethostbyname_a()` 不会使用宏  
`ipconfigDNS_SEND_BLOCK_TIME_TICKS` 和 `ipconfigDNS_RECEIVE_BLOCK_TIME_TICKS`。


#### ipconfigMAXIMUM_DISCOVER_TX_PERIOD

当 `ipconfigUSE_DHCP` 设为 1 时，DHCP 请求将以
增加的时间间隔发送，直到从 DHCP 服务器收到并接受一个响应，
或者传输间隔达到 
`ipconfigMAXIMUM_DISCOVER_TX_PERIOD`。TCP/IP 堆栈将恢复为使用
静态 IP 地址作为参数传递到 [FreeRTOS_IPInit()](API/FreeRTOS_IPInit.md)，条件是 
重新传输时间间隔达到 `ipconfigMAXIMUM_DISCOVER_TX_PERIOD` 时也没有
收到 DHCP 的答复。


#### ipconfigUSE_DHCP

如果 `ipconfigUSE_DHCP` 设为 1，则 FreeRTOS-Plus-TCP 将尝试从 DHCP 服务器
检索 IP 地址、子网掩码、DNS 服务器地址和网关地址，并
在无法获取 IP 地址的情况下恢复为使用定义的静态地址。

如果 `ipconfigUSE_DHCP` 为 0，则 FreeRTOS-Plus-TCP 将不会尝试从 DHCP 服务器获取其地址信息
。相反，它将立即使用定义的静态地址
信息。


#### ipconfigUSE_DHCP_HOOK

正常 [DHCP](DHCP.md) 事务涉及以下序列：

1. 客户端发送 DHCP 发现数据包，向 DHCP 服务器请求 IP 地址。
2. DHCP 服务器通过包含所提供 IP 地址的提供数据包来响应。
3. 客户端发送 DHCP 请求数据包以领取所提供的 IP 地址
4. DHCP 服务器发送确认数据包，以授权使用所提供 IP 地址的客户端， 
   并向客户端发送其他配置信息。其他配置信息 
   通常包括[网关](router.md) IP 地址和 [DNS](DNS.md) 服务器 IP 地址 
   以及 IP 地址租用长度。

如果 `ipconfigUSE_DHCP_HOOK` 设为 1，则 FreeRTOS-Plus-TCP 将调用
应用程序提供的名为 `xApplicationDHCPUserHook()` 的钩子（或“回调” ）函数，
该调用在初始发现数据包被发送之前和收到 DHCP 的提供之后均进行——
钩子函数可用于在 DHCP 序列中的这两个阶段中的任一个
终止 DHCP 进程。例如，
即使在 [ipconfigUSE_DHCP](#ipconfiguse_dhcp) 设置为 1 时，应用程序编写者也可以
有效地禁用 DHCP，禁用方法是在初始发现数据包被发送之前
终止 DHCP 进程。作为另一个示例，应用程序写入器可以检查静态 IP 地址
与网络的兼容性，设备通过接收 DHCP 服务器提供的 IP 地址
连接到该网络，但随后终止 DHCP 进程，而无需
发送请求数据包以领取所提供的 IP 地址。

如果 `ipconfigUSE_DHCP_HOOK` 设为 1，则应用程序编写者必须
提供具有以下名称和原型的钩子（回调）函数：

```c
eDHCPCallbackAnswer_t xApplicationDHCPHook( eDHCPCallbackPhase_t eDHCPPhase,  
                                            uint32_t ulIPAddress );  

```
*DHCP 应用程序钩子函数的名称和原型*


`eDHCPCallbackQuestion_t` 和 `eDHCPCallbackAnswer_t` 的定义如下所示

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
*EDHCPCallbackQuestion_t 和 eDHCPCallbackAnswer_t 定义*

仅出于示例目的，以下是 `xApplicationDHCPHook` 的引用实现，
它让 DHCP 序列可以进行直到提供 IP 地址之时，
此时，比较所提供的 IP 地址与静态
配置的 IP 地址。如果提供的和静态配置的 IP 地址是
在同一子网上，则使用静态配置的 IP 地址。如果
提供的和静态配置的 IP 地址不在同一子网上，则
使用 DHCP 服务器提供的 IP 地址。

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
*xApplicationDHCPHook() 参考实现*

当 `eDHCPPhase` 参数设置为 `eDHCPPhasePreDiscover` 时，
ulIPAddress 参数设置为正在使用的 IP 地址。`eDHCPPhase` 参数设为 
 `eDHCPPhasePreRequest` 时，`ulIPAddress` 参数设为 DHCP 服务器所提供的 IP 地址 
。


#### ipconfigUSE_DNS

将 `ipconfigUSE_DNS` 设置为 1 以包含基本的 DNS 客户端/解析器。DNS 
通过 [FreeRTOS_gethostbyname()](API/gethostbyname.md) API 函数使用。

  
#### ipconfigUSE_DNS_CACHE

如果 `ipconfigUSE_DNS_CACHE` 设为 1，则将启用 DNS 缓存。如果 `ipconfigUSE_DNS_CACHE` 
 设为 0，则 DNS 缓存将被禁用。

  
#### ipconfigUSE_LLMNR

将 `ipconfigUSE_LLMNR` 设为 1 以包含 [LLMNR](LLMNR.md)。

  
#### ipconfigUSE_NBNS

将 `ipconfigUSE_NBNS` 设为 1 以包含 [NBNS](NetBIOS.md)。

  
### 影响 IP 和 ICMP 行为的常量

#### ipconfigFORCE_IP_DONT_FRAGMENT

此宏与 IP 碎片化有关。通过互联网发送 IP 数据包时，大数据包可能被拆分为 
较小的部件，然后由接收器组合。发件人可以确定是否允许进行这种碎片化。 
默认情况下，`ipconfigFORCE_IP_DONT_FRAGMENT` 为 0，这意味着允许碎片化。

请注意，FreeRTOS-Plus-TCP 堆栈不接受收到的碎片数据包。


#### ipconfigICMP_TIME_TO_LIVE

在回复 ICMP 数据包时，TTL 字段将被设置为此宏的值。默认值为 64 
（根据 RFC 1700 的建议）。最小值为 1，最大值为 255。


#### ipconfigIP_PASS_PACKETS_WITH_IP_OPTIONS

如果 `ipconfigIP_PASS_PACKETS_WITH_IP_OPTIONS` 设为 1，则 FreeRTOS-Plus-TCP 接受包含 IP 选项的 IP 数据包，
但不处理这些选项（不支持 IP 选项）。

如果 `ipconfigIP_PASS_PACKETS_WITH_IP_OPTIONS` 设为 0 ，则 FreeRTOS-Plus-TCP 将丢弃包含 IP 选项的 IP 数据包
。


#### ipconfigREPLY_TO_INCOMING_PINGS

如果 `ipconfigREPLY_TO_INCOMING_PINGS` 设为 1，则 TCP/IP 堆栈将
生成对传入 ICMP 回显 (ping) 请求的响应。

  
#### ipconfigSUPPORT_OUTGOING_PINGS

如果 `ipconfigSUPPORT_OUTGOING_PINGS` 设为 1，则 `FreeRTOS_SendPingRequest()` 
API 函数可用。

  
### 提供目标支持的常量

#### ipconfigHAS_INLINE_FUNCTIONS

如果正在使用的编译器支持内联函数，并且 `portINLINE` 定义为
编译器的正确内联关键字，则将 `ipconfigHAS_INLINE_FUNCTIONS` 
设为 1。否则将 `ipconfigHAS_INLINE_FUNCTIONS` 设为 0，这会导致
一些内联函数使用替代宏实现。

  
#### ipconfigRAND32()

TCP/IP 堆栈调用 `ipconfigRAND32()` 以生成一个随机数，
然后用作 DHCP 事务号。随机数生成
通过此宏执行，以使应用程序可以使用自己的随机数生成
方法。例如，可能可以通过以下方式生成随机数：
在模拟输入上采样噪声。

**注意：**
在 TCP/IP 堆栈启动之前，必须接种随机数生成器，
即在调用 [FreeRTOS_IPInit()](API/FreeRTOS_IPInit.md) 之前。


#### ipconfigIS_VALID_PROG_ADDRESS( x )

在使用可安装应用程序钩子的情况下，调用此宏以检查给定地址是否引用 
有效（指令）内存。以下是一个小例子，取自 FreeRTOS_TCP _IP.c：

```c
   if( ipconfigIS_VALID_PROG_ADDRESS( pxSocket->u.xTCP.pxHandleSent ) )  
    {  
        pxSocket->u.xTCP.pxHandleSent( pxSocket, ulCount );  
    }  

```

