---
title: "ff_fgetc()"
description: FreeRTOS+FAT ff_fgetc API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_fgetc( FF_FILE * pxStream );	
```
Reads a single byte from an open file in the embedded FAT file system.
 The read/write position is incremented by one.

Returning a char in an int may not seem optimal, but the ff_fgetc()
 prototype conforms to the standard and expected stdio fgetc() function prototype.


## Parameters 
+ *pxStream*

  A pointer to the file from which the data is being read. This is the same
   pointer that was returned from the call to ff_fopen() used to originally
   open the file.

## Returns
On success the byte read from the file system is returned. If a byte
 could not be read from the file because the read position is already at
 the end of the file then FF_EOF is returned.

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
        iReturnedByte = ff_fgetc( pxFile );

        if( iReturnedByte == FF_EOF )
        {
            /* A byte could not be read because the end of the file has
               been reached. */
            break;
        }
        else
        {
            /* Write the byte into the buffer. */
            pcBuffer[ lBytesRead ] = ( char ) iReturnedByte;
        }
    }

    /* Finished with the file. */
    ff_fclose( pxFile );
}
```
*Example use of the ff_fgetc() API function*
