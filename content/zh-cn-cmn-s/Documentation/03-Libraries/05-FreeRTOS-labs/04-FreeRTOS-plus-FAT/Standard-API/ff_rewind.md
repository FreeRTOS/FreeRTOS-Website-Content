---
title: "ff_rewind()"
description: FreeRTOS+FAT ff_rewind API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
void ff_rewind( FF_FILE *pxStream );
```
将当前读/写位置移回文件的开头。
 调用 ```ff_rewind( pxStream )``` 等同于调用 
 ```ff_fseek( pxStream, 0, FF_SEEK_SET )```。

## 参数 
+ *pxStream*

  要将当前读/写位置重置到
  文件开头的文件。

## 用法示例 
```c
void vSampleFunction( void )
{
    char pcBuffer1[ 4 ], pcBuffer2[ 4 ];
    FF_FILE *pxFile;

    /* Open the file "afile.bin". */
    pxFile = ff_fopen( "afile.bin", "r" );

    if( pxFile != NULL )
    {
        /* Read four bytes into pcBuffer1. */
        ff_fread( pcBuffer1, 4, 1, pxFile );

        /* Set the current read pointer back to the start of the file. */
        ff_rewind( pxFile );

        /* Read the same four bytes into pcBuffer2. */
        ff_fread( pcBuffer2, 4, 1, pxFile );

        /* Finished with the file. */
        ff_fclose( pxFile );
    }
}
```
*ff_rewind() API 函数用法示例*
