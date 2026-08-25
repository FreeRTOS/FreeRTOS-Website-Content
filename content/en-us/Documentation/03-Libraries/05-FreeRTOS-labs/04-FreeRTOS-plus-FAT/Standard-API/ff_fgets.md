---
title: "ff_fgets()"
description: FreeRTOS+FAT ff_fgets API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
char *ff_fgets( char *pcBuffer, size_t xCount, FF_FILE *pxStream );	
```
Reads a string from a file by reading bytes from pxStream into pcBuffer until either (xCount - 1) bytes have been read,
 or a newline ('n') character has been read into to pcBuffer.

Carriage return characters ('r') are not treated in any special way, and
 are copied into pcBuffer.

The string copied into pcBuffer is NULL terminated before ff_fgets() returns.

## Parameters 
+ *pcBuffer*

  A pointer to the buffer into which characters read from the file will be 
   placed. The buffer must be at least big enough to hold xCount bytes.

+ *xCount*

  Bytes will be read from the file until either a newline character has been
   received, or (xCount - 1) bytes have been read.

+ *pxStream*

  A pointer to the file from which the data is being read. This is the same
   pointer that was returned from the call to ff_fopen() used to originally 
   open the file.

## Returns
On success a pointer to pcBuffer is returned. If there is a read error then NULL is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) is set to indicate the reason.

A task can obtain its errno value using the [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API function.

## Example usage 
```c
static void prvTest_ff_fgets_ff_printf( const char *pcMountPath )
{
    FF_FILE *pxFile;
    int iString;
    const int iMaxStrings = 1000;
    char pcReadString[ 20 ], pcExpectedString[ 20 ], *pcReturned;
    const char *pcMaximumStringLength = "Test string 999n";

    /* Open a file for reading and writing. */
    pxFile = ff_fopen( "/nand/myfile.txt", "w+" );

    /* Use ff_fprintf() to write some strings to the file. The strings are
       generated as "Test string nnnn", where nnn is the loop counter. */
    for( iString = 0; iString < iMaxStrings; iString++ )
    {
        /* Call ff_fprintf() to write the formatted string to the file. Note
           the n character on the end of the string. */
        ff_fprintf( pxFile, "Test string %dn", iString );
    }

    /* Move back to the start of the file. */
    ff_rewind( pxFile );

    /* This time use the ff_fgets() string to read back each string at a time,
       then compare it against the expected string. The strings were written with
       a newline character at their end, so ff_fgets() will read up to and
       including the newline. */
    for( iString = 0; iString < iMaxStrings; iString++ )
    {
        /* Read back the next string. */
        pcReturned = ff_fgets( pcReadString, sizeof( pcReadString ), pxFile );

        if( pcReturned != pcReadString )
        {
            /* Error! */
        }
        else
        {
            /* Generate the string that is expected to have been read back. */
            sprintf( pcExpectedString, "Test string %dn", iString );

            /* Compare the string that was expected to be returned against the
               string that was returned. */
            if( strcmp( pcExpectedString, pcReadString ) == 0 )
            {
                /* The strings matched, as expected. */
            }
            else
            {
                /* Error - the strings didn't match. */
            }
        }
    }

    ff_fclose( pxFile );
}
```
*Example use of the ff_fgets() API function*
