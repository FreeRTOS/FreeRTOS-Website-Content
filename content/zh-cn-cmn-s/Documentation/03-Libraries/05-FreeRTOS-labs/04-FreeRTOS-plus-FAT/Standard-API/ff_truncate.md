---
title: "ff_truncate()"
description: FreeRTOS+FAT ff_truncate API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h

```c
FF_FILE *ff_truncate( const char * pcFileName, long lTruncateSize );
```

打开文件，写入数据，然后截断文件，长度为 lTruncateSize。

如果文件长度超过 lTruncateSize，则超过部分的数据
将被丢弃。

如果文件长度小于 lTruncateSize，则在文件末尾追加的新数据
将被设置为 0。


## 参数

+ *pcFileName*

  指向以 null 结尾的标准 C 字符串的指针，该字符串包含要打开并截断的文件的名称。 
  文件名称可以包含指向该文件的相对路径。

+ *lTruncateSize*

  目标长度，以字节为单位，文件的长度将设置为此值。


## 返回

如果文件长度成功设置为 lTruncateSize，
则返回指向已打开文件的指针。

如果文件长度未能成功设置为 lTruncateSize， 
 则返回 NULL，关闭文件，并设置任务的
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务可以 
 使用 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API 函数获取其 errno 值。


## 用法示例

```c
void vSampleFunction( char *pcFileName, long lLength )  
{  
    FF_FILE *pxFile;  
  
    /* Open and truncate the file specified by the pcFileName parameter. */  
    pxFile = ff_truncate( pcFileName, lLength );  
  
    if( pxFile == NULL )  
    {  
        /* The file could not be opened, or the file could not be truncated. */  
    }  
    else  
    {  
        /* The file was opened and the file length was set. */  
  
        /*  
         * The file can be accessed here.  
         */  
      
        /* Close the file when it is no longer required. */  
        ff_fclose( pxFile );  
    }  
}  
  
```
*ff_truncate() API 函数用法示例*
