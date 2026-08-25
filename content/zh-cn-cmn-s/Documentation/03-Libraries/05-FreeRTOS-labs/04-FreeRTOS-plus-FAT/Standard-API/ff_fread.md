---
title: "ff_fread()"
description: FreeRTOS+FAT ff_fread API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)


ff_stdio.h
```c
size_t ff_fread( void *pvBuffer, size_t xSize, size_t xItems, FF_FILE * pxStream );	
```

从嵌入式 FAT 文件系统中的打开文件的
 当前读取/写入位置读取数据。读取/写入位置按读取的
 字节数递增。


## 参数 

+ *pvBuffer* 
  
  指向放置从文件所读取数据的缓冲区的指针。
   缓冲区必须至少大到足以容纳正在读取的字节数
   。

+ *xSize* 
  
  从文件读取的每个项目的大小（以字节为单位）。

+ *xItems* 

  要从文件读取的项目数。每个项目的大小由
  xSize 参数设置。

+ *pxStream*

  指向正在读取数据的文件的指针。这与
   调用 ff_fopen() 函数后返回的指针相同。此函数用于最初 
   打开文件。

## 返回

返回实际从文件读取的
 项目数。从文件读取的项目数只能等于
 当项目大小为 1 时从文件读取的项目数。
 每个项目的大小由 xSize 参数设置。


如果从文件读取的项目数小于 xItems 值，
 则设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值以指示原因。任务
 可以使用 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API 函数获取其 errno 值。

## 用法示例 

[ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen) 文档页面中提供的示例
显示了 ff_fread() 的使用方式。
