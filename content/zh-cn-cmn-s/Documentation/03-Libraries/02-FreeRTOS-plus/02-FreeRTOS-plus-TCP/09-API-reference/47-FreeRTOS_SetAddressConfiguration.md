---
title: FreeRTOS_SetAddressConfiguration()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_IP.h

```c
void FreeRTOS_SetAddressConfiguration( const uint32_t * pulIPAddress,
                                       const uint32_t * pulNetMask,
                                       const uint32_t * pulGatewayAddress,
                                       const uint32_t * pulDNSServerAddress );
```

这个函数可以用来更新 IPv4 地址和网络掩码、网关地址和 DNS 服务器地址 
（由 FreeRTOS-Plus-TCP 设备使用）——在调用 FreeRTOS_IPInit() 初始化 TCP 堆栈之后 
[FreeRTOS_IPInit()](https://www.freertos.org/FreeRTOS-Plus/FreeRTOS_Plus_TCP/API/FreeRTOS_IPInit.html)。


**参数：**

+ *`pulIPAddress`*

  指向设备应该使用的 32 位 IPv4 地址的指针（按网络 Endian 顺序排列）。 
  如需保持 IP 地址不变，该指针可以为 NULL。
  
+ *`pulNetMask`*

  指向设备应该使用的 32 位 IPv4 网络掩码的指针（按网络 Endian 顺序排列）。 
  如需保持 IP 网络掩码不变，该指针可以为 NULL。
  
+ *`pulGatewayAddress`* 

  指向设备应该使用的 32 位 IPv4 [gateway](../router)地址的指针（按网络 Endian 顺序排列） 
  。如需保持设备网关地址不变，该指针可以为 NULL。
  
+ *`pulDNSServerAddress`*

  指向设备应使用的 32 位 IPv4 DNS 服务器地址的指针。如果您想让使用中的 
  DNS 服务器 IP 地址保持不变，这个指针可以是 NULL。
  

**注意事项： **

此函数不是线程安全的，应与 `taskENTER_CRITICAL/taskEXIT_CRITICAL` 
对一起使用。只有在没有活动连接（UDP 或 TCP）时才应调用此函数， 
否则连接可能被切断。


**用法示例：**

```c
    void vUserTask( void *pvParameters )  
    {  
        /* 32-bit representation of 192.168.1.12. */  
        uint32_t ulHostEndianIPAddress = 0xC0A8010C;  
        uint32_t ulNetworkEndianIPAddress = FreeRTOS_htonl( ulHostEndianIPAddress );  
        /* 32-bit representation of 192.168.1.1. */  
        uint32_t ulHostEndianGatewayAddress = 0xC0A80101;  
        uint32_t ulNetworkEndianGatewayAddress = FreeRTOS_htonl( ulHostEndianGatewayAddress );  
        /* 32-bit representation of OpenDNS server address 208.67.222.222 */  
        uint32_t ulHostEndianDNSServerAddress = 0xD043DEDE;  
        uint32_t ulNetworkEndianDNSServerAddress = FreeRTOS_htonl( ulHostEndianDNSServerAddress );  
        BaseType_t xUserWantsToUpdateConfiguration = pdFALSE;  
          
        /* Ignore compiler warnings about unused variables. */  
        ( void )  pvParameters;  
      
        for( ; ; )  
        {  
            /* Execute some code. */  
            /* .
             * .  
             * .  
             */ 
      
            /* Note: Make sure that there are no active UDP/TCP conenctions. */  
      
            /* Check whether the user wants to update the IP address. */  
            if( xUserWantsToUpdateConfiguration == pdTRUE )  
            {  
                /* Make sure that no other task can the current task while the  
                 * IP-address is being set. */  
                taskENTER_CRITICAL();  
                {  
                    /* Update the IP address, gateway address and the DNS server address of  
                     * this device but leave the netmask unchanged by passing NULL. */  
                    FreeRTOS_SetAddressConfiguration( &ulNetworkEndianIPAddress ,  
                                                      NULL,  
                                                      &ulNetworkEndianGatewayAddress,  
                                                      &ulNetworkEndianDNSServerAddress );  
                }  
                /* Exit critical section. */  
                taskEXIT_CRITICAL();  
            }  
        }  
    }  
```

