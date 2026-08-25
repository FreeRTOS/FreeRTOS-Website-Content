---
title: FreeRTOS_open()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

**[[FreeRTOS-Plus-IO API](FreeRTOS_IO_API_Functions)]**

FreeRTOS_IO.h

```c
Peripheral_Descriptor_t FreeRTOS_open( const int8_t *pcPath, const uint32_t ulFlags );
```

使用 FreeRTOS-Plus-IO 打开外围设备以供使用。[板级支持包](Board_Support_Packages)
可定义哪些外围设备在任何特定平台上均可用。


**参数：** 

+  *pcPath* 

   根据板级支持包的定义打开的外围设备的[文本名称](Board_Support_Packages#FreeRTOS_Peripheral_Support)  ， 
   如板级支持包中定义的那样。

+ *ulFlags* 

   模式标志。当前未使用此参数。收录此参数有两个原因，  一是使 FreeRTOS_open() 原型 
   与标准 open() 原型保持一致，  二是确保未来 
   FreeRTOS-Plus-IO 开发后的向后兼容性。


**返回：** 

+ 如果无法打开外围设备，则返回 NULL，否则返回一个 Peripheral_Descriptor_t 类型的变量， 
  该变量可用于在今后调用 
  [FreeRTOS_read(), FreeRTOS_write() and FreeRTOS_ioctl()](FreeRTOS_IO_API_Functions) 时访问已打开的外设。


**用法示例：** 

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
*FreeRTOS_open() 示例*

