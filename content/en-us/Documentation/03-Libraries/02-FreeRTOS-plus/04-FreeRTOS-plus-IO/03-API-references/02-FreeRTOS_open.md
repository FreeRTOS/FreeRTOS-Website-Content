---
title: "FreeRTOS_open()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**[[FreeRTOS-Plus-IO API](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/01-FreeRTOS_IO_API_Functions)]**

FreeRTOS\_IO.h

```c
Peripheral_Descriptor_t FreeRTOS_open( const int8_t *pcPath, const uint32_t ulFlags );
```

Opens a peripheral for use with FreeRTOS-Plus-IO. The [board support package](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/Board_Support_Packages)
defines which peripherals are available on any particular platform.
 

**Parameters:** 

+  *pcPath* 

   The [text name](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/Board_Support_Packages#FreeRTOS_Peripheral_Support) of the peripheral  being opened, 
   as defined by the board support package.

+ *ulFlags* 

   Mode flags. This parameter is not currently used. It is included  for two reasons - so the FreeRTOS\_open() 
   prototype complies with the standard open()  prototype, and to ensure backward compatibility after future 
   FreeRTOS-Plus-IO developments.


**Returns:** 
 
+ NULL if the peripheral could not be opened, otherwise a variable of type Peripheral\_Descriptor\_t 
  that can be used to access the opened peripheral in future calls 
  to [FreeRTOS\_read(), FreeRTOS\_write() and FreeRTOS\_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/01-FreeRTOS_IO_API_Functions).
 

**Example usage:** 

```c
/* FreeRTOS-Plus-IO includes. */  
#include "FreeRTOS_IO.h"  
  
void vAFunction( void )  
{  
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */  
Peripheral_Descriptor_t xOpenedPort;  
  
    /* Open the SPI port identified in the board support package as using the  
       path string "/SPI2/". The second parameter is not currently used and can  
       be set to anything, although, for future compatibility, it is recommended   
       that it is set to NULL. */  
    xOpenedPort = FreeRTOS_open( "/SPI2/", NULL );  
  
    if( xOpenedPort != NULL )  
    {  
        /* xOpenedPort now contains a valid descriptor that can be used with  
           other FreeRTOS-Plus-IO API functions. */  
          
        . . .  
    }  
    else  
    {  
        /* The port was not opened successfully. */  
    }  
}  
```
*FreeRTOS_open() example*
