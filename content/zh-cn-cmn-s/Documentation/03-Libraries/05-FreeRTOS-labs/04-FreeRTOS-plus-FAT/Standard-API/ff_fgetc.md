---
title: "ff_fgetc()"
description: FreeRTOS+FAT ff_fgetc API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_fgetc( FF_FILE * pxStream );	
```
从嵌入的 FAT 文件系统的打开文件中读取单个字节。
 增加了一个读/写位置。

在 int 中返回字符可能不是最佳方式，但 ff_fgetc()
 原型符合标准和预期的 stdio fgetc() 函数原型。


## 参数 
+ *pxStream*

  指向正在读取数据的文件的指针。这与
   调用 ff_fopen() 函数后返回的指针相同。此函数用于最初
   打开文件。

## 返回
如果成功，将返回从文件系统读取的字节。如果无法从文件读取
 一个字节，因为读取位置已位于
 文件末尾，则返回 FF_EOF。

## 用法示例 
```c
void vSampleFunction( char *pcFileName, char *pcBuffer, int32_t lBufferSize )
{
    FF_FILE *pxFile;
    int32_t lBytesRead;
    int iReturnedByte;

    /* Open the file specified by the pcFileName parameter. */
    pxFile = ff_fopen( pcFileName, "r" );

    /* Read the number of bytes specified by the lBufferSize parameter. */
    for( lBytesRead = 0; lBytesRead < lBufferSize; lBytesRead++ )
    {
        iReturnedByte = ff_fgetc( pxFile );

        if( iReturnedByte == FF_EOF )
        {
            /* A byte could not be read because the end of the file has
               been reached. */
            break;
        }
        else
        {
            /* Write the byte into the buffer. */
            pcBuffer[ lBytesRead ] = ( char ) iReturnedByte;
        }
    }

    /* Finished with the file. */
    ff_fclose( pxFile );
}
```
*ff_fgetc() API 函数用法示例*
