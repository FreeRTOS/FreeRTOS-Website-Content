---
title: vApplicationPingReplyHook()
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
void vApplicationPingReplyHook( ePingReplyStatus_t eStatus, uint16_t usIdentifier );
```

vApplicationPingReplyHook() 是由应用程序定义的钩子（或*回调*）函数， 
TCP/IP 堆栈会在收到使用
[FreeRTOS_SendPingRequest()](FreeRTOS_SendPingRequest) 函数生成的 ICMP 回显 (ping) 请求的回复时调用该函数。

回调函数由应用程序编写者实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上述原型（包括函数名称）完全匹配。


**参数：** 

+ *eStatus* 
  
  eStatus（由 TCP/IP 堆栈）设置为以下任意一值：

  + eSuccess
   
    正确收到回显回复。
  
  + eInvalidChecksum
   
    回显回复中收到的数据与回显请求中发送的数据匹配，但回复的 
    校验和不正确。
  
  + eInvalidData
   
    回显回复中收到的数据与回显请求中发送的数据不匹配。
  
+ *usIdentifier* 
  
  回显回复中收到的标识符。

  每个回显请求都有一个唯一标识符，以确保回复与请求匹配。 
  FreeRTOS_SendPingRequest() 函数会返回其生成的传出回显请求的标识符。


**用法示例：** 

请参阅 [FreeRTOS_SendPingRequest()](FreeRTOS_SendPingRequest) 文档页面，其中包括 
vApplicationPingReplyHook() 的示例实现。

