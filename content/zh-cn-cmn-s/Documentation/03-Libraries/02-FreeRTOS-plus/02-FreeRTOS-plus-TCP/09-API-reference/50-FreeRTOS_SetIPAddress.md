---
title: FreeRTOS_SetIPAddress()
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
void FreeRTOS_SetIPAddress( uint32_t ulIPAddress );
```

此函数可用于更新 FreeRTOS-Plus-TCP 设备使用的 IPv4 地址， 
——在通过调用 [FreeRTOS_IPInit()](FreeRTOS_IPInit) 初始化 TCP 堆栈之后。


**参数：**

+ *ulIPAddress*

  设备应使用的 32 位 IPv4 地址（按网络 Endian 顺序排列）。 [FreeRTOS_htonl](htons_ntohs_htonl_ntohl) 
  可用于获取 32 位 IP 地址的网络 Endian 表示。


**注意事项： **

此函数不是线程安全的，应与 `taskENTER_CRITICAL/taskEXIT_CRITICAL` 
对一起使用。只有在没有活动连接（UDP 或 
或 TCP）时才应调用此函数，否则连接可能被切断。


**用法示例：**

可参考下述代码片段了解如何使用 `FreeRTOS_SetIPAddress`。

```c
    void vUserTask( void *pvParameters )  
    {  
        /* 32-bit representation of 192.168.1.12. */  
        uint32_t ulHostEndianIPAddress = 0xC0A8010C;  
        uint32_t ulNetworkEndianIPAddress = FreeRTOS_htonl( ulHostEndianIPAddress );  
        /* 32-bit representation of 192.168.1.1. */  
        uint32_t ulHostEndianGatewayAddress = 0xC0A80101;  
        uint32_t ulNetworkEndianGatewayAddress = FreeRTOS_htonl( ulHostEndianGatewayAddress );  
        uint32_t ulHostEndianNetmask = 0xFFFFFF00;  
        uint32_t ulNetworkEndianNetmask = FreeRTOS_htonl( ulHostEndianNetmask );  
        BaseType_t xUserWantsToUpdateIP = pdFALSE;  
        BaseType_t xUserWantsToUpdateNetmask = pdFALSE;  
        BaseType_t xUserWantsToUpdateGateway = pdFALSE;  
      
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
            if( xUserWantsToUpdateIP == pdTRUE )  
            {  
                /* Make sure that no other task can the current task while the  
                 * IP-address is being set. */  
                taskENTER_CRITICAL();  
                {  
                    /* Set the IP address of this device. */  
                    FreeRTOS_SetIPAddress( ulNetworkEndianIPAddress );  
                }  
                /* Exit critical section. */  
                taskEXIT_CRITICAL();  
            }  
              
            /* Check whether the user wants to update the IP netmask. */  
            if( xUserWantsToUpdateNetmask == pdTRUE )  
            {  
                /* Make sure that no other task can the current task while the  
                 * IP-address is being set. */  
                taskENTER_CRITICAL();  
                {  
                    /* Set the IP netmask of this device. */  
                    FreeRTOS_SetNetmask( ulNetworkEndianNetmask );  
                }  
                /* Exit critical section. */  
                taskEXIT_CRITICAL();  
            }  
              
            /* Check whether the user wants to update the gateway address. */  
            if( xUserWantsToUpdateGateway == pdTRUE )  
            {  
                /* Make sure that no other task can the current task while the  
                 * IP-address is being set. */  
                taskENTER_CRITICAL();  
                {  
                    /* Set the IP netmask of this device. */  
                    FreeRTOS_SetGetwayAddress( ulNetworkEndianGatewayAddress );  
                }  
                /* Exit critical section. */  
                taskEXIT_CRITICAL();  
            }  
        }  
    }  
```

