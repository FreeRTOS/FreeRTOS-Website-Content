---
title: "ff_fprintf()"
description: FreeRTOS+FAT ff_fprintf API 文档
---
[[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)]

ff_stdio.h
```c
size_t ff_fprintf( FF_FILE * pxStream, const char *pcFormat, ... );	
```
将格式化数据写入文件，
 方式与 sprintf() 将格式化数据写入缓冲区或 printf() 将格式化数据写入控制台完全相同。

ff_fprintf() 会调用 vsnprintf() 函数，您的 C 库必须能够提供该函数的实现，
 否则使用 ff_fprintf() 的项目无法正常运行。可以使用的格式说明符和
 扩展（例如 "%02D"、"%s" 等）
 将取决于您的 C 库。

必须在 FreeRTOSFATConfig.h 中将 FF_FPRINTF_SUPPORT 设置为 1 才能使用 ff_fprintf()
 。

**注意：**ff_fprintf() 函数比较耗时，因为它在将格式化数据输出到文件之前，
 会分配内存来写入这些数据
 ，还会使用 vsnprintf()，可能会导致
 项目中包含大量额外的库代码。

## 参数 
+ *pxStream*

  指向要写入格式化数据的文件的指针。这是
  通过调用 ff_fopen() 打开文件时 
  返回的指针。

+ *pcFormat*

  格式字符串，其使用方式
  与 printf() 调用中的格式字符串输入完全相同。可以使用的格式说明符
  取决于所使用的 C 库。

+ *...*

  实参值的可变列表，每个值对应格式字符串中的
  一个说明符。

## 返回
如果 ff_printf() 无法分配缓冲区，则返回 0。

如果成功将数据写入文件，则返回写入的
 字节数。 

如果写入文件时发生错误，则返回 -1，并设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，
 以指示原因。任务可以使用 
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数获取其 errno 值。

## 用法示例 
[ff_fgets()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fgets) 文档页面中提供的示例
 显示了 ff_fprintf() 的使用方式。
