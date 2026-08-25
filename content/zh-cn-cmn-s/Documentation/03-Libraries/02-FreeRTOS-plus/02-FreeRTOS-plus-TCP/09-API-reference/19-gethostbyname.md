---
title: FreeRTOS_gethostbyname()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h

```c
uint32_t FreeRTOS_gethostbyname( const uint8_t *pcHostName );
```

对主机名执行域名系统 (DNS) 查找，返回主机 IP 地址。例如， 
假设 DNS 服务器回复了查找请求，对 FreeRTOS_gethostbyname ("www.freertos.org") 的调用 
将返回 freertos.org 的 IP 地址。

要使用 FreeRTOS_gethostbyname()，必须在 FreeRTOSIPConfig.h 中将 ipconfigUSE_DNS 设置为 1。

只有当 FreeRTOS-Plus-TCP 知道 DNS 服务器的 IP 地址时，才会执行 DNS 查找 。如果 
 FreeRTOSIPConfig.h 中的 ipconfigUSE_DHCP 值为 0 ，则 DNS 服务器地址会传入 FreeRTOS-Plus-TCP， 
作为 FreeRTOS_IPInit() 函数的参数。如果 ipconfigUSE_DHCP 在 FreeRTOSIPConfig.h 中为 1， 
则可以从 DHCP 服务器获取 DNS 服务器地址。

FreeRTOS_gethostbyname() 将在每个  
DNS 请求后等待（处于阻塞状态，以便可以执行其他任务）回复 200 毫秒——最多发送 5 个 DNS 请求。


**参数：** 

+ *pcHostName*

  标准的零结尾字符串，其中包含正在查找的主机的名称。


**返回：** 

+ 如果查找成功，则以网络字节顺序返回主机 IP 地址。

+ 如果查找失败，则返回 0。


**用法示例：** 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( void )  
{  
uint32_t ulIPAddress;  
int8_t cBuffer[ 16 ];  
  
    /* Lookup the IP address of the FreeRTOS.org website. */  
    ulIPAddress = FreeRTOS_gethostbyname( "www.freertos.org" );  
  
    if( ulIPAddress != 0 )  
    {  
        /* Convert the IP address to a string. */  
        FreeRTOS_inet_ntoa( ulIPAddress, ( char * ) cBuffer );  
  
        /* Print out the IP address. */  
        printf( "www.FreeRTOS.org is at IP address %srn", cBuffer );  
    }  
    else  
    {  
        printf( "DNS lookup failed. " );  
    }  
}  
```
*FreeRTOS_gethostbyname() API 函数用法示例*

