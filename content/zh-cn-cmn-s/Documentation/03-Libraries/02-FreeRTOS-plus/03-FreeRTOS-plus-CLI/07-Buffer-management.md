---
title: FreeRTOS_CLIGetOutputBuffer()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS_CLI.h
   
```c
char *FreeRTOS_CLIGetOutputBuffer( void );
```

FreeRTOS-Plus-CLI 是一个可扩展的框架， 
应用程序写入器可以通过该框架定义并注册自己的命令行输入命令。提供了单独的文档页面，描述了 
[如何编写实现用户定义命令行为的函数](FreeRTOS_Plus_CLI_Implementing_A_Command) 
， 
[如何使用 FreeRTOS-Plus-CLI](FreeRTOS_Plus_CLI_Registering_A_Command) 注册用户定义的命令，
以及如何将 FreeRTOS-Plus-CLI 集成到 FreeRTOS 任务中。

此页面介绍了可选的 FreeRTOS_CLIGetOutputBuffer() 函数。

命令解释器的实现需要一个输出缓冲区， 
用于保存运行命令时产生的任何输出。 

如果使用 FreeRTOS-Plus-CLI 实现单一命令解释器接口， 
输出缓冲区可在
执行 [FreeRTOS_CLIProcessCommand()](FreeRTOS_Plus_CLI_Calling_The_Interpreter) API 函数的任务或文件本地定义。

如果使用 FreeRTOS-Plus-CLI 在多个接口 
（例如 UART 和 TCP/IP 套接字）上执行命令解释器，那么这两个接口都能以相同方式提供各自的输出缓冲区。
但是，如果每次只使用其中一个接口，则可以通过让两个接口共用一个输出缓冲区来节省 RAM。 
FreeRTOS_CLIGetOutputBuffer() 可以简化这一过程 
。


**参数：** 

 无。


**返回：** 

FreeRTOS_CLIGetOutputBuffer() 只需返回 
在 FreeRTOS-Plus-CLI 代码中声明的输出缓冲区的地址， 
而无需命令接口实现声明自己的输出缓冲区。

缓冲区的大小由 configCOMMAND_INT_MAX_OUTPUT_SIZE 常量定义， 
使用 FreeRTOS-Plus-CLI 时应在 FreeRTOSConfig.h 中定义该常量。

configCOMMAND_INT_MAX_OUTPUT_SIZE 应设置为 1，以便在以下情况下，尽量减少 RAM 的使用： 
所有命令解释器接口都使用自己本地定义的缓冲区，且不使用 FreeRTOS_CLIGetOutputBuffer() API 函数 
。

