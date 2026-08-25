---
title: xApplicationDNSQueryHook()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h
  
**注意**：仅当 `ipconfigUSE_NBNS` 或 `ipconfigUSE_LLMNR` 
在 FreeRTOSIPConfig.h 文件中设置为 1 时，才需要定义此钩子。
  
```c
BaseType_t xApplicationDNSQueryHook( const char * pcName );
```

xApplicationDNSQueryHook 是由应用程序定义的钩子（或回调）函数， 
FreeRTOS-Plus-TCP 堆栈会调用这个函数，以检查收到的 LLMNR 或 NBNS 名称 
是否与设备正在查找的名称相同。

回调函数由应用程序编写者实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上述原型（包括函数名称）完全匹配。应用程序钩子中的代码 
不应调用会导致阻塞的 FreeRTOS-Plus-TCP API。这很容易导致 
死锁。

应用程序钩子执行时，会借用 IP 任务的优先级和堆栈。因此， 
建议应用程序钩子尽量简短，只做一些简单的工作，例如唤醒其他应用程序任务，由这些任务进行进一步处理 
。


**参数：**

+ *pcName*

  由 TCP/IP 堆栈接收的名称。


**返回值：** 

如果 pcName 中的值与设备名称相匹配，则钩子应返回 pdTRUE； 
否则应返回 pdFALSE。

