---
title: "ff_filelength()"
description: FreeRTOS+FAT ff_filelength API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
size_t ff_filelength( FF_FILE *pxStream );
```
返回已打开以供读取的文件的长度（以字节为单位）。

## 参数 
 - *pxStream*

  指向正在查询的文件的指针。这将是文件最初打开时
   ff_fopen() 返回的相同指针。

## 返回
如果成功获取文件的长度，则返回文件的
 长度。

如果无法获取文件的长度，则返回 0，并且设置任务的
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 以指示原因。只有当
 文件打开以供读取且文件长度适合 type size_t 的变量时，
 才能获取文件的长度。
