---
title: "ff_findfirst()"
description: FreeRTOS+FAT ff_findfirst API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_findfirst( const char *pcDirectory, ff_finddata_t *pxFindData );
```
在嵌入式 FAT 文件系统的目录中查找第一个文件。

ff_findfirst() 可与 [ff_findnext()](ff_findnext) 一起用于
 扫描目录，以查找目录包含的所有文件。

由于其大小相对而言较大，建议动态分配 FF_FindData_t 结构体，
 而不是声明为堆栈
 变量。该结构体在使用前，也**必须**清零
 。请参阅以下示例。

 FF_FindData_t 包含的字段如下表所示：
+ pcFileName

  文件的名称。

+ ulFileSize

  文件长度（以字节为单位）

+ ucAttributes

  文件属性，是以下位定义的按位 OR： 
  * FF_FAT_ATTR_READONLY
  * FF_FAT_ATTR_HIDDEN
  * FF_FAT_ATTR_SYSTEM
  * FF_FAT_ATTR_DIR（目录）

## 参数 
+ *pcDirectory*

  指向以 null 结尾的标准 C 字符串的指针，该字符串保存
   第一个文件所在目录的名称。（暂且）不支持文件通配符，
   因此字符串只能包含目录名称
   。例如，要使用当前工作目录，请使用
   空字符串 ( "" )，请勿使用 ("*.*")。

+ *pxFindData* 

  指向一个结构体的指针，该结构体用于储存目录扫描所需的信息，
   并传递目录中包含的文件的详细信息。

## 返回
如果找到文件或目录，则返回 0。如果发生错误
 返回非零值。

## 用法示例 
```c
void DIRCommand( const char *pcDirectoryToScan )
{
FF_FindData_t *pxFindStruct;
    const char *pcAttrib;
               *pcWritableFile = "writable file",
               *pcReadOnlyFile = "read only file",
               *pcDirectory = "directory";

    /* FF_FindData_t can be large, so it is best to allocate the structure
       dynamically, rather than declare it as a stack variable. */
    pxFindStruct = ( FF_FindData_t * ) pvPortMalloc( sizeof( FF_FindData_t ) );

    /* FF_FindData_t must be cleared to 0. */
    memset( pxFindStruct, 0x00, sizeof( FF_FindData_t ) );

    /* The first parameter to ff_findfist() is the directory being searched. Do
       not add wildcards to the end of the directory name. */
    if( ff_findfirst( pcDirectoryToScan, pxFindStruct ) == 0 )
    {
        do
        {
            /* Point pcAttrib to a string that describes the file. */
            if( ( pxFindStruct->ucAttributes & FF_FAT_ATTR_DIR ) != 0 )
            {
                pcAttrib = pcDirectory;
            }
            else if( pxFindStruct->ucAttributes & FF_FAT_ATTR_READONLY )
            {
                pcAttrib = pcReadOnlyFile;
            }
            else
            {
                pcAttrib = pcWritableFile;
            }

            /* Print the files name, size, and attribute string. */
            FreeRTOS_printf( ( "%s [%s] [size=%d]", pxFindStruct->pcFileName,
                                                  pcAttrib,
                                                  pxFindStruct->ulFileSize ) );

        } while( [ff_findnext](ff_findnext)( pxFindStruct ) == 0 );
    }

    /* Free the allocated FF_FindData_t structure. */
    vPortFree( pxFindStruct );
}
```
*通过 ff_findfirst() API 函数创建目录列表的用法示例*
