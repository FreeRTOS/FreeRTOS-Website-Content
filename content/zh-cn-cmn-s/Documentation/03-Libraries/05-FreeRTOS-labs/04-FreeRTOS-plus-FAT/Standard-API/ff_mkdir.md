---
title: "ff_mkdir()"
description: FreeRTOS+FAT ff_mkdir API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_mkdir( const char *pcDirectory );
```
在嵌入式 FAT 文件系统中新建目录。

## 参数 
+ *pcDirectory*
  指向以 null 结尾的标准 C 字符串的指针，该字符串包含
  要创建目录的名称，还可包含相对路径。

## 返回
如果创建目录成功，则返回零。

如果无法创建目录，则返回 -1，并设置任务的
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务可以 
 使用 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数获取其 errno 值。

## 用法示例 
```c
void vExampleFunction( void )
{
    /* Create a sub directory called subfolder. */
    ff_mkdir( "subfolder" );

    /* Create three subdirectories called sub1, sub2 and sub three respectively
       inside the subfolder directory. */
    ff_mkdir( "subfolder/sub1" );
    ff_mkdir( "subfolder/sub2" );
    ff_mkdir( "subfolder/sub3" );

    /* Move into the subfolder/sub1 directory. */
    ff_chdir( "subfolder/sub1" );

    /* Create another directory called sub4 inside the subfolder/sub1 directory. */
    ff_mkdir( "sub4" );
}
```
*通过 ff_mkdir() API 函数创建目录的用法示例*
