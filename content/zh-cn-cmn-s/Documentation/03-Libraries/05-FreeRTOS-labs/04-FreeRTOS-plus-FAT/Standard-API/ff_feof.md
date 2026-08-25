---
title: "ff_feof()"
description: FreeRTOS+FAT ff_feof API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_feof( FF_FILE *pxStream );
```
查询嵌入式 FAT 文件系统中打开文件的
 读/写指针是否位于文件末尾。

## 参数 
+ *pxStream*

  正在查询的文件。必须先调用
   [ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen) 以打开文件。

## 返回

如果文件的读/写指针位于文件末尾，
 则返回非零值。

如果文件的读/写指针不在文件末尾，并且没有
 发生错误，则返回 0，并且任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 也设置为
 0。

如果由于某种错误导致函数无法确定
 文件的读/写指针位置，则返回 0，并设置任务的 errno，
 以指示原因。

任务可以使用 [stdioGET_ERRNO](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数
 获取其 errno 值。

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
        if( ff_feof( pxFile ) != 0 )
        {
            /* The end of the file has been reached, there are no more bytes to
               read. */
            break;
        }
        else
        {
            iReturnedByte = ff_fgetc( pxFile );
        }

        /* Write the byte into the buffer. */
        pcBuffer[ lBytesRead ] = ( char ) iReturnedByte;
    }

    /* Finished with the file. */
    ff_fclose( pxFile );
}
```
ff_feof() API 函数的用法示例
