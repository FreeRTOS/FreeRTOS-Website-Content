---
title: "FreeRTOS_IsEndPointUp()"
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
BaseType_t FreeRTOS_IsEndPointUp( const struct xNetworkEndPoint * pxEndPoint )
```

用于测试端点 (pxEndPoint) 当前是接通（已连接）还是中断（已断开）。请注意， 
断开事件由网络接口驱动器引起，因此其实现取决于网络接口驱动器 
。如果 pxEndPoint 为 NULL，则此函数将返回是否所有端点都已连接。


**参数：**

+ *pxEndPoint*

  如果为 NULL，则返回相关端点，并将检查所有端点的状态。


**返回：**

如果给定的端点接通（已连接），则返回 pdTRUE（如果 pxEndPoint 为 NULL，则返回所有端点）。否则返回 pdFALSE。

