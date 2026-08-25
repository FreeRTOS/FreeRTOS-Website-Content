---
title: "ff_remove()"
description: FreeRTOS+FAT ff_remove API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_remove( const char *pcPath );
```
从嵌入式 FAT 文件系统中移除、删除文件或取消该文件链接。如果文件已打开，
 则无法移除。

## 参数
+ *pcDirectory*

  指向以 null 结尾的标准 C 字符串的指针，该字符串包含
  要移除文件的名称。文件名称可以包含指向该目录的 
  相对路径。

## 返回
如果文件移除成功，则返回零。

如果无法移除文件，则返回 NULL ，
 并设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务
 可以使用 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API 函数获取其 errno 值。如果文件已打开，则无法移除。

## 用法示例

```c
void vExampleFunction( void )
{
    /* Delete a file. */
    ff_remove( "/ram1/filename.txt" );
}
```
*通过 ff_remove() API 函数删除文件的用法示例*
