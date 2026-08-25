---
title: TCP/IP 特定追踪钩子宏
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

用于调试和优化 FreeRTOS-Plus-TCP 行为

**另请参阅 FreeRTOSIOConfig.h 中的[调试、追踪和日志记录](TCP_IP_Configuration.md#LOGGING)设置。** 


### 描述

追踪钩子宏可用于在 FreeRTOS-Plus-TCP 应用程序运行期间
收集数据。这些数据可用于调试和
优化目的。

在 RTOS 的 TCP 源代码中，关键关注点包含一些宏，
应用程序可定义这些宏，以提供
特定的追踪功能。应用程序仅需
实现相关宏，默认情况下未实现的宏
将保留为空（不生成任何代码）。

建议在头文件中实现追踪宏，然后 
在 [FreeRTOSIPConfig.h](TCP_IP_Configuration.md) 底部#包含该头文件。

在 Windows 模拟器中运行的 FreeRTOS-Plus-TCP 示例（可
从本网站下载）使用
追踪宏来收集 TCP/IP 堆栈运行时信息，这些信息
可通过 TCP/IP CLI 接口查看。

可以定义的宏如下：

+ iptraceNETWORK_DOWN()  

  网络驱动程序指示网络连接已断开时，调用此宏（并非所有网络驱动程序都可实现）。  

+ iptraceNETWORK_BUFFER_RELEASED( pxBufferAddress )  

  地址为 pxBufferAddress 的网络缓冲区释放回 TCP/IP 堆栈时，调用此宏。  

+ iptraceNETWORK_BUFFER_OBTAINED( pxBufferAddress )  

  RTOS 任务从 TCP/IP 堆栈获取地址为 pxBufferAddress 的网络缓冲区时，调用此宏。  

+ iptraceNETWORK_BUFFER_OBTAINED_FROM_ISR( pxBufferAddress )  

  中断服务程序从 TCP/IP 堆栈获取地址为 pxBufferAddress 的网络缓冲区时，调用此宏。  

+ iptraceFAILED_TO_OBTAIN_NETWORK_BUFFER()  

  任务尝试获取网络缓冲区，但经过定义的阻塞期后缓冲区仍不可用时，调用此宏。  

+ iptraceFAILED_TO_OBTAIN_NETWORK_BUFFER_FROM_ISR()  

  中断服务程序尝试获取网络缓冲区，但缓冲区不可用时，调用此宏。  

+ iptraceCREATING_ARP_REQUEST( ulIPAddress )  

  IP 生成 ARP 请求数据包时，调用此宏。  

+ iptraceARP_TABLE_ENTRY_WILL_EXPIRE( ulIPAddress )  

  因 ARP 缓存中对应 IP 地址 ulIPAddress 的条目已过时而即将发送 ARP 请求时，调用此宏。 
  ulIPAddress 是以网络字节顺序表示的 32 位数字。  

+ iptraceARP_TABLE_ENTRY_EXPIRED( ulIPAddress )  

  ARP 缓存中对应 IP 地址 ulIPAddress 的条目被删除时，调用此宏。 
  ulIPAddress 是以网络字节顺序表示的 32 位数字。  

+ iptraceARP_TABLE_ENTRY_CREATED( ulIPAddress, ucMACAddress )  

  在 ARP 表中创建新条目以将 IP 地址 ulIPAddress 映射到 MAC 地址 ucMACAddress 时，调用此宏。 
  ulIPAddress 是以网络字节顺序表示的 32 位数字。ucMACAddress 
  是指向 MACAddress_t 结构体的指针。  

+ iptraceSENDING_UDP_PACKET( ulIPAddress )  

  向 IP 地址 ulIPAddress 发送 UDP 数据包时，调用此宏。ulIPAddress 是以网络字节顺序表示的 32 位数字。  

+ iptracePACKET_DROPPED_TO_GENERATE_ARP( ulIPAddress )  

  因 ARP 缓存中没有 IP 地址 ulIPAddress 的条目 
  而丢弃发往该 IP 地址的数据包时，调用此宏。该数据包会自动替换为 ARP 数据包。 
  ulIPAddress 是以网络字节顺序表示的 32 位数字。  

+ iptraceICMP_PACKET_RECEIVED()  

  收到 ICMP 数据包时，调用此宏。  

+ iptraceSENDING_PING_REPLY( ulIPAddress )  

  向 IP 地址 ulIPAddress 发送 ICMP 回显应答（ping 应答）以响应 
  来自同一地址的 ICMP 回显请求（ping 请求）时，调用此宏。ulIPAddress 是以网络字节顺序 
  表示的 32 位数字。  

+ traceARP_PACKET_RECEIVED()  

  收到 ARP 数据包（即使本地网络节点未参与该 ARP 事务）时，调用此宏。  

+ iptracePROCESSING_RECEIVED_ARP_REPLY( ulIPAddress )  

  接收到 ARP 应答后，ARP 缓存即将更新时，调用此宏。ulIPAddress 
  保存 ARP 消息的目标 IP 地址（以网络字节顺序表示的 32 位数字），该地址可能不是 
  本地网络节点（取决于 [FreeRTOSIPConfig.h](TCP_IP_Configuration.md) 设置）。  

+ iptraceSENDING_ARP_REPLY( ulIPAddress )  

  发送 ARP 应答以响应来自 IP 地址 ulIPAddress 的 ARP 请求。 
  ulIPAddress 是以网络字节顺序表示的 32 位数字。  

+ iptraceFAILED_TO_CREATE_SOCKET()  

  调用 FreeRTOS_socket() 失败，因为没有足够的 [FreeRTOS 堆内存](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 
  可用于创建套接字结构体。  

+ iptraceRECVFROM_DISCARDING_BYTES( xNumberOfBytesDiscarded )  

  FreeRTOS_recvfrom() 丢弃 xNumberOfBytesDiscarded 个字节，因为收到的字节数 
  超过用户提供的缓冲区 
  （作为 FreeRTOS_recvfrom() 函数参数传入的缓冲区）可容纳的字节数。  

+ iptraceETHERNET_RX_EVENT_LOST()  

  因以下任一原因而丢弃网络驱动程序收到的数据包时，调用此宏： 
  网络事件队列中的空间不足（请参阅 
  [FreeRTOSIPConfig.h](TCP_IP_Configuration.md) 中的 ipconfigEVENT_QUEUE_LENGTH 设置），收到的数据包的数据长度无效， 
  或者没有可用的网络缓冲区（请参阅 
  [FreeRTOSIPConfig.h](TCP_IP_Configuration.md) 中的 ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS 设置）。请注意，此宏由网络驱动程序 
  （而不是 TCP/IP 堆栈）调用，第三方提供的驱动程序可能根本不会调用此宏。  

+ iptraceSTACK_TX_EVENT_LOST( xEvent )  

  因网络事件队列空间不足而丢弃 TCP/IP 堆栈生成的数据包时，调用此宏 
  （请参阅 [FreeRTOSIPConfig.h](TCP_IP_Configuration.md) 中的 ipconfigEVENT_QUEUE_LENGTH 设置）。  

+ iptraceNETWORK_EVENT_RECEIVED( eEvent )  

  TCP/IP 堆栈处理先前发布到网络事件队列的事件时，调用此宏。 
  eEvent 可能为以下任意一值： 

  * eNetworkDownEvent - 网络接口已丢失，并且/或者需要[重新]连接。

  * eNetworkRxEvent - 网络接口已将接收的以太网帧排入队列。

  * eARPTimerEvent - ARP 定时器已过期。

  * eStackTxEvent - 软件堆栈已将要传输的数据包排入队列。

  * eDHCPEvent - 处理 DHCP 状态机。请注意，这些事件由私有 eIPEvent_t 类型定义， 
    该类型通常不可访问。  

+ iptraceBIND_FAILED( xSocket, usPort )  

  调用 FreeRTOS_bind() 失败。usPort 是要绑定到套接字 xSocket 的端口号。  

+ iptraceDHCP_REQUESTS_FAILED_USING_DEFAULT_IP_ADDRESS( ulIPAddress )  

  因无法从 DHCP 获取 IP 地址而使用默认 IP 地址时，调用此宏。 
  ulIPAddress 是以网络字节顺序表示的 32 位数字。  

+ iptraceSENDING_DHCP_DISCOVER()  

  发送 DHCP 发现数据包时，调用此宏。  

+ iptraceSENDING_DHCP_REQUEST()  

  发送 DHCP 请求数据包时，调用此宏。  

+ iptraceNETWORK_INTERFACE_TRANSMIT()  

  网络驱动程序向网络发送数据包时，调用此宏。请注意，此宏由网络 
  驱动程序（而不是 TCP/IP 堆栈）调用，第三方提供的驱动程序可能根本不会调用此宏。  

+ iptraceNETWORK_INTERFACE_RECEIVE()  

  网络驱动程序从网络接收到数据包时，调用此宏。请注意，此宏由 
  网络驱动器程序（而不是 TCP/IP 堆栈）调用，第三方提供的驱动程序可能根本不会调用 
  此宏。  

+ iptraceSENDING_DNS_REQUEST()  

  发送 DNS 请求时，调用此宏。  

+ iptraceWAITING_FOR_TX_DMA_DESCRIPTOR()  

  因驱动程序必须等待 DMA 描述符变为空闲 
  而导致网络驱动程序级别的传输无法立即完成时，调用此宏。尝试增加 
  FreeRTOSConfig.h 中的 configNUM_TX_ETHERNET_DMA_DESCRIPTORS 设置（如果使用的网络驱动程序存在该设置）。  

+ iptraceDHCP_SUCCEDEED( ulOfferedIPAddress )   

  DHCP 协商完成且 ulOfferedIPAddress 中的 IP 地址提供给设备时，调用此宏。  

+ iptraceDROPPED_INVALID_ARP_PACKET( pxARPHeader )  

  因地址为 pxARPHeader 的标头中的协议和硬件字段无效而丢弃 ARP 数据包时，调用此宏。  

+ iptraceFAILED_TO_CREATE_EVENT_GROUP()  

  在创建新套接字期间无法创建事件组（可能是由于堆空间不足）时，调用此宏。  

+ iptraceMEM_STATS_CLOSE()  

  应用程序需停止收集内存统计信息时，调用此宏。  

+ iptraceMEM_STATS_CREATE( xMemType, pxObject, uxSize )  

  从堆中分配了对象（地址为 pxObject，类型为 xMemType，大小为 uxSize）时，调用此宏。  

+ iptraceMEM_STATS_DELETE( pxObject )  

  地址为 pxObject 的对象已释放且内存已返回到堆时，调用此宏。  

+ iptraceNETWORK_INTERFACE_INPUT( uxDataLength, pucEthernetBuffer )  

  收到长度为 uxDataLength 且内容位于地址 pucEthernetBuffer 处的数据包时，调用此宏。  

+ iptraceNETWORK_INTERFACE_OUTPUT( uxDataLength, pucEthernetBuffer )  

  发送长度为 uxDataLength 且内容位于地址 pucEthernetBuffer 处的数据包时，调用此宏。  

+ iptraceNO_BUFFER_FOR_SENDTO()  

  调用 FreeRTOS_sendto() 以尝试分配缓冲区，但经过定义的阻塞期后 
  缓冲区仍不可用时，调用此宏。  

+ iptraceRECVFROM_INTERRUPTED()  

  对 FreeRTOS_recvfrom() 的阻塞调用因 FreeRTOS_SignalSocket() 的调用而中断时，调用此宏。  

+ iptraceRECVFROM_TIMEOUT()  

  FreeRTOS_recvfrom() 经过定义的阻塞期后仍未在给定套接字上获取数据时，调用此宏。  

+ iptraceSENDTO_DATA_TOO_LONG()  

  请求通过调用 FreeRTOS_sendto() 发送的数据太长而无法发送时，调用此宏。  

+ iptraceSENDTO_SOCKET_NOT_BOUND()  

  对 FreeRTOS_sendto() 的调用中使用的套接字尚未绑定到端口时，调用此宏。   



