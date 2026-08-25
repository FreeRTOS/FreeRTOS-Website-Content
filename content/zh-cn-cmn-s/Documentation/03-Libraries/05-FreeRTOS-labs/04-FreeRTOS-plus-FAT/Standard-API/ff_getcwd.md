---
title: "ff_getcwd()"
description: FreeRTOS+FAT ff_getcwd API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
char *ff_getcwd( char *pcBuffer, size_t xBufferLength );	
```
将当前工作目录 (CWD) 的名称写入 pcBuffer 指向的缓冲区
 。该名称写入形式为以 null 结尾的标准
 C 字符串。

## 参数 
+ *pcBuffer*

  指向缓冲区的指针，可向该缓冲区写入当前工作目录的名称。

+ *xBufferLength*

  pcBuffer 指向的缓冲区的大小（以字节为单位）。

## 返回

 如果当前工作目录名称成功写入 pcBuffer，
 则返回 pcBuffer，否则返回 NULL。

## 用法示例 
```c
void vExampleFunction( void )
{
    char pcBuffer[ 50 ];

    /* Create a sub directory called subfolder, and sub directory within
       subfolder called sub1. */
    ff_mkdir( "subfolder" );
    ff_mkdir( "subfolder/sub1" );

    /* Move into subfolder/sub1. */
    ff_chdir( "subfolder/sub1" );

    /* Print out the current working directory - it should be
       "subfolder/sub1". */
    ff_getcwd( pcBuffer, sizeof( pcBuffer ) );
    printf( "%s", pcBuffer );
}
```
*通过 ff_getcwd() API 函数打开或创建文件的用法示例*
