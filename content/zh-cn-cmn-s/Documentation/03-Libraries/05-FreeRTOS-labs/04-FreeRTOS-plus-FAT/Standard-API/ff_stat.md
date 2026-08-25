---
title: "ff_stat()"
description: FreeRTOS+FAT ff_stat API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_stat( const char *pcFileName, FF_Stat_t *pxStatBuffer );
```
使用文件的相关信息填充 FF_Stat_t。FF_Stat_t 包含以下字段：

+ st_dev 

  包含该文件的设备的 ID。

+ st_ino

  文件序列号。

+ st_mode

   如果文件为目录，st_mode 将设置为 FF_IFDIR，如果是常规文件，st_mode 将设置为 FF_IFREG。

+ st_nlink 

  指向该文件的硬链接数量。对于大多数文件系统，通常为 1。

+ st_uid

  拥有该文件的用户的 ID

+ st_gid

  拥有该文件的群组的 ID

+ st_rdev

   设备 ID

+ st_size

   文件的大小（以字节为单位）。ff_stat() 无法用于获取已打开文件的大小。

+ st_atime 

  上次访问文件的时间。仅当在 FreeRTOSFATConfig.h 中将 FF_TIME_SUPPORT 设置为 1 时才可用。

+ st_mtime 

  上次修改文件的时间。仅当在 FreeRTOSFATConfig.h 中将 FF_TIME_SUPPORT 设置为 1 时才可用。

+ st_ctime 

  上次更改文件状态的时间。仅当在 FreeRTOSFATConfig.h 中将 FF_TIME_SUPPORT 设置为 1 时才可用。

## 参数

+ *pcFileName*

  指向以 null 结尾的标准 C 字符串的指针，该字符串包含要在其中检索 stat 信息的文件的名称 
  。文件名称可以包含指向该目录的相对路径。

+ *pxStatBuffer*

  指向 FF_Stat_t 的指针，以文件相关信息填充。


## 返回

+ 如果 stat 结构体中填充了文件的相关信息，则返回 0。

+ 如果 stat 结构体无法填充文件信息，则返回 -1，并设置任务的 
  [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务可以使用 
  [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数获取其 errno 值。


## 用法示例

```c
long lGetFileLength( char *pcFileName )  
{  
    FF_Stat_t xStat;  
    long lReturn;  
  
    /* Find the length of the file with name pcFileName. */  
    if( ff_stat( pcFileName, &xStat ) == 0 )  
    {  
        lReturn = xStat.st_size;  
    }  
    else  
    {  
        /* Could not obtain the length of the file. */  
        lReturn = -1;  
    }
    return lReturn;  
}
```
*ff_stat() API 函数用法示例*
