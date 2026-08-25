---
title: xApplicationDHCPHook()
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
eDHCPCallbackAnswer_t xApplicationDHCPHook( eDHCPCallbackPhase_t eDHCPPhase,uint32_t ulIPAddress );
```

xApplicationDHCPHook 是一个应用程序定义的钩子（或回调）函数， 
由 FreeRTOS-Plus-TCP 堆栈调用，用于检查是否应发送 DHCP “发现”和“请求”消息， 
以完成获取动态 IP 地址的过程，或检查设备是否使用默认的静态 IP。

回调函数由应用程序写入程序实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上面的原型完全匹配（包括函数名称）。应用程序 
钩子中的代码不应调用阻塞的 FreeRTOS-Plus-TCP API。这样很容易导致 
死锁。

当应用程序钩子执行时，会借用任务优先级和 IP 任务堆栈。因此， 
我们建议您保持应用程序钩子的简短性——它可能需要唤醒一些负责执行进一步处理的应用程序任务 
。


**参数：**

+ *eDHCPPhase*
  
  当 TCP 堆栈将分别发送一条“请求”或“发现”消息时，此参数可以为 eDHCPPhasePreRequest 或 eDHCPPhasePreDiscover 
  。
  
+ *ulIPAddress*
  
  当参数 eDHCPPhase 为 eDHCPPhasePreDiscover 时，此参数将包含默认 IP 地址， 
  否则（当 eDHCPPhase 为 eDHCPPhasePreRequest 时），此参数将包含由 DHCP 服务器提供的 IP 地址 
  。


**返回值：** 

返回值可为以下枚举值： 

* 如果应用程序想要继续 DHCP 事务，返回 `eDHCPContinue`。
* 如果应用程序想要使用默认网络参数，返回 `eDHCPUseDefaults`。
* 在必须中止 DHCP 进程且所有网络参数保持不变的情况下，返回 `eDHCPStopNoChanges`
  。

