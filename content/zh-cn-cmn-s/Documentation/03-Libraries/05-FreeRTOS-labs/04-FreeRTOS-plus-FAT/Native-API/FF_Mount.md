---
title: "FF_Mount()"
description: FreeRTOS+FAT FF_Mount API 文档
---
[FreeRTOS-Plus-FAT 原生 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)


ff_ioman.h
```c
FF_Error_t FF_Mount( FF_Disk_t *pxDisk, BaseType_t xPartitionNumber );

```

媒体是用于存储文件的物理设备。适用于
 嵌入式文件系统的媒体包括 SD 卡、
 固态磁盘、NOR 闪存芯片、NAND 闪存芯片和 RAM
 芯片。

将媒体划分为多个单元，每个单元
 称为一个分区。分区必须经过格式化之后才能用于存放 FreeRTOS-Plus-FAT
 文件系统。

格式化分区必须 
 先[挂载](http://en.wikipedia.org/wiki/Mount_%28computing%29)，
 方可通过 FreeRTOS-Plus-FAT [标准 API](FF_Format) 使用。

## 参数 

+ *pxDisk* 

  存放要挂载的格式化分区的 FF_Disk_t 结构体。

+ *xPartitionNumber* 

  媒体上要挂载的分区的编号，从 0 开始。


## 返回

如果分区已成功挂载，则返回 FF_ERR_NONE。

如果无法挂载分区，则返回错误代码。

FF_GetErrMessage() 可将错误代码转换为错误描述。

## 用法示例 

此[页面不仅记录了如何创建 FreeRTOS-Plus-FAT 媒体驱动程序](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/File_System_Media_Driver/Media_Driver_Initialisation)，
还演示了如何使用 FF_Mount() 函数。
