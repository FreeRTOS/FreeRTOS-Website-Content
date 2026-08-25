---
title: xApplicationGetRandomNumber()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h
  
```c
BaseType_t xApplicationGetRandomNumber( uint32_t * pulNumber );
```

xApplicationGetRandomNumber 是应用程序定义的钩子（或回调）函数， 
由 FreeRTOS-Plus-TCP 堆栈调用，以获取随机数。应用程序应尽量提供真随机数 
。如果可能，应使用硬件随机数生成器。所提供的随机数的质量 
对通信安全有极大影响。

回调函数由应用程序写入程序实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上面的原型完全匹配（包括函数名称）。应用程序 
钩子中的代码不应调用阻塞的 FreeRTOS-Plus-TCP API。这样很容易导致 
死锁。

当应用程序钩子执行时，会借用任务优先级和 IP 任务堆栈。因此， 
我们建议您保持应用程序钩子的简短性——它可能需要唤醒一些负责执行进一步处理的应用程序任务 
。


**参数：**

+ *pulNumber*
  
  如果成功生成随机数，则该指针将填入生成的 32 位 
  随机数。
  

**返回值：** 

如果成功生成随机数，则应返回 pdTRUE， 
并应复制 pulNumber 参数中的随机数。否则应返回 pdFALSE。

