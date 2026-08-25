---
title: "xApplicationDHCPHook_Multi()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h
  
***注意**：仅当 `ipconfigUSE_DHCP_HOOK` 在 FreeRTOSIPConfig.h 文件中设置为 1 时才需要定义此钩子。

```c
eDHCPCallbackAnswer_t xApplicationDHCPHook_Multi( eDHCPCallbackPhase_t eDHCPPhase,
                                                  struct xNetworkEndPoint * pxEndPoint,
                                                  IP_Address_t * pxIPAddress 
                                                );
```

`xApplicationDHCPHook_Multi` 是应用程序定义的钩子（或回调）函数， 
由 FreeRTOS-Plus-TCP 堆栈调用，用于检查设备是应发送 DHCPv4 的 'Discover' 和 'Request' 消息或 DHCPv6 的 'Solicitation' 
和 'Request' 消息，以完成获取动态 IP 地址的过程， 
还是应使用默认的静态 IP。

回调函数由应用程序编写者实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上述原型（包括函数名称）完全匹配。应用程序钩子中的代码 
不应调用会导致阻塞的 FreeRTOS-Plus-TCP API。这样很容易导致 
死锁。

应用程序钩子执行时，会借用 IP 任务的优先级和堆栈。因此， 
建议应用程序钩子尽量简短，只做一些简单的工作，例如唤醒其他应用程序任务， 
由这些任务进行进一步处理。


**参数：**

+ *eDHCPPhase*

  对于 DHCPv4，当 TCP 堆栈即将发送 Request 或 Discover 消息时，该参数可以为 eDHCPPhasePreRequest 或 eDHCPPhasePreDiscover 
  。对于 DHCPv6， 
  当 TCP 堆栈即将发送 Solicitation 或 Request 消息时，该参数可以为 eDHCPPhasePreRequest 或 eDHCPPhasePreDiscover 
  。

+ *pxEndPoint*

    端点当前执行 DHCP（v4 或 v6）。

+ *pxIPAddress*

  当参数 eDHCPPhase 为 eDHCPPhasePreDiscover 时，此参数将包含默认 IP 地址， 
  否则（当 eDHCPPhase 为 eDHCPPhasePreRequest 时），此参数将包含由 DHCP 服务器提供的 IP 地址。


**返回值：**

返回值可为以下枚举值之一：

+ 如果应用程序想要继续 DHCP 事务，返回 `eDHCPContinue`。
+ 如果应用程序想要使用默认网络参数，返回 `eDHCPUseDefaults`。
+ 在必须中止 DHCP 进程且所有网络参数保持不变的情况下，返回 `eDHCPStopNoChanges` 
  。

