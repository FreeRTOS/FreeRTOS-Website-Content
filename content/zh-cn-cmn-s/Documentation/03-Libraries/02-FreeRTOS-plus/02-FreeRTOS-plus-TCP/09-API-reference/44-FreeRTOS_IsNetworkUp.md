---
title: FreeRTOS_IsNetworkUp()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_IP.h

```c
BaseType_t FreeRTOS_IsNetworkUp( void );
```

用于测试网络当前是接通（已连接）还是中断（已断开）。请注意， 
断开连接事件来自网络接口驱动程序，因此它们依赖网络接口驱动程序来实现。


**返回：** 

如果网络已接通（已连接），返回 pdTRUE。否则返回 pdFALSE。

