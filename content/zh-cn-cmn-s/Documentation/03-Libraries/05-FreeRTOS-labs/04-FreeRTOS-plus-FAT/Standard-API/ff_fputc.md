---
title: "ff_fputc()"
description: FreeRTOS+FAT ff_fputc API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_fputc( int iChar, FF_FILE * pxStream );	
```
在嵌入式 FAT 文件系统已打开的文件中写入单个字节。

读/写位置增加 1。

将字符作为整型参数传递可能不是最佳方式，但 ff_fputc() 的
 原型符合标准库 stdio 中 fputc() 函数的 
 预期原型。

## 参数 

+ *iChar*
  
  写入文件的值。该值在写入前会被转换为无符号字符 
   （8 位）。

+ *pxStream* 
  
  指向要写入字符的文件的指针。这是
   通过调用 ff_fopen() 打开文件时返回的指针 
   。

## 返回

如果成功，则返回写入文件的字节。如果失败，则返回
 其他值（不是写入文件的字节数），并设置任务的
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务
 可以使用 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数
 获取其 errno 值。

## 用法示例 

```c
void vSampleFunction( char *pcFileName, int32_t lNumberToWrite )
{
    FF_FILE *pxFile;
    const int iCharToWrite = 'A';
    int iCharWritten;
    int32_t lBytesWritten;

    /* Open the file specified by the pcFileName parameter for writing. */
    pxFile = ff_fopen( pcFileName, "w" );

    /* Write 'A' to the file the number of times specified by the
       lNumberToWrite parameter. */
    for( lBytesWritten = 0; lBytesWritten < lNumberToWrite; lBytesWritten++ )
    {
        /* Write the byte. */
        iCharWritten = ff_fputc( iCharToWrite, pxFile );

        /* Was the character written to the file successfully? */
        if( iCharWritten != iCharToWrite )
        {
            /* The byte could not be written to the file. */
            break;
        }
    }

    /* Finished with the file. */
    ff_fclose( pxFile );
}
```
*ff_fputc() API 函数用法示例*
