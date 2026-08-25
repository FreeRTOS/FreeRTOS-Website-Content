---
title: "ff_rmdir()"
description: FreeRTOS+FAT ff_rmdir API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_rmdir( const char *pcPath );
```

从嵌入式 FAT 文件系统中删除一个目录。仅当目录
 不包含任何文件时才可以被删除。

## 参数
+ *pcDirectory*

  指向以 null 结尾的标准 C 字符串的指针，该字符串保存
  正在删除的目录的名称。该字符串可包含相对路径。

## 返回

如果目录已成功删除，则返回 0。

如果无法删除目录，则返回 -1，并
 设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务可以使用
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数获取其 errno 值。

## 用法示例

```c
void vExampleFunction( void )  
{  
    /* Create a sub directory called subfolder, and sub directory within  
       subfolder called sub1. */  
    ff_mkdir( "subfolder" );  
    ff_mkdir( "subfolder/sub1" );
    /* The directories can be accessed here. */
    /* Delete the two sub directories again. */  
    ff_rmdir( "subfolder/sub1" );  
    ff_rmdir( "subfolder" );  
}  
```
*通过 ff_rmdir() API 函数删除目录的用法示例*
