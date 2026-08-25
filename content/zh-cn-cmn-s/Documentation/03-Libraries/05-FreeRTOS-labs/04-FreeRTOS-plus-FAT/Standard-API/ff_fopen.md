---
title: "ff_fopen()"
description: FreeRTOS+FAT ff_fopen API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
FF_FILE *ff_fopen( const char *pcFile, const char *pcMode );	
```
在嵌入式 FAT 文件系统中打开文件。

## 参数 
+ *pcFile*

  指向以 null 结尾的标准 C 字符串的指针，该字符串保存正在打开的文件名称。该字符串可包含相对路径。

+ *pcMode*

  设置文件打开模式的字符串。 
  有效字符串包括：

  - "r"：以只读方式打开文件。

  - "r+"：以可读写方式打开文件。

  - "w"：以可读写方式打开文件。如果文件已经存在， 
    则文件长度会被截断为 0。如果文件尚不存在， 
    则将创建文件。

  - "a"：以可写入方式打开文件。如果文件已经存在，则新数据 
    将附加到文件末尾。如果文件尚不存在，
    则将创建文件。

  - "a+"：以可读写方式打开文件。如果文件已经存在，
    则新数据将附加到文件末尾。如果文件
    尚不存在，则将创建文件。文件始终以二进制模式打开。

## 返回
如果成功打开文件，
 则返回指向该文件的指针。

如果无法打开文件，则返回 NULL，
 并设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务
 可以使用 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API 函数获取其 errno 值。

## 用法示例 
```c
BaseType_t xCopyFile( char *pcSourceFileName, char *pcDestinationFileName )
{
    FF_FILE *pxSourceFile, *pxDestinationFile;
    size_t xCount;
    uint32_t ucBuffer[ 50 ];

    /* Open the source file in read only mode. */
    pxSourceFile = ff_fopen( pcSourceFileName, "r" );

    if( pxSourceFile != NULL )
    {
        /* Create or overwrite a writable file. */
        pxDestinationFile = ff_fopen( pcDestinationFileName, "w+" );

        if( pxDestinationFile != NULL )
        {
            for( ;; )
            {
                /* Read sizeof( ucBuffer ) bytes from the source file into a buffer. */
                xCount = ff_fread( ucBuffer, 1, sizeof( ucBuffer ), pxSourceFile );

                /* Write however many bytes were read from the source file into the
                   destination file. */
                ff_fwrite( ucBuffer, xCount, 1, pxDestinationFile );

                if( xCount < sizeof( ucBuffer ) )
                {
                    /* The end of the flie was reached. */
                    break;
                }
            }

            /* Close the destination file. */
            ff_fclose( pxDestinationFile );
        }

        /* Close the source file. */
        ff_fclose( pxSourceFile );
    }
}
```
*通过 ff_fopen() API 函数打开或创建文件的使用示例*
