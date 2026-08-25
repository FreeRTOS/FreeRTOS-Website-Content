---
title: "ff_getcwd()"
description: FreeRTOS+FAT ff_getcwd API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
char *ff_getcwd( char *pcBuffer, size_t xBufferLength );	
```
Writes the name of the current working directory (CWD) to the buffer
 pointed to by pcBuffer. The name is written as a standard null terminated
 C string.

## Parameters 
+ *pcBuffer*

  A pointer to the buffer into which the name of the current working directory will be written.

+ *xBufferLength*

  The size (in bytes) of the buffer pointed to by pcBuffer.

## Returns

 If the current working directory name was successfully written to pcBuffer
 then pcBuffer is returned. Otherwise NULL is returned.
 
## Example usage 
```c
void vExampleFunction( void )
{
    char pcBuffer[ 50 ];

    /* Create a sub directory called subfolder, and sub directory within
       subfolder called sub1. */
    ff_mkdir( "subfolder" );
    ff_mkdir( "subfolder/sub1" );

    /* Move into subfolder/sub1. */
    ff_chdir( "subfolder/sub1" );

    /* Print out the current working directory - it should be
       "subfolder/sub1". */
    ff_getcwd( pcBuffer, sizeof( pcBuffer ) );
    printf( "%s", pcBuffer );
}
```
*Example use of the ff_getcwd() API function to open or create a file*
