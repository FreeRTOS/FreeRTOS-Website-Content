---
title: "ff_rewind()"
description: FreeRTOS+FAT ff_rewind API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
void ff_rewind( FF_FILE *pxStream );
```
Moves the current read/write position back to the start of a file.
 Calling ```ff_rewind( pxStream )``` is equivalent to calling 
 ```ff_fseek( pxStream, 0, FF_SEEK_SET )```.

## Parameters 
+ *pxStream*

  The file in which the current read/write position is being set back to the
  start of the file.

## Example usage 
```c
void vSampleFunction( void )
{
    char pcBuffer1[ 4 ], pcBuffer2[ 4 ];
    FF_FILE *pxFile;

    /* Open the file "afile.bin". */
    pxFile = ff_fopen( "afile.bin", "r" );

    if( pxFile != NULL )
    {
        /* Read four bytes into pcBuffer1. */
        ff_fread( pcBuffer1, 4, 1, pxFile );

        /* Set the current read pointer back to the start of the file. */
        ff_rewind( pxFile );

        /* Read the same four bytes into pcBuffer2. */
        ff_fread( pcBuffer2, 4, 1, pxFile );

        /* Finished with the file. */
        ff_fclose( pxFile );
    }
}
```
*Example use of the ff_rewind() API function*
