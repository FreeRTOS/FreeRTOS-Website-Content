---
title: "ff_seteof()"
description: FreeRTOS+FAT ff_seteof API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_seteof( FF_FILE *pxStream );
```
从文件的当前读/写位置进行截断。文件
 必须已通过调用 [ff_fopen()](ff_fopen) 打开，
 并且模式字符串设置为 "a" 或 "w"。

## 参数
+ *pxStream*

  待截断的文件。

## 返回

如果文件截断成功，则返回零。

如果文件无法截断，则返回 FF_EOF，并设置任务的 
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务可以使用
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数获取其 errno 值。

## 用法示例

```c
void vSampleFunction( char *pcFileName, long lTruncatePosition )  
{  
    FF_FILE *pxFile;  
    
    /* Open the file specified by the pcFileName parameter. */  
    pxFile = ff_fopen( pcFileName, "a" );  
    
    /* Move the current read/write position to the position specified by  
       the lTruncatePosition parameter. */  
    ff_fseek( pxFile, lTruncatePosition, FF_SEEK_SET );  
    
    /* Truncate the file so all data past the current file position is lost. */  
    if( ff_seteof( pxFile ) != FF_EOF )  
    {  
    /* The truncate failed. */  
    }  
    
    /* Finished with the file. */  
    ff_fclose( pxFile );  
}  
```
*ff_seteof() API 函数用法示例*
