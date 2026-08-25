---
title: 使用 coreMQTT 的 MQTT Agent 及其演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

包括 Over the Air ([OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)) 更新

**注意**：本页已作废。请使用采用 coreMQTT Agent 的线程安全 [coreMQTT Agent 演示](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)
。


* 本页内容：
    + [实现情况概览和使用模型](#实现情况概览和使用模型)
    + [MQTT Agent 演示项目](#演示项目)

        - [功能](#功能)
        - [获取源文件](#获取源代码)
        - [源代码组织](#源代码组织)
        - [配置 FreeRTOS-Plus-TCP](#配置-freertos-plus-tcp)
        - [配置 MQTT 代理连接](#配置-mqtt-代理连接)
        - [配置 MQTT agent](#mqtt-agent-配置常量)+ [使用 MQTT agent API 的示例](#mqtt-agent-api-使用示例)
    + [MQTT agent API](#mqtt-agent-api)


## 引言

coreMQTT 是一个 MIT 授权的开源 MQTT 客户端 C 库，适用于基于微控制器和小型微处理器的
IoT 设备。该客户端库设计简洁，确保其不依赖任何其他库或操作系统，
能更好地执行静态分析，如内存安全证明。正因为这种简单性
和独立于操作系统的特性（coreMQTT 完全不需要多线程），coreMQTT
不会直接在实现过程中构建线程安全。相反，线程安全必须
由更高级别的软件提供。本页所演示的 coreMQTT 扩展
以 MQTT agent（或 MQTT 守护进程）的形式提供更高级的功能。虽然此处演示的实现
目前专用于 FreeRTOS，但对 FreeRTOS 的依赖项并不多，
也就是说可以轻松调整该实现，以适配其他操作系统。


## 实现情况概览和使用模型

MQTT Agent 是独立的任务（或执行线程）。它是获准访问 MQTT 库 API 的唯一任务，
因此可轻松实现线程安全。隔离对单个任务的所有 MQTT API 调用
可以实现访问序列化，进而无需信号量或任何其他同步原语。

使用 Agent 时，如果应用程序任务想要执行 MQTT 操作，例如发布消息，
其会调用 MQTT Agent 的 MQTTAgent_Publish() API ，而不是调用 coreMQTT 的 MQTT_Publish()
API。MQTTAgent_Publish() 将完成 Publish 操作所需的信息打包到结构体中，
然后通过队列将该结构体发送到 MQTT Agent 任务。MQTT Agent 任务
接收该结构体，然后代表应用程序调用基础 MQTT 库的 MQTT_Publish() API。

应用程序写入器可借助向 MQTT Agent 发送命令的 API，
选择性指定回调函数以及要传递给回调的参数（称为“回调上下文”），
以便 Agent 在生成的 MQTT 操作完成时执行。如此一来，应用程序任务可以
选择进入阻塞状态（因此不会占用任何 CPU 时间）等待回调执行，
或者在 MQTT 操作正在进行时继续执行
。[请参阅本页末尾的示例](#mqtt-agent-api-使用示例)。

如果在 MQTT Agent API 调用时队列已满，
应用程序写入器还可借助向 MQTT Agent 发送命令的 API，
指定调用任务在阻塞状态下等待用于向 MQTT Agent 发送命令的队列中存在可用空间的最长时间。
同样，[请参阅本页末尾的示例](#mqtt-agent-api-使用示例)。


## 演示项目

### 序言

**注意：**MQTT agent 和相关示例项目可以正常运行，但尚未完成。请注意，
该 Agent 尚不符合我们的代码质量标准，也尚未经过全面测试。API
在正式首次发布之前不太可能发生变化。


### 功能

main() 会先初始化 TCP/IP 堆栈，然后启动 FreeRTOS 内核调度器。
有网络连接时，网络事件钩子可创建单项 RTOS 任务。该
任务可选择性创建多项其他任务，每项任务都会连接到
MQTT 代理，然后发送和接收各种不同大小
和不同服务质量 (QoS) 级别的 MQTT 数据包。原始线程
随后成为 MQTT Agent 线程。

以下[常量](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/configuration-files/demo_config.h)
用于定义创建的演示任务。描述中的链接指向注释，
这些注释位于每个实现源文件的顶部，可提供更多信息。

* **#define democonfigCREATE_LARGE_MESSAGE_SUB_PUB_TASK [1 或 0]**

  设置为 1 时，可创建
  运行在 [large_message_sub_pub_demo.c](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/demo-tasks/large_message_sub_pub_demo.c#L27) 中实现的 MQTT 演示的任务；
  设置为 0 时，可从构建中省略该任务。

* **#define democonfigNUM_SIMPLE_SUB_PUB_TASKS_TO_CREATE [n]**

  设置
  [simple_pub_sub_demo.c](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/demo-tasks/simple_sub_pub_demo.c) 中实现的任务要创建的实例数，
  该值可以为 0。

* **#define democonfigCREATE_CODE_SIGNING_OTA_DEMO [1 或 0]**

  设置为 1 时，可包括 [Over the Air (OTA) 更新功能](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/demo-tasks/ota_over_mqtt_demo.c#L30)；
  设置为 0 时，则忽略 OTA。我们提供[单独的页面](/Documentation/03-Libraries/07-Modular-over-the-air-updates/02-Demos/02-mqtt-ota-agent-orchestrator)，说明如何使用 OTA
  和该演示。

* **#define democonfigCREATE_DEFENDER_DEMO [1 或 0]**

  设置为 1 时，可生成 [AWS Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) 演示；设置为 0 时，则忽略此功能。有关
  Device Defender 演示的说明，请参阅[此处](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/03-Demo-with-MQTT-agent)。


### 获取源代码

[coreMQTT-Agent-Demos 存储库](https://github.com/FreeRTOS/coreMQTT-Agent-Demos)（位于 FreeRTOS GitHub 账号中）
演示了如何在 coreMQTT 上使用 Agent，还演示了如何
将其他 FreeRTOS 库以子模块形式纳入到项目中。请勿使用 GitHub 中的 "Download Zip" 链接来获取代码，
因为该 zip 文件不包括子模块化库。请改用以下 Git 命令将存储库
及其子模块克隆到本地计算机上：

使用 HTTPS 进行克隆：

```c
git clone https://github.com/FreeRTOS/coreMQTT-Agent-Demos.git --recurse-submodules
```

使用 SSH：

```c
git clone git@github.com:FreeRTOS/coreMQTT-Agent-Demos.git --recurse-submodules
```

如果下载存储库时未使用 --recurse-submodules 实参，则需运行：

```c
git submodule update --init --recursive
```

撰写本文时，项目使用的是
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
[FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) TCP/IP 堆栈，并使用
[Visual Studio 免费社区版](https://visualstudio.microsoft.com/vs/community/)构建。然而，
其目录结构经过精心编排，旨在将来针对其他开发工具添加项目。


### 源代码组织

Git 存储库的组织结构如下：

```c
+-build
|  |
|  +-VisualStudio  **Contains the Visual Studio project for this demo**
|
+-lib
|  |
|  +-AWS           **Contains a sub-module for the OTA library along with an OTA PAL port for Windows.**
|  +-FreeRTOS      **Contains sub-modules of the FreeRTOS libraries used by the demo**
|  +-ThirdParty    **Contains submodules of third party libraries used by the demo**
|
+-source
   |
   +-configuration-files    **Contains configuration files for the demo and libraries**
   +- .                     **Contains source files that implement the various demos**

```


### 配置 FreeRTOS-Plus-TCP

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，因此
请按照
为 [TCP/IP 入门项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)提供的说明操作
以确保您：

1. [安装了必备组件](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)（例如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)（可选）。

3. [设置了 MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr)（可选）。

4. [选择主机上的以太网接口](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)。

5. **最重要的是**，在尝试运行 MQTT 演示之前，[测试了网络连接](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test)。

每个演示项目都有自己的配置设置。当你按照网络配置说明进行操作时，
确保应用 MQTT 演示项目中的设置，而不是
TCP/IP 入门项目中的设置。默认情况下，TCP/IP 堆栈被配置为使用动态 IP 地址。


### 配置 MQTT 代理连接

MQTT Agent 可以本地或远程使用 TLS 或纯文本连接到任何 MQTT 代理
。非 Agent
[纯文本演示文档页面](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#option1)上的“配置 MQTT 代理”部分
详细介绍了一些本地和远程纯文本 MQTT 代理选项。服务器
[身份验证](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/02-coreMQTT-demo-LTS#configuration)和[相互身份验证](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection)页面上的“配置 MQTT 代理”部分
则详细介绍了一些 TLS 加密的 MQTT 代理选项。


**AWS IoT 用户其他注意事项：** 如果希望连接到 AWS IoT，
则可以创建必要的云端和设备端配置，
请按照记录单独相互身份验证演示的页面中“[使用 AWS IoT 消息代理](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection)”部分提供的说明进行操作
。该部分引用的脚本
可在 MQTT Agent 存储亏的 /lib/AWS/tools 目录中找到。

确定要连接到的代理之后，请参阅要点下方的代码片段，这些片段介绍了
配置 MQTT 连接的编译时配置常量。这些常量位于
/Source/configuration-files/demo_config.h 中。  请将 TLS 连接所需的所有密钥放置在同一文件中。


**重要提示：**

* 纯文本连接可用于了解 MQTT 的工作原理和调试连接，这是因为
  可以在 [WireShark](https://www.wireshark.org/) 等网络嗅探器中查看 MQTT 对话。
  但是，实际 IoT 设备不应使用未经加密的纯文本连接。切勿
  通过纯文本连接发送私人数据，强烈建议
  所有 IoT 设备使用经过加密和相互身份验证的连接。

* 将按键放在头文件中仅为方便演示。强烈建议
  实际设备将密钥存储在安全位置，如 Secure Element 或 Secure Enclave 中。
  此外，建议实际 IoT 设备通过不会泄露密钥的 API
  （例如 [PKCS #11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)
  或 [PSA](/Community/Blogs/2020/security-for-arm-cortex-m-devices-with-freertos) API）访问密钥和其他加密对象。


```c
/**
 * The MQTT client identifier used in this example. Each client identifier
 * must be unique so edit as required to ensure no two clients connecting to the
 * same broker use the same client identifier.
 *
 *!!! Please note a #defined constant is used for convenience of demonstration
 *!!! only. Production devices can use something unique to the device that can
 *!!! be read by software, such as a production serial number, instead of a
 *!!! hard coded constant.
 *
 * Below is an example only.
 */

#define democonfigCLIENT_IDENTIFIER    "Thing1"


/**
 * MQTT broker endpoint to connect to.
 *
 * This demo application can be run with any MQTT broker, although it is
 * recommended to use one that supports mutual authentication. If mutual
 * authentication is not used, then #democonfigUSE_TLS should be set to 0.
 *
 * Not for AWS users: Your AWS IoT Core endpoint can be found in the AWS IoT
 * console under Settings/Custom Endpoint, or using the describe-endpoint REST
 * API (with AWS CLI command line tool).
 *
 * #define democonfigMQTT_BROKER_ENDPOINT "insert here."
 *
 * Examples include:
 * #define democonfigMQTT_BROKER_ENDPOINT "test.mosquitto.org"
 * #define democonfigMQTT_BROKER_ENDPOINT "x-ats.iot.us-west-2.amazonaws.com"
 */

#define democonfigMQTT_BROKER_ENDPOINT   "192.168.0.100" /* Local broker */


/**
 * The TCP port to connect to.
 *
 * In general, port 8883 is for secured MQTT connections, and port 1883 if not
 * using TLS.
 *
 * #define democonfigMQTT_BROKER_PORT ( insert here. )
 *
 * Below is an example only.
 */

#define democonfigMQTT_BROKER_PORT ( 8883 )


/**
 * Whether to use mutual authentication. If this macro is not set to 1 or not
 * defined, then plaintext TCP will be used instead of TLS over TCP.
 */

#define democonfigUSE_TLS                   1

```


### MQTT Agent 配置常量

以下代码片段显示了与 MQTT Agent 相关的编译时常量，
及其默认值（在未定义的情况下）。MQTT Agent 没有自己的配置文件，
但会使用
[core_mqtt_config.h](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/configuration-files/core_mqtt_config.h) 中定义的任意宏。
该函数中定义的宏将替代默认值。

```c
/**
 * The maximum number of pending acknowledgments to track for a single
 * connection.
 *
 * The MQTT agent tracks MQTT commands (such as PUBLISH and SUBSCRIBE) that
 * are still waiting to be acknowledged. MQTT_AGENT_MAX_OUTSTANDING_ACKS set
 * the maximum number of acknowledgments that can be outstanding at any one time.
 * If this threshold is reached, packets will still be sent, but reported as failure.
 * The higher this number is the greater the agent’s RAM consumption will be.
 * Each entry uses up to 8 bytes on a 32-bit microprocessor.
 */

#ifndef MQTT_AGENT_MAX_OUTSTANDING_ACKS
    #define MQTT_AGENT_MAX_OUTSTANDING_ACKS               ( 20 )
#endif


/**
 * Time in MS that the MQTT agent task will wait in the Blocked state (so not
 * using any CPU time) for a command to arrive in its command queue before
 * exiting the blocked state so it can call MQTT_ProcessLoop().
 *
 * It is important MQTT_ProcessLoop() is called often if there is known MQTT
 * traffic, but calling it too often can take processing time away from lower
 * priority tasks and waste CPU time and power.
 */

#ifndef MQTT_AGENT_MAX_EVENT_QUEUE_WAIT_TIME
    #define MQTT_AGENT_MAX_EVENT_QUEUE_WAIT_TIME         ( 1000 )
#endif

```


## MQTT Agent API 使用示例

关于以下代码的重要提示：

1. 在 MQTT PUBLISH 得到 MQTT 代理的确认之前，
   MQTT PUBLISH 有效载荷和主题字符串必须保持有效。在下面的示例中，主题字符串是一个静态常量，
   因此无论如何都是有效的。

2. 在本示例中，调用 `MQTTAgent_Publish()` 的任务
   需等待收到服务器已确认 MQTT PUBLISH 命令的通知。任务可以选择性传递完成回调
   （该回调在收到确认后执行），但这一操作很有用，
   因为可发出信号，表明用于保存 MQTT 发布信息的缓冲区何时可以重用。

```c
/* Application defined structure that will get typedef'ed to CommandContext_t. */
struct CommandContext
{
    TaskHandle_t xTaskToNotify;
    MQTTStatus_t xReturnStatus;
};

static const char * const pcTopicName = "/my/topic/x";

/* The information associated with a single MQTT agent. Each agent context
 * holds the information for a single MQTT connection. This context must be
 * initialized with a call to MQTTAgent_Init() prior to its use. */
static MQTTAgentContext_t xAgentContext;


/* Callback executed when the MQTT PUBLISH is acknowledged by the MQTT broker. */
static void prvCommandCallback( void *pxCommandContext,
                                MQTTStatus_t xReturnStatus )
{
CommandContext_t *pxApplicationDefinedContext = ( CommandContext_t * ) pxCommandContext;

    /* Store the result in the application defined context and send a notification
       to the initiating task. Since this callback executes in the thread context of
       the MQTT agent task, the notification is necessary to signal the caller. */
    pxApplicationDefinedContext->xReturnStatus = xReturnStatus;

    xTaskNotify( pxApplicationDefinedContext->xTaskToNotify,
                 xReturnStatus,
                 eSetValueWithOverwrite );
}


void ExampleOfCallingAgentPublish( char *pcPayload, uint16_t usPayloadLength )
{
    MQTTPublishInfo_t xPublishInfo;
    /* The context for the completion callback must stay in scope until
     * the completion callback is invoked. In this example, using a stack variable
     * is safe because the function waits for the callback to execute before returning. */
    CommandContext_t xCommandContext;
    MQTTStatus_t xCommandAdded;
    BaseType_t xReturn;
    CommandInfo_t xCommandInformation;

    /* Complete an MQTTPublishInfo_t structure describing the publish operation.
       MQTTPublishInfo_t is defined by coreMQTT and is the same as would be passed
       into MQTT_Publish. */
    xPublishInfo.qos = MQTTQoS1;
    xPublishInfo.pTopicName = pcTopicName;
    xPublishInfo.topicNameLength = ( uint16_t ) strlen( pcTopicName );
    xPublishInfo.pPayload = pcPayload;
    xPublishInfo.payloadLength = usPayloadLength;

    /* Complete the CommandContext_t structure that will get passed into the
       callback that executes when the publish command is ACKed by the MQTT
       broker. The application writer defines this structure, and can put whatever
       they like in it. This simple example stores the handle of the calling task
       and provides a variable to store the status of the operation. See the
       implementation of prvCommandCallback() above. */
    xCommandContext.xTaskToNotify = [xTaskGetCurrentTaskHandle](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle)();


    /* Callback to execute the PUBLISH is acknowledged by the server. */
    xCommandInformation.cmdCompleteCallback = prvCommandCallback;

    /* The parameter to pass into the callback. In this case the parameter just
     * holds the handle of the task calling this function. */
    xCommandInformation.pCmdCompleteCallbackContext = &xCommandContext;

    /* Maximum time to wait enqueue the command for the agent. */
    xCommandInformation.blockTimeMs = mqttexampleMAX_COMMAND_SEND_BLOCK_TIME_MS;


    /* Send the command to the MQTT agent. */
    xCommandAdded = MQTTAgent_Publish( /* The MQTT context to use. */
                                       &xAgentContext,
                                       /* Structure that defined the MQTT PUBLISH
                                          operation. */
                                       &xPublishInfo,
                                       /* Command Information. */
                                       &xCommandInformation );

    if( xCommandAdded == MQTTSuccess )
    {
        /* The command was successfully sent to the agent. At this point the
           application writer can opt to wait for the callback to be executed,
           meaning the MQTT broker acknowledged the MQTT PUBLISH. Note the data
           pointed to by xPublishInfo.pTopicName and xPublishInfo.pPayload must
           remain valid (not be lost from a stack frame or overwritten in a buffer)
           until the PUBLISH is acknowledged. In this simple example the callback
           sends a notification to this task. */
        xReturn = xTaskNotifyWait( 0,
                                   0,
                                   NULL,
                                   portMAX_DELAY ); /* Wait indefinitely. */

        if( xReturn != pdFAIL )
        {
            /* The message was acknowledged and
               xCommandContext.xReturnStatus holds the result of the operation. */
        }
    }
}

```


## MQTT agent API

目前，MQTT Agent API 记录在
[mqtt_agent.h](https://github.com/FreeRTOS/coreMQTT-Agent/blob/d61dd0921bd651c0bfbaa2e41bb0eda56245a36b/source/include/mqtt_agent.h)
头文件和 [MQTT Agent API 引用文件](https://freertos.github.io/coreMQTT-Agent/)中。
