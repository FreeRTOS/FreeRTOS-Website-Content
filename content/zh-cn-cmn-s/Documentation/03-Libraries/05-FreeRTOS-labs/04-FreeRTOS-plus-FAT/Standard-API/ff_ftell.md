---
title: "ff_ftell()"
description: FreeRTOS+FAT ff_ftell API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
long ff_ftell( FF_FILE *pxStream );	
```
返回嵌入式 FAT 文件系统中已打开文件的 
 当前读/写位置。

返回的位置以字节为单位，从文件开头算起。

## 参数 
+ *pxStream*

  正在查询的文件。必须先调用
  [ff_fopen()](ff_fopen) 以打开文件。

## 返回

如果 pxStream 不为 NULL，则返回文件的当前读/写位置
 。返回值为 
 文件读/写位置从文件开头算起的字节数。

如果 pxStream 为 NULL，则返回 -1。

## 用法示例
```c
void vSampleFunction( char *pcFileName, char *pcBuffer )
{
FF_FILE *pxFile;
long lPosition;

    /* Open the file specified by the pcFileName parameter. */
    pxFile = ff_fopen( pcFileName, "r" );

    /* Expect the file position to be 0. */
    lPosition = ff_ftell( pxFile );
    configASSERT( lPosition == 0 );

    /* Read one byte. */
    ff_fread( pcBuffer, 1, 1, pxFile );

    /* Expect the file position to be 1. */
    lPosition = ff_ftell( pxFile );
    configASSERT( lPosition == 1 );

    /* Read another byte. */
    ff_fread( pcBuffer, 1, 1, pxFile );

    /* Expect the file position to be 2. */
    lPosition = ff_ftell( pxFile );
    configASSERT( lPosition == 2 );

    /* Close the file again. */
    ff_fclose( pxFile );
}
```
*ff_ftell() API 函数用法示例*
