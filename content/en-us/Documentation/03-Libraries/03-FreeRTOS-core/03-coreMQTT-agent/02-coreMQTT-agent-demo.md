---
title: MQTT Agent and Demos using coreMQTT
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Including Over the Air ([OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)) updates

**NOTE**: This page is obsolete. Please use the thread safe [coreMQTT Agent Demo](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)
that uses the coreMQTT Agent instead.


* On this Page
    + [Implementation overview and usage model](#implementation-overview-and-usage-model)
    + [The MQTT agent demo project](#demo-project)

        - [Functionality](#functionality)
        - [Obtaining the source files](#obtaining-the-source-code)
        - [Source code organisation](#source-code-organisation)
        - [Configuring FreeRTOS-Plus-TCP](#configuring-freertos-plus-tcp)
        - [Configuring the MQTT broker connection](#configuring-the-mqtt-broker-connection)
        - [Configuring the MQTT agent](#mqtt-agent-configuration-constants)+ [Example of using the MQTT agent API](#example-of-using-the-mqtt-agent-api)
    + [MQTT agent API](#mqtt-agent-api)


## Introduction

coreMQTT is an MIT licensed open source C MQTT client library for microcontroller and small microprocessor
based IoT devices. Its design is intentionally simple to ensure it has no dependency on any other library
or operating system, and to better enable static analysis including memory safety proofs. That simplicity
and lack of operating system dependency (coreMQTT does not require multithreading at all) means coreMQTT
does not build thread safety directly into its implementation. Instead thread safety must be provided
by higher level software. This webpage demonstrates a coreMQTT extension that provides that higher level
functionality in the form of an MQTT agent (or MQTT daemon). While the implementation demonstrated here
is currently specific to FreeRTOS, there are not many dependencies on FreeRTOS, meaning the implementation
can easily be adapted for use with other operating systems.


## Implementation overview and usage model

The MQTT agent is an independent task (or thread of execution). It achieves thread safety very simply
be being the only task that is permitted to access the MQTT library's API. Isolating all MQTT API calls
to a single task serialises access, removing the need for semaphores or any other synchronisation primitives.

When using the agent, if an application task wants to perform an MQTT operation, for example publishing
a message, it calls the MQTT agent's MQTTAgent\_Publish() API instead of calling coreMQTT's MQTT\_Publish()
API. MQTTAgent\_Publish() packages the information required to complete the Publish operation into a
structure, then sends that structure over a queue to the MQTT agent task. The MQTT agent task receives
the structure, then it calls the underlying MQTT library's MQTT\_Publish() API on behalf of the application.

Each API that sends a command to the MQTT agent allows the application writer to optionally specify a
callback function, and a parameter to be passed into the callback (called the callback context), for
the agent to execute when the resultant MQTT operation completes. That way, the application task can
opt to enter the Blocked state (so not consuming any CPU time) to wait for the callback's execution,
or alternatively continue executing while the MQTT operation is in
process. [See the example](#example-of-using-the-mqtt-agent-api) at the end of this page.

Each API that sends a command to the MQTT agent also allows the application writer to specify the maximum
time the calling task should wait in the Blocked state for space to become available in the queue used
to send commands to the MQTT agent, should the queue be full at the time of the MQTT agent API call.
Again, [see the example](#example-of-using-the-mqtt-agent-api) at the end of this page.


## Demo project

### Preamble

**Note:** The MQTT agent and associated example project are functional but not yet complete. Be aware
the agent does not yet comply with our code quality standards and is not yet fully tested. The APIs are
unlikely to change before its official first release.


### Functionality

main() initialises the TCP/IP stack before starting the FreeRTOS kernel scheduler.
When the network connects, the network event hook creates a single RTOS task. That
task optionally creates multiple other tasks, each of which connects to the
MQTT broker before sending and receiving MQTT packets of various different size
and at various different Quality of Service (QoS) levels. The original thread
then becomes the MQTT agent thread.

The following [constants](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/configuration-files/demo_config.h)
define the created demo tasks. The links in the descriptions go to comments that provide more information at
the top of each implementing source file.

* **#define democonfigCREATE\_LARGE\_MESSAGE\_SUB\_PUB\_TASK [1 or 0]**

  Set to 1 to create the task that runs the MQTT demo implemented
  in [large\_message\_sub\_pub\_demo.c](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/demo-tasks/large_message_sub_pub_demo.c#L27),
  or 0 to omit that task from the build.

* **#define democonfigNUM\_SIMPLE\_SUB\_PUB\_TASKS\_TO\_CREATE [n]**

  Sets the number of instances to create of the task implemented
  in [simple\_pub\_sub\_demo.c](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/demo-tasks/simple_sub_pub_demo.c),
  which can be 0.

* **#define democonfigCREATE\_CODE\_SIGNING\_OTA\_DEMO [1 or 0]**

  Set to 1 to include [Over the Air (OTA) update functionality](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/demo-tasks/ota_over_mqtt_demo.c#L30),
  or 0 to omit OTA. There is a [separate page](/Documentation/03-Libraries/07-Modular-over-the-air-updates/02-Demos/02-mqtt-ota-agent-orchestrator) that describes using OTA
  with this demo.

* **#define democonfigCREATE\_DEFENDER\_DEMO [1 or 0]**

  Set to 1 to build the [AWS Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) demo, or 0 to omit. The
  instructions for the Device Defender demo can be found [here](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/03-Demo-with-MQTT-agent).


### Obtaining the source code

The [coreMQTT-Agent-Demos repository](https://github.com/FreeRTOS/coreMQTT-Agent-Demos) in the FreeRTOS
GitHub account demonstrates the use of an agent on top of coreMQTT. It also demonstrates how to submodule
other FreeRTOS libraries into a project. Do not use the "Download Zip" link in GitHub to obtain the code
as the zip file will not include the submoduled libraries. Instead use one of the following Git commands
to clone the repo and its submodules onto your local machine:

To clone using HTTPS:

```c
git clone https://github.com/FreeRTOS/coreMQTT-Agent-Demos.git --recurse-submodules
```

Using SSH:

```c
git clone git@github.com:FreeRTOS/coreMQTT-Agent-Demos.git --recurse-submodules
```

If you have downloaded the repo without using the --recurse-submodules argument, you need to run:

```c
git submodule update --init --recursive
```

At the time of writing the project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
the [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) TCP/IP stack, and builds using the
free [Community Edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/). Its directory
structure is however structured to enable the addition of projects for other development tools soon.


### Source code organisation

The git repo is organised as follows:

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


### Configuring FreeRTOS-Plus-TCP

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so
follow the instructions provided for
the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) to
ensure you:

1. Have the [pre-requisite components installed](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface) on your host machine.

5. …and **importantly** [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test) before attempting to run the MQTT demo.

Each demo project has its own configuration settings. When you are following the network
configuration instructions, make sure to apply the settings in the MQTT demo project, rather than
the TCP/IP starter project. By default the TCP/IP stack is configured to use a dynamic IP address.


### Configuring the MQTT broker connection

The MQTT agent can connect to any MQTT broker, either locally or remotely, and either using TLS or in
plain text. The Configuring an MQTT Broker section on the
non-agent [plain text demo documentation page](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#option1) details some local and
remote plain text MQTT broker options. The Configuration an MQTT Broker section on
the [server authentication](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/02-coreMQTT-demo-LTS#configuration) and [mutual authentication](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection) pages detail some TLS
encrypted MQTT broker options.


**Additional notes for AWS IoT users:** If you are going to connect to AWS IoT then you can create the
necessary cloud and device side configurations by following the instructions provided in
the [Using the AWS IoT Message Broker](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection) section
of the page that documents the separate mutual authentication demo. That section references scripts that
can be found in the /lib/AWS/tools directory of the MQTT Agent repository.

Once you have decided on the broker to connect to, the code snippet below the following bullet points
describes the compile time configuration constants that configure the MQTT connection. These constants are
in /Source/configuration-files/demo\_config.h.  Place any keys required for TLS connections in the same file.


**Important notes:**

* Plain text connections are useful to learn how MQTT works and to debug connections because
  the MQTT conversation can be viewed in a network sniffer such as [WireShark](https://www.wireshark.org/).
  However, real IoT devices should not use an unencrypted plain text connection. Never send private
  data over a plain text connection - we highly recommend using encrypted and mutually authenticated
  connections for all IoT devices.

* Placing keys in a header file is for convenience of demonstration only. We strongly recommend
  that real devices store keys in a secure location, such as a secure element or enclave.
  Further, we recommend real IoT devices access keys and other crypto objects via an API
  that does not expose the keys, such as [PKCS #11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)
  or [PSA](/Community/Blogs/2020/security-for-arm-cortex-m-devices-with-freertos) APIs.


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
 * authentication is not used, then #democonfigUSE\_TLS should be set to 0.
 *
 * Not for AWS users: Your AWS IoT Core endpoint can be found in the AWS IoT
 * console under Settings/Custom Endpoint, or using the describe-endpoint REST
 * API (with AWS CLI command line tool).
 *
 * #define democonfigMQTT\_BROKER\_ENDPOINT "insert here."
 *
 * Examples include:
 * #define democonfigMQTT\_BROKER\_ENDPOINT "test.mosquitto.org"
 * #define democonfigMQTT\_BROKER\_ENDPOINT "x-ats.iot.us-west-2.amazonaws.com"
 */

#define democonfigMQTT_BROKER_ENDPOINT   "192.168.0.100" /* Local broker */


/**
 * The TCP port to connect to.
 *
 * In general, port 8883 is for secured MQTT connections, and port 1883 if not
 * using TLS.
 *
 * #define democonfigMQTT\_BROKER\_PORT ( insert here. )
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


### MQTT agent configuration constants

The following code snippet shows the compile time constants relevant to the MQTT agent, along with their
default values should they be left undefined. The MQTT agent does not have its own configuration file,
but it will use any macros defined
in [core\_mqtt\_config.h](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/configuration-files/core_mqtt_config.h).
Macros defined there will be used in place of these defaults.

```c
/**
 * The maximum number of pending acknowledgments to track for a single
 * connection.
 *
 * The MQTT agent tracks MQTT commands (such as PUBLISH and SUBSCRIBE) that
 * are still waiting to be acknowledged. MQTT\_AGENT\_MAX\_OUTSTANDING\_ACKS set
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
 * exiting the blocked state so it can call MQTT\_ProcessLoop().
 *
 * It is important MQTT\_ProcessLoop() is called often if there is known MQTT
 * traffic, but calling it too often can take processing time away from lower
 * priority tasks and waste CPU time and power.
 */

#ifndef MQTT_AGENT_MAX_EVENT_QUEUE_WAIT_TIME
    #define MQTT_AGENT_MAX_EVENT_QUEUE_WAIT_TIME         ( 1000 )
#endif
```


## Example of using the MQTT agent API

Important notes on the following code:

1. The MQTT PUBLISH payload and topic string must remain valid until the MQTT PUBLISH has been acknowledged
   by the MQTT broker. In the example below the topic string is a static const, so it will always be valid
   anyway.

2. In this example the task that calls `MQTTAgent_Publish()` waits to be notified that the MQTT PUBLISH
   command has been acknowledged by the server. It is optional for the task to pass the completion callback
   which executes upon receipt of the acknowledgment, but it is useful as it also signals when the buffers
   used to hold the MQTT publish information can be reused.

```c
/* Application defined structure that will get typedef'ed to CommandContext\_t. */
struct CommandContext
{
    TaskHandle_t xTaskToNotify;
    MQTTStatus_t xReturnStatus;
};

static const char * const pcTopicName = "/my/topic/x";

/* The information associated with a single MQTT agent. Each agent context
 * holds the information for a single MQTT connection. This context must be
 * initialized with a call to MQTTAgent\_Init() prior to its use. */
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

    /* Complete an MQTTPublishInfo\_t structure describing the publish operation.
       MQTTPublishInfo\_t is defined by coreMQTT and is the same as would be passed
       into MQTT\_Publish. */
    xPublishInfo.qos = MQTTQoS1;
    xPublishInfo.pTopicName = pcTopicName;
    xPublishInfo.topicNameLength = ( uint16_t ) strlen( pcTopicName );
    xPublishInfo.pPayload = pcPayload;
    xPublishInfo.payloadLength = usPayloadLength;

    /* Complete the CommandContext\_t structure that will get passed into the
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

At this time the MQTT agent API is documented in
the [mqtt\_agent.h](https://github.com/FreeRTOS/coreMQTT-Agent/blob/d61dd0921bd651c0bfbaa2e41bb0eda56245a36b/source/include/mqtt_agent.h)
header file and at the [MQTT agent API References](https://freertos.github.io/coreMQTT-Agent/).
