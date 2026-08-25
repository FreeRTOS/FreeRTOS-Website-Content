---
title: "ff_feof()"
description: FreeRTOS+FAT ff_feof API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_feof( FF_FILE *pxStream );
```
Queries an open file in the embedded FAT file system to see if the file's
 read/write pointer is at the end of the file.

## Parameters 
+ *pxStream*

  The file being queried. The file must have first been opened using a call to
  [ff_fopen()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fopen).

## Returns

If the file's read/write pointer is at the end of the file then
 a non-zero value is returned.

If the file's read/write pointer is not at the end of the file, and no
 errors occur, then zero is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is also set to zero.

If an error prevents the function from determining the position of the
 file's read/write pointer then zero is returned and the task's errno is
 set to indicate the reason.

A task can obtain its errno value using the
 [stdioGET_ERRNO](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage 
```c
void vSampleFunction( char *pcFileName, char *pcBuffer, int32_t lBufferSize )
{
    FF_FILE *pxFile;
    int32_t lBytesRead;
    int iReturnedByte;

    /* Open the file specified by the pcFileName parameter. */
    pxFile = ff_fopen( pcFileName, "r" );

    /* Read the number of bytes specified by the lBufferSize parameter. */
    for( lBytesRead = 0; lBytesRead < lBufferSize; lBytesRead++ )
    {
        if( ff_feof( pxFile ) != 0 )
        {
            /* The end of the file has been reached, there are no more bytes to
               read. */
            break;
        }
        else
        {
            iReturnedByte = ff_fgetc( pxFile );
        }

        /* Write the byte into the buffer. */
        pcBuffer[ lBytesRead ] = ( char ) iReturnedByte;
    }

    /* Finished with the file. */
    ff_fclose( pxFile );
}
```
Example use of the ff_feof() API function
