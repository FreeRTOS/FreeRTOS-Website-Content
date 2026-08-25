---
title: "ff_fclose()"
description: FreeRTOS+FAT ff_fclose API 文档
---
[[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)]

ff_stdio.h
```c
int ff_fclose( FF_FILE *pxStream );;
```
刷新后关闭嵌入式 FAT 文件系统中的文件。 
 此文件必须已先用 [ff_fopen()](ff_fopen) 打开过。

## 参数 
+ *pxStream*

  指向待关闭文件的指针。这将是文件最初打开时
   ff_fopen() 返回的相同指针。

## 返回
如果文件关闭成功，则返回 0。

如果无法关闭文件，则返回 -1 ，并且设置任务的
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 以指示原因。任务 可使用
 [stdioGET_ERRNO](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API 函数获取其 errno 值。

## 用法示例 
[ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen)
 文档页面中提供的示例 显示了 ff_fclose() 的使用方式。
