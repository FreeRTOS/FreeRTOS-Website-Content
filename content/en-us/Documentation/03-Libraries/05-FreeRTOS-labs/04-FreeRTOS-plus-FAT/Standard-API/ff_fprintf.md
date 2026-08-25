---
title: "ff_fprintf()"
description: FreeRTOS+FAT ff_fprintf API documentation
---
[[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)]

ff_stdio.h
```c
size_t ff_fprintf( FF_FILE * pxStream, const char *pcFormat, ... );	
```
Writes formatted data to a file in exactly the same way sprintf() writes
 formatted data to a buffer, or printf() writes formatted data to a console.

ff_fprintf() calls vsnprintf(), which must be provided by your C library
 for a project that uses ff_fprintf() to link. The format specifiers and
 extensions (for example "%02D", "%s", etc.) that are available for use
 will depend on your C library.

FF_FPRINTF_SUPPORT must be set to 1 in FreeRTOSFATConfig.h for ff_fprintf()
 to be available.

**Note:** ff_fprintf() is quite a heavy function as it allocates
 memory into which it writes is formatted data before outputting the data
 to the file. It also uses vsnprintf(), which can result in lots of
 additional library code being included in your project.

## Parameters 
+ *pxStream*

  A pointer to the file to which the formatted data is being written. This is
  the same pointer that was returned from the call to ff_fopen() used to 
  originally open the file.

+ *pcFormat*

  The format string, which is used in exactly the same way as the format string
  input to a printf() call. The format specifiers that are available for use
  will depend on the C library in use.

+ *...*

  A variable list of argument values - with one value for each specifier
  included in the format string.

## Returns
If ff_printf() could not allocate a buffer then 0 is returned.

If data was written to the file then the number of bytes written is
 returned. 

If there was a write error then -1 is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the 
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage 
The example provided on the [ff_fgets()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/ff_fgets)
 documentation page shows how ff_fprintf() is used.
