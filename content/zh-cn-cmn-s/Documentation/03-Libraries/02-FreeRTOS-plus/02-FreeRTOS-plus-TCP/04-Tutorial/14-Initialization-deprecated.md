---
title: 初始化 TCP/IP 堆栈
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

**注意：自 FreeRTOS V4.0.0 起，这些堆栈初始化 API 已被弃用。有关支持 IPv6、多端点和多接口的新 API，请参阅
“初始化 TCP/IP 堆栈”。
要使用已弃用的 API，请在 FreeRTOSIPConfig.h 头
文件中将 ipconfigIPv4_BACKWARD_COMPATIBLE 设置为 1。**


此页介绍了 [FreeRTOS_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit)
以及当“网络启用”和“网络关闭”事件发生时被调用的[回调函数](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/57-vApplicationIPNetworkEventHook)
。

[FreeRTOS_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit)
必须是调用的首个 FreeRTOS-Plus-TCP 函数。FreeRTOS_IPInit() 可以
在 RTOS 调度器启动之前或之后调用。

FreeRTOS_IPInit () 会创建 FreeRTOS-Plus-TCP RTOS 任务。FreeRTOS-Plus-TCP 任务
会配置和初始化网络接口。如果 ipconfigUSE_NETWORK_EVENT_HOOK
在 [FreeRTOSIPConfig.h](TCP_IP_Configuration) 中设置为 1，
当网络准备就绪时，TCP/IP 堆栈将调用 [vIPNetworkEventHook()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/57-vApplicationIPNetworkEventHook) 
回调函数。

以下为两个示例。第一个示例演示了 FreeRTOS_IPInit()。
第二个示例演示了 vIPNetworkEventHook()。

```c
/* The MAC address array is not declared const as the MAC address will
   normally be read from an EEPROM and not hard coded (in real deployed
   applications).*/
static uint8_t ucMACAddress[ 6 ] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55 };

/* Define the network addressing. These parameters will be used if either
   ipconfigUDE_DHCP is 0 or if ipconfigUSE_DHCP is 1 but DHCP auto configuration
   failed. */
static const uint8_t ucIPAddress[ 4 ] = { 10, 10, 10, 200 };
static const uint8_t ucNetMask[ 4 ] = { 255, 0, 0, 0 };
static const uint8_t ucGatewayAddress[ 4 ] = { 10, 10, 10, 1 };

/* The following is the address of an OpenDNS server. */
static const uint8_t ucDNSServerAddress[ 4 ] = { 208, 67, 222, 222 };

int main( void )
{
    /* Initialise the RTOS's TCP/IP stack. The tasks that use the network
       are created in the vApplicationIPNetworkEventHook() hook function
       below. The hook function is called when the network connects. */
    FreeRTOS_IPInit( ucIPAddress,
                     ucNetMask,
                     ucGatewayAddress,
                     ucDNSServerAddress,
                     ucMACAddress );

    /*
     * Other RTOS tasks can be created here.
     */

    /* Start the RTOS scheduler. */
    vTaskStartScheduler();

    /* If all is well, the scheduler will now be running, and the following
       line will never be reached. If the following line does execute, then
       there was insufficient FreeRTOS heap memory available for the idle and/or
       timer tasks to be created. */
    for( ;; );
}

```
*FreeRTOS_IPInit() API 函数的使用示例*


```c
void vApplicationIPNetworkEventHook( eIPCallbackEvent_t eNetworkEvent )
{
static BaseType_t xTasksAlreadyCreated = pdFALSE;

    /* Both eNetworkUp and eNetworkDown events can be processed here. */
    if( eNetworkEvent == eNetworkUp )
    {
        /* Create the tasks that use the TCP/IP stack if they have not already
           been created. */
        if( xTasksAlreadyCreated == pdFALSE )
        {
            /*
             * For convenience, tasks that use FreeRTOS-Plus-TCP can be created here
             * to ensure they are not created before the network is usable.
             */

            xTasksAlreadyCreated = pdTRUE;
        }
    }
}

```
*vApplicationIPNetworkEventHook() 定义示例*

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
