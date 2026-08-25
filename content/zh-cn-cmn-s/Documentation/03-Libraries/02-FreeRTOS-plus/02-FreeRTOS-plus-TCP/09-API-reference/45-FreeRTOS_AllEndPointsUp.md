---
title: "FreeRTOS_AllEndPointsUp()"
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
BaseType_t FreeRTOS_AllEndPointsUp( const struct xNetworkInterface * pxInterface )
```

用于测试与接口关联的所有端点当前是处于开启状态（连接）还是关闭状态（断开连接）。 
请注意，断开事件由网络接口驱动器引起，因此其实现取决于网络接口驱动器 
。


**参数：**

+ *pxInterface* 

  必须检查其端点状态的接口。如果为 NULL，则该函数返回所有可用端点， 
  无论其所属接口是否已启动。


**返回：**

如果所有端点均已启动（已连接），则返回 pdTRUE，否则返回 pdFALSE。

