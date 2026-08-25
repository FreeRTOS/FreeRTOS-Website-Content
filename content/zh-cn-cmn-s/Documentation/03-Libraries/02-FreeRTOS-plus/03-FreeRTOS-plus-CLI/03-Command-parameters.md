---
title: FreeRTOS_CLIGetParameter()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS_CLI.h
   

```c
const char *FreeRTOS_CLIGetParameter( const char *pcCommandString, 
                                         UBaseType_t uxWantedParameter, 
                                         BaseType_t *pxParameterStringLength )		
```

FreeRTOS-Plus-CLI 是一个可扩展的框架， 
应用程序写入器可以通过该框架定义并注册自己的命令行输入命令。实现用户自定义命令行为的函数必须使用一个特定的接口， 
该接口将在[另一页面上](FreeRTOS_Plus_CLI_Implementing_A_Command)进行介绍。

有些命令需要参数。例如，文件系统 “copy” 命令需要 
带有源文件的名称和目标文件的名称。此页面描述了名为 `FreeRTOS_CLIGetParameter()` 的辅助函数， 
此函数由 FreeRTOS-Plus-CLI 提供，用于简化输入参数解析。

`FreeRTOS_CLIGetParameter()` 将完整的命令字符串和所请求参数的位置作为输入， 
并产生一个指向所请求参数起点的指针和 
以字节为单位的参数字符串长度作为输出。

**参数：** 

+ *pcCommandString*

   指向用户输入的整个命令字符串的指针。 

+ *ucWantedParameter*

  所请求的参数在命令字符串中的位置。例如，
  如果输入命令是 "copy [source\\_file] [destination\\_file]"，将 `ucWantedParameter` 设置为 1 
  可以请求 source_file 参数的名称和长度。将 `ucWantedParameter` 设置为 2 
  可以请求 destination_file 参数的名称和长度。 

+ *pucParameterStringLength*

  返回所请求参数的字符串长度（单位：`*pucParameterStringLength`）。例如， 
  如果参数文本是 "filename.txt"，则 `*pucParameterStringLength` 将被设置为 12， 
  因为该字符串中有 12 个字符。 


**返回：** 

指向返回所请求的参数开头的指针。例如，如果完整的命令字符串是 
 “copy file1.txt file2.txt”，且 `ucWantedParameter` 为 2，那么 `FreeRTOS_CLIGetParameter()` 
将返回指向 “file2.txt” 中的 “f” 的指针。


### 示例

有关示例，请参阅  
[实现命令](FreeRTOS_Plus_CLI_Implementing_A_Command#Example_Of_Using_FreeRTOS_CLIGetParameter) 
页面。

