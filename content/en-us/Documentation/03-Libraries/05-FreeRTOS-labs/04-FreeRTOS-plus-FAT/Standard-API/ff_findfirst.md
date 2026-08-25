---
title: "ff_findfirst()"
description: FreeRTOS+FAT ff_findfirst API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_findfirst( const char *pcDirectory, ff_finddata_t *pxFindData );
```
Find the first file in a directory within the embedded fat file system.

ff_findfirst() is used with [ff_findnext()](ff_findnext)
 to scan a directory to find all the files the directory contains.
 
Due to its relatively large size it is recommended that the FF_FindData_t
 structure is allocated dynamically, rather than declared as a stack
 variable. The structure **must** also be cleared to zero before it is
 used. See the example below.

 FF_FindData_t contains the fields listed below:
+ pcFileName

  The name of the file.

+ ulFileSize

  The length of the file in bytes

+ ucAttributes

  The file's attributes, which is a bitwise OR of the following bit definitions: 
  * FF_FAT_ATTR_READONLY
  * FF_FAT_ATTR_HIDDEN
  * FF_FAT_ATTR_SYSTEM
  * FF_FAT_ATTR_DIR (directory)

## Parameters 
+ *pcDirectory*

  A pointer to a standard null terminated C string that holds the name of the
   directory in which the first file is to be found. File wildcards are not
   (yet) supported, so the string should only contain the name of the
   directory. For example, to use the current working directory use an
   empty string ( "" ), do not use ("*.*").

+ *pxFindData* 

  A pointer to a structure that is used to store information required to scan a
   directory, and to pass out details of the files contained in the directory.

## Returns
If a file or directory was found then 0 is returned. If an error occurs
 a non-zero value is returned.

## Example usage 
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
*Example use of the ff_findfirst() API function create a directory listing*
