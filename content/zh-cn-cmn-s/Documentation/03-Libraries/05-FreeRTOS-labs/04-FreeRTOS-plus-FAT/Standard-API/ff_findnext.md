---
title: "ff_findnext()"
description: FreeRTOS+FAT ff_findnext API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_findnext( FF_FindData_t *pxFindData );
```

查找嵌入式 FAT 文件系统目录中的下一个文件或目录。
 ff_findnext() 只能在首次调用
 [ff_findfirst()](ff_findfirst) 之后调用。ff_findfirst() 查找
 目录中的第一个文件，ff_findnext() 则查找
 目录中的所有后续文件。

传递给 ff_findnext() 的 FF_FindData_t 对象实例必须
 与传递给 ff_findfirst() 的实例相同。

FF_FindData_t 包含以下字段：
+ pcFileName

  文件名称

+ ulFileSize

  文件长度（以字节为单位）

+ ucAttributes 
  
  文件属性，可以通过“按位或”运算符将以下位的定义 
  组合起来：
    * FF_FAT_ATTR_READONLY
    * FF_FAT_ATTR_HIDDEN
    * FF_FAT_ATTR_SYSTEM
    * FF_FAT_ATTR_DIR（目录）

## 参数 
+ *pxFindData*

  指向一个结构体的指针，该结构体用于存储
  扫描目录所需信息并传递目录中文件的详细信息。

## 返回
如果找到文件或目录，则返回 0。如果发生错误，
 则返回非零值。

## 用法示例
```c
void DIRCommand( const char *pcDirectoryToScan )  
{
    FF_FindData_t *pxFindStruct;
    const char  *pcAttrib;
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
    if( [ff_findfirst](ff_findfirst)( pcDirectoryToScan, pxFindStruct ) == 0 )
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

        } while( ff_findnext( pxFindStruct ) == 0 );
    }

    /* Free the allocated FF_FindData_t structure. */
    vPortFree( pxFindStruct );
}
```
*通过 ff_findfirst() API 函数创建目录列表的用法示例*
