---
title: "ff_fseek()"
description: FreeRTOS+FAT ff_fseek API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_fseek( FF_FILE *pxStream, int iOffset, int iWhence );
```

Moves the current read/write position of an open file to ( iWhence + iOffset ).

The read/write position of an open file cannot be set to beyond the end of the
 existing data of the file. If the value of either of iOffset, iWhence,
 (iOffset + iWhence) is larger than the size of the file pointed by *pxStream,
 ff_fseek() returns an illegal seek (29) error.

## Parameters 
+ *pxStream* 

  The file in which the current read/write position is being updated.

+ *iOffset*

  An offset (in bytes) from the position set by the iWhence parameter to which
  the file's current read/write position will be set.

+ *iWhence*

  The position within the file from which the iOffset value is relative. Valid
  values for iWhence include:
  + *FF_SEEK_CUR*: The current file position.
  + *FF_SEEK_END*: The end of the file.
  + *FF_SEEK_SET*: The beginning of the file.

## Returns

On success 0 is returned.

If the read/write position could not be moved, then -1 is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage 
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
*Example use of the ff_fseek() API function*
