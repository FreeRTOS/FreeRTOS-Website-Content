---
title: "ff_fseek()"
description: FreeRTOS+FAT ff_fseek API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_fseek( FF_FILE *pxStream, int iOffset, int iWhence );
```

将打开文件的当前读/写位置移动到 ( iWhence + iOffset )。

## 参数 
+ *pxStream* 

  正在更新当前读/写位置的文件。

+ *iOffset*

  与 iWhence 参数所设位置（文件当前读/写位置将设为此位置）的偏移量
  （单位为字节）。

+ *iWhence*

  与 iOffset 值相对的文件中位置。iWhence
  的有效值包括：
  + *FF_SEEK_CUR*：当前文件位置。
  + *FF_SEEK_END*：文件末尾。
  + *FF_SEEK_SET*：文件开头。

## 返回

成功时返回 0。

如果无法移动读/写位置，则返回 -1，并
 设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务可以使用
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数获取其 errno 值。

## 用法示例 
```c
void vSampleFunction( char *pcFileName, char *pcBuffer )
{
    FF_FILE *pxFile;

    /* Open the file specified by the pcFileName parameter. */
    pxFile = ff_fopen( pcFileName, "r" );

    if( pxFile != NULL )
    {
        /* Read one byte from the opened file. */
        ff_fread( pcBuffer, 1, 1, pxFile );

        /* Move the current file position back to the very start of the file. */
        ff_fseek( pxFile, 0, FF_SEEK_SET );

        /* Read a byte again. As the file position was moved back to the start
           of the file the byte that is read is the same byte read by the first
           ff_fread() call. */
        ff_fread( pcBuffer, 1, 1, pxFile );

        /* This time move the current position to the last byte in the file. */
        ff_fseek( pxFile, -1, FF_SEEK_END );

        /* Now the byte read is the last byte in the file. */
        ff_fread( pcBuffer, 1, 1, pxFile );

        /* Finished with the file, close it. */
        ff_fclose( pxFile );
    }
}
```
*ff_fseek() API 函数用法示例*
