---
title: FreeRTOS_IPInit()
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
BaseType_t FreeRTOS_IPInit( const uint8_t ucIPAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucNetMask[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucGatewayAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucDNSServerAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucMACAddress[ ipMAC_ADDRESS_LENGTH_BYTES ] );
```

初始化 FreeRTOS-Plus-TCP 堆栈。必须在调用任何其他 FreeRTOS-Plus-TCP 函数之前调用 FreeRTOS_IPInit()。

ipIP_ADDRESS_LENGTH_BYTES 定义为 4。ipMAC_ADDRESS_LENGTH_BYTES 定义为 6。


**参数：** 

+ *ucIPAddress* 
  
  如果 ipconfigUSE_DHCP 设为 0（在 FreeRTOSIPConfig.h 中），则网络节点的 IP 地址 
  为静态地址，并由 ucIPAddress 的值配置。

  如果 ipconfigUSE_DHCP 设为 1，则 FreeRTOS-Plus-TCP 将尝试从  
  DHCP 服务器获取 IP 地址。无法获取 IP 地址，则网络节点将恢复使用 
  ucIPAddress 的值配置的静态 IP 地址。

  IP 地址指定为 4 字节数组，其中索引 0 保存 IP 地址的第一个八位组， 
  而索引 3 保存 IP 地址的最后一个八位组。请参阅以下示例。

+ *ucNetmask* 
  
  如果 ipconfigUSE_DHCP 设为 0（在 FreeRTOSIPConfig.h 中），则网络节点的网络掩码为静态掩码， 
  并由 ucNetmask 的值配置。

  如果 ipconfigUSE_DHCP 设为 1，则 FreeRTOS-Plus-TCP 将尝试从 DHCP 服务器获取网络掩码 
  。如果无法获取网络掩码，则网络节点将恢复使用 
  由 ucNetMask 的值配置的静态网络掩码。

  网络掩码指定为 4 字节数组，其中索引 0 保存网络掩码的第一个八位组， 
  索引 3 保存网络掩码的最后一个八位组。请参阅以下示例。

+ *ucGatewayAddress* 
  
  如果 ipconfigUSE_DHCP 设为 0（在 FreeRTOSIPConfig.h 中），则网络网关的 IP 地址为静态地址， 
  并由 ucGatewayAddress 的值配置。

  如果 ipconfigUSE_DHCP 设为 0，则 FreeRTOS-Plus-TCP 将尝试从 DHCP 服务器获取网络网关的 IP 地址 
  。如果无法获取网关 IP 地址，则网络节点 
  将恢复使用由 ucGatewayAddress 的值配置的静态 IP 地址，作为网关地址  
  。

  IP 地址指定为 4 字节数组，其中索引 0 保存 IP 地址的第一个八位组， 
  而索引 3 保存 IP 地址的最后一个八位组。请参阅以下示例。

+ *ucDNSServerAddress* 
  
  如果 ipconfigUSE_DHCP 设为 0（在 FreeRTOSIPConfig.h 中），则 DNS 服务器的 IP 地址为静态地址， 
  并由 ucDNSServerAddress 的值配置。

  如果 ipconfigUSE_DHCP 设为 1，则 FreeRTOS-Plus-TCP 将尝试从 DHCP 服务器获取 DNS 服务器的 IP 地址
  。如果无法获取 DNS 服务器 IP 地址，则网络节点将 
  恢复使用由 ucDNSServerAddress 的值配置的静态 IP 地址，作为 DNS 服务器地址 
  。

  IP 地址指定为 4 字节数组，其中索引 0 保存 IP 地址的第一个八位组， 
  而索引 3 保存 IP 地址的最后一个八位组。请参阅以下示例。

+ *ucMACAddress* 

  网络节点的 MAC 地址。

  MAC IP 地址指定为六字节数组，其中索引 0 保存 MAC 地址的第一个八位组， 
  而索引 5 保存 MAC 地址的最后一个八位组。请参阅以下示例。


**返回：** 

+ 如果 TCP/IP 堆栈初始化成功，则返回 pdPASS。

+ 如果 TCP/IP 堆栈因为以下原因未初始化，则返回 pdFAIL：因为 FreeRTOS_IPInit() 
  之前已调用，或者是无法创建网络缓冲区或 IP RTOS 任务 
  。


**用法示例：** 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
/* Define the network addressing. These parameters will be used if either  
   ipconfigUDE_DHCP is 0 or if ipconfigUSE_DHCP is 1 but DHCP auto configuration  
   failed. */  
static const uint8_t ucIPAddress[ 4 ] = { 192, 168, 0, 200 };  
static const uint8_t ucNetMask[ 4 ] = { 255, 255, 255, 255 };  
static const uint8_t ucGatewayAddress[ 4 ] = { 192, 168, 0, 1 };  
  
/* The following is the address of an OpenDNS server. */  
static const uint8_t ucDNSServerAddress[ 4 ] = { 208, 67, 222, 222 };  
  
/* The MAC address array is not declared const as the MAC address will normally  
   be read from an EEPROM and not hard coded (in real deployed applications).*/  
static uint8_t ucMACAddress[ 6 ] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55 };  
  
void aFunction( void )  
{  
    /* Initialise the TCP/IP stack. */  
    FreeRTOS_IPInit( ucIPAddress,  
                     ucNetMask,  
                     ucGatewayAddress,  
                     ucDNSServerAddress,  
                     ucMACAddress );  
}  
```
*FreeRTOS_IPInit() API 函数的使用示例*

