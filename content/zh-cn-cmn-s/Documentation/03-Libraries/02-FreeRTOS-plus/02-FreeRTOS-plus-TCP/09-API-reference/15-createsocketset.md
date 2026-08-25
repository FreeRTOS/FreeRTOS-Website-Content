---
title: FreeRTOS_CreateSocketSet()
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
SocketSet_t FreeRTOS_CreateSocketSet()( unsigned BaseType_t uxEventQueueLength );
```

创建用于 [FreeRTOS_select()](select) 函数的套接字集。ipconfigSUPPORT_SELECT_FUNCTION 
必须在 [FreeRTOSIPConfig.h](../TCP_IP_Configuration#ipconfigSUPPORT_SELECT_FUNCTION) 中设置为 1，
才能使用 FreeRTOS_CreateSocketSet()。

*套接字集*允许应用程序 RTOS 任务在多个套接字上同时进入阻塞状态。

要使用套接字集，请执行下列操作：

1. 调用 FreeRTOS_CreateSocketSet() 创建套接字集。

   套接字集相当于 Berkeley 套接字 fd_set 类型。

2. 调用 [FreeRTOS_FD_SET()](FD_SET) 向套接字集添加一个或多个套接字。

   FreeRTOS_FD_SET() 相当于 Berkeley 套接字 FD_SET() 宏。

3. 调用 [FreeRTOS_Select()](select) 以测试套接字集中的套接字，检查其中是否包含任何 
   挂起的事件。

4. 如果 FreeRTOS_select() 返回非零值，则调用  
   [FreeRTOS_FD_ISSET()](FD_ISSET) 检查套接字集中的所有套接字，以确定哪些事件处于挂起状态。

[FreeRTOS_FD_CLR()](FD_CLR) API 函数用于从套接字集中移除套接字。


**参数：** 


+ *uxEventQueueLength* 

  每次套接字集中的套接字接收数据时，都会生成一个接收事件。uxEventQueueLength 
  设置套接字每次可存储的最大接收事件数。  如果 
  如果作为套接字组一员的套接字接收到一个数据包，而套接字组的事件队列已满， 
  则该数据包将被丢弃。  


**返回：** 

如果创建了套接字集，则返回创建的套接字集的句柄。如果未创建套接字组 
（因为 [FreeRTOS 堆内存不足](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)）， 
则返回 NULL。


**用法示例：** 

请参阅 [FreeRTOS_select()](select) 文档页面上的示例。

