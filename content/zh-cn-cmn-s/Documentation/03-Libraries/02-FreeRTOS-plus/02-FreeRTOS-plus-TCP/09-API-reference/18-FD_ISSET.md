---
title: FreeRTOS_FD_ISSET()
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
BaseType_t FreeRTOS_FD_ISSET( Socket_t xSocket, SocketSet_t xSocketSet );
```

检查套接字集中的套接字是否有事件位集。pconfigSUPPORT_SELECT_FUNCTION  
必须在 [FreeRTOSIPConfig.h](../TCP_IP_Configuration#ipconfigSUPPORT_SELECT_FUNCTION) 中设为 1， 
FreeRTOS_FD_ISSET() 才可用。

*套接字集*允许应用程序 RTOS 任务在多个套接字上同时进入阻塞状态。

要使用套接字集，请执行下列操作：

1. 调用 [FreeRTOS_CreateSocketSet()](createsocketset) 创建套接字集。

   套接字集相当于 Berkeley 套接字 fd_set 类型。

2. 调用 [FreeRTOS_FD_SET()](FD_SET) 向套接字集添加一个或多个套接字。

   FreeRTOS_FD_SET() 相当于 Berkeley 套接字 FD_SET() 宏。

3. 调用 [FreeRTOS_Select()](select) 以测试套接字集中的套接字，检查其中是否包含任何 
   挂起的事件。

4. 如果 FreeRTOS_select() 返回非零值，则调用  
   FreeRTOS_FD_ISSET() 检查套接字集中的所有套接字，以确定哪些事件处于挂起状态。

相关事件位是以下一个或多个值的按位 OR 结合值：

+ eSELECT_READ

  对于正在读取数据的套接字，只要套接字中包含未读数据，eSELECT_READ 事件都将在套接字中处于挂起的状态 
  。  对于正在监听新连接的套接字， 
  每次接收到新连接时，eSELECT_READ 事件将被挂起。  

+ eSELECT_WRITE

  只要套接字有写入空间，eSELECT_WRITE 事件都将留在挂起状态中。  如果 TCP  
  套接字正主动连接到 pear，则在建立连接后， 
  会立即触发 eSELECT_WRITE 事件。  当 eSELECT_WRITE 事件被挂起后，就应将其禁用， 
  或者调用者应在套接字中写入足够的数据以填满传输缓冲区， 
  否则，挂起的 eSELECT_WRITE 事件将不会被清除。  

+ eSELECT_EXCEPT

  如果套接字断开连接，则 eSELECT_EXCEPT 事件会进入挂起状态。 

[FreeRTOS_FD_CLR()](FD_CLR) API 函数清除相关事件位并从套接字集中移除套接字 
。


**参数：** 

+ *xSocket*

  正在测试的套接字集中的套接字，以确定其中是否包含任何事件位集。  

+ *xSocketSet*

  正在向其中添加套接字的套接字集。  


**返回：** 

函数返回 eSELECT_READ (1)、eSELECT_WRITE (2) 和 eSELECT_EXCEPT (4) 等值的位掩码。 
只有通过调用 [FreeRTOS_FD_SET()](FD_SET) 指定的相关位才会被返回。


**用法示例：** 

请参阅 [FreeRTOS_select()](select) 文档页面上的示例。

