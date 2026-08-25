---
title: FreeRTOS_CLIProcessCommand()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS_CLI.h

```c
BaseType_t FreeRTOS_CLIProcessCommand( char *pcCommandInput, 
                                       char *pcWriteBuffer, 
                                       size_t xWriteBufferLen  );
```


FreeRTOS-Plus-CLI 是一个可扩展的框架， 
应用程序写入器可以通过该框架定义并注册自己的命令行输入命令。提供了单独的文档页面，描述了 
如何[编写实现用户定义命令行为的函数](FreeRTOS_Plus_CLI_Implementing_A_Command)， 
如何[使用 FreeRTOS-Plus-CLI](FreeRTOS_Plus_CLI_Registering_A_Command) 注册用户定义的命令，
以及如何[实现 FreeRTOS-Plus-CLI 任务](FreeRTOS_Plus_CLI_IO_Interfacing_and_Task)。

此页面描述了 FreeRTOS_CLIProcessCommand() 函数。FreeRTOS_CLIProcessCommand() 
是一个 API 函数，它接收用户在命令提示符下输入的字符串， 
如果该字符串与已注册的命令相匹配，则执行实现该命令行为的函数。


**参数：** 

+ *pcCommandInput*

  完整的输入字符串，与用户在命令提示符（可能是 
  UART 控制台、键盘、Telnet 客户端或其他用户输入客户端）中输入的字符串完全相同。

+ *pcWriteBuffer*

  如果 pcCommandInput 不包含格式正确的命令，那么 FreeRTOS_CLIProcessCommand() 
  将在 pcWriteBuffer 缓冲区中输出一条以 NULL 结尾的错误信息。如果 pcCommandInput 包含格式正确的命令， 
  那么 FreeRTOS_CLIProcessCommand() 将执行实现命令行为的函数， 
  并将其生成的输出放入 pcWriteBuffer 缓冲区。

+ *xWriteBufferLen*

  pcWriteBuffer参数所指向的缓冲区大小。向 pcWriteBuffer 写入超过 xWriteBufferLen 个字符 
  将导致缓冲区溢出。


**返回：** 

FreeRTOS_CLIProcessCommand() 执行一个实现命令行为的函数， 
并返回其执行的函数所返回的值。这些值在 
[“实现命令”](FreeRTOS_Plus_CLI_Implementing_A_Command)页面上有说明。


### 示例

[FreeRTOS-Plus-CLI Task Implementation](FreeRTOS_Plus_CLI_IO_Interfacing_and_Task) 页面包含 
示例代码，其中包含如何使用 FreeRTOS_CLIProcessCommand() 的演示。

