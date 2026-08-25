---
title: pcApplicationHostnameHook()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h
  
**注意**：仅当 `ipconfigDHCP_REGISTER_HOSTNAME` 在 FreeRTOSIPConfig.h 文件中设置为 1 时才需要定义此钩子。
  
```c
const char * pcApplicationHostnameHook( void );
```
eApplicationHostnameHook 是由应用程序定义的钩子（或回调）函数， 
由 FreeRTOS-Plus-TCP 堆栈在向 DHCP 服务器发送 IP 地址请求时调用。它允许设备 
将其主机名注册到 DHCP 服务器。

回调函数由应用程序写入程序实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上面的原型完全匹配（包括函数名称）。应用程序 
钩子中的代码不应调用阻塞的 FreeRTOS-Plus-TCP API。这样很容易导致死锁 
。

当应用程序钩子执行时，会借用任务优先级和 IP 任务堆栈。因此， 
我们建议您保持应用程序钩子的简短性——它可能需要唤醒一些负责执行进一步处理的应用程序任务 
。


**返回值：** 

设备可以发送到 DHCP 服务器进行注册的以 NULL 结尾的主机名。主机名的最大长度 
可以是 32 个字符。

