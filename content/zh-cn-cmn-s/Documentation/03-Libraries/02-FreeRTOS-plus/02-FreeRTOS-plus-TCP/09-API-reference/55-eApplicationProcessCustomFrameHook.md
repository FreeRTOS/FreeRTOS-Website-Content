---
title: eApplicationProcessCustomFrameHook()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---



[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]


FreeRTOS_sockets.h
  
**注意**：仅当 `ipconfigPROCESS_CUSTOM_ETHERNET_FRAMES` 
在 FreeRTOSIPConfig.h 文件中设置为 1 时，才需要定义此钩子。
  

```c
eFrameProcessingResult_t eApplicationProcessCustomFrameHook( NetworkBufferDescriptor_t * const pxNetworkBuffer );
```

eApplicationProcessCustomFrameHook 是由应用程序定义的钩子（或*回调*）函数， 
FreeRTOS-Plus-TCP 堆栈在收到未处理的帧 
（ARP 帧或 IP 数据包除外）时会调用该函数。 

回调函数由应用程序编写者实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上述原型（包括函数名称）完全匹配。应用程序钩子中的代码 
不应调用会导致阻塞的 FreeRTOS-Plus-TCP API。这很容易导致 
死锁。

应用程序钩子执行时，会借用 IP 任务的优先级和堆栈。因此， 
建议应用程序钩子尽量简短，只做一些简单的工作，例如唤醒其他应用程序任务，由这些任务进行进一步处理 
。


**参数：** 

+ *pxNetworkBuffer*

  包含不受支持的帧的网络缓冲区。


**返回值：** 

返回值必须为 `eFrameProcessingResult_t` 类型。如果要释放帧，则应返回 
eReleaseBuffer，网络堆栈将负责清理。如果返回其他值， 
则用户/应用程序必须通过 
调用 [vReleaseNetworkBufferAndDescriptor()](vReleaseNetworkBufferAndDescriptor) 来释放网络缓冲区。

