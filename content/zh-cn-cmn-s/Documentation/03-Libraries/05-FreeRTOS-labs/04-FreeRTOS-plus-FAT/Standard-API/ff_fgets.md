---
title: "ff_fgets()"
description: FreeRTOS+FAT ff_fgets API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
char *ff_fgets( char *pcBuffer, size_t xCount, FF_FILE *pxStream );	
```
从文件中读取字符串的步骤为：将字节从 pxStream 读入 pcBuffer，直至读取了 (xCount - 1) 个字节，
 或遇到换行符 ('n')。

回车符 ('r') 不会被特殊处理，
 而是直接复制到 pcBuffer 中。

在 ff_fgets() 返回之前，复制到 pcBuffer 中的字符串以 NULL 结尾。

## 参数 
+ *pcBuffer*

  指向用于存放从文件中读取的字符的缓冲区的指针 
   。缓冲区的大小至少要能够容纳 xCount 个字节。

+ *xCount*

  从文件中读取的字节数，直到收到
   换行符或读取了 (xCount - 1) 个字节。

+ *pxStream*

  指向正在读取数据的文件的指针。这是
   从最初调用 ff_fopen() 打开文件时返回的 
   指针。

## 返回
如果成功，返回指向 pcBuffer 的指针。如果读取出错，
 则返回 NULL，并设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。

任务可以使用 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API 函数获取其 errno 值。

## 用法示例 
```c
static void prvTest_ff_fgets_ff_printf( const char *pcMountPath )
{
    FF_FILE *pxFile;
    int iString;
    const int iMaxStrings = 1000;
    char pcReadString[ 20 ], pcExpectedString[ 20 ], *pcReturned;
    const char *pcMaximumStringLength = "Test string 999n";

    /* Open a file for reading and writing. */
    pxFile = ff_fopen( "/nand/myfile.txt", "w+" );

    /* Use ff_fprintf() to write some strings to the file. The strings are
       generated as "Test string nnnn", where nnn is the loop counter. */
    for( iString = 0; iString < iMaxStrings; iString++ )
    {
        /* Call ff_fprintf() to write the formatted string to the file. Note
           the n character on the end of the string. */
        ff_fprintf( pxFile, "Test string %dn", iString );
    }

    /* Move back to the start of the file. */
    ff_rewind( pxFile );

    /* This time use the ff_fgets() string to read back each string at a time,
       then compare it against the expected string. The strings were written with
       a newline character at their end, so ff_fgets() will read up to and
       including the newline. */
    for( iString = 0; iString < iMaxStrings; iString++ )
    {
        /* Read back the next string. */
        pcReturned = ff_fgets( pcReadString, sizeof( pcReadString ), pxFile );

        if( pcReturned != pcReadString )
        {
            /* Error! */
        }
        else
        {
            /* Generate the string that is expected to have been read back. */
            sprintf( pcExpectedString, "Test string %dn", iString );

            /* Compare the string that was expected to be returned against the
               string that was returned. */
            if( strcmp( pcExpectedString, pcReadString ) == 0 )
            {
                /* The strings matched, as expected. */
            }
            else
            {
                /* Error - the strings didn't match. */
            }
        }
    }

    ff_fclose( pxFile );
}
```
*ff_fgets() API 函数用法示例*
