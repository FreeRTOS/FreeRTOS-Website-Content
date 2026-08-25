---
title: "FF_FS_Add()"
description: FreeRTOS+FAT FF_FS_Add API 文档
---
[FreeRTOS-Plus-FAT 原生 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_sys.h
```c
BaseType_t FF_FS_Add( const char *pcPath, FF_Disk_t *pxDisk );
```

将挂载分区添加到 FreeRTOS-Plus-FAT 虚拟文件系统，
它将显示为文件系统根目录下的目录。


## 参数 

+ *pcPath* 

  虚拟文件系统中分区所使用的名称。例如，
  如果 pcPath 为 “/SDCard”，则分区将在文件系统的根目录中显示为 /SDCard 
  。

  pcPath 必须是以正斜杠 (/) 开头的绝对路径。

+ *pdDisk* 

  用于访问和管理被添加到文件系统的分区的 FF_Disk_t 结构体
   。


## 返回

如果分区已成功添加到 FreeRTOS-Plus-FAT 虚拟文件
系统，则返回 1，否则返回 0。

