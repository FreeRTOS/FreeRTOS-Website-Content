---
title: "ff_ftell()"
description: FreeRTOS+FAT ff_ftell API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
long ff_ftell( FF_FILE *pxStream );	
```
Returns the current read/write position of an open file in the embedded FAT 
 file system.
 
The position is returned as the number of bytes from the start of the file.

## Parameters 
+ *pxStream*

  The file being queried. The file must have first been opened using a call
  to [ff_fopen()](ff_fopen).

## Returns

If pxStream is not NULL then the file's current read/write position is
 returned. The returned value is the number of bytes the file's read/write 
 position is from the start of the file.
 
If pxStream is NULL then -1 is returned.

## Example usage
```c
void vSampleFunction( char *pcFileName, char *pcBuffer )
{
FF_FILE *pxFile;
long lPosition;

    /* Open the file specified by the pcFileName parameter. */
    pxFile = ff_fopen( pcFileName, "r" );

    /* Expect the file position to be 0. */
    lPosition = ff_ftell( pxFile );
    configASSERT( lPosition == 0 );

    /* Read one byte. */
    ff_fread( pcBuffer, 1, 1, pxFile );

    /* Expect the file position to be 1. */
    lPosition = ff_ftell( pxFile );
    configASSERT( lPosition == 1 );

    /* Read another byte. */
    ff_fread( pcBuffer, 1, 1, pxFile );

    /* Expect the file position to be 2. */
    lPosition = ff_ftell( pxFile );
    configASSERT( lPosition == 2 );

    /* Close the file again. */
    ff_fclose( pxFile );
}
```
*Example use of the ff_ftell() API function*
