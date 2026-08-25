---
title: "ff_fwrite()"
description: FreeRTOS+FAT ff_fwrite API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
size_t ff_fwrite( const void *pvBuffer, size_t xSize, size_t xItems, FF_FILE * pxStream );
```
将数据写入嵌入式 FAT 文件系统中打开文件的
 当前读取/写入位置。读取/写入位置按写入字节数
 递增。


## 参数 
+ *pvBuffer*

  指向要写入文件的数据源的指针。

+ *xSize*

  正在写入文件的每个项目的大小（以字节为单位）。

+ *xItems*

  待写入文件的项目数。每个项目的大小由
   xSize 参数设置。

+ *pxStream*

  指向正在写入数据的文件的指针。这与
  调用 ff_fopen() 函数后返回的指针相同。此函数用于最初
  打开文件。

## 返回

 返回实际写入文件的项目数。写入文件的
 项目数将只会等于项目大小为 1 时写入文件的字节数。
 每个项目的大小由 xSize 参数设置 
 。

 如果写入文件的项目数小于 xItems 值，
 则设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值以指示原因。任务
 可以使用 [stdioGET_ERRNO()()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API 函数获取其 errno 值。


## 用法示例

[ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen) 文档页面中提供的示例
显示了 ff_fwrite() 的使用方式。
