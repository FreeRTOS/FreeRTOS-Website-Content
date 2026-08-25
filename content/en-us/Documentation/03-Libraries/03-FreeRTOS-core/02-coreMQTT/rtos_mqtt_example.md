---
title: coreMQTT Basic Multithreaded Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**Note: We recommend to always use mutual authentication in building any Internet of Things (IoT) application.
The demo on this page is only meant for educational purposes and demonstrates MQTT communication prior to
introducing encryption and authentication. It is not intended to be suitable for production use.**


## Single Threaded Vs Multi Threaded

There are two coreMQTT usage models, *single threaded* and *multithreaded* (multitasking). The demo
documented on this page provides an example of creating your own multithreading scheme. There is also
a multithreaded example that instead executes the MQTT protocol in the background
within [an agent (or daemon) task](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo). Executing the MQTT protocol in an agent task removes
the need for the application writer to explicitly manage any MQTT state or call the `MQTT_ProcessLoop()`
API function. Using an agent task also enables multiple application tasks to share a single MQTT connection
without the need for synchronization primitives such as mutexes.


## Demo introduction

The coreMQTT Basic Multithreaded demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so you can build and evaluate it with
the [free Community version of Visual Studios](https://visualstudio.microsoft.com/vs/community/) on
Windows, without the need for any particular MCU hardware.

This demo uses a thread safe queue to hold commands for interacting with the MQTT API. There are four
tasks to note in this demo:

* A command (main) task processes the commands from the command queue while the other tasks enqueue
  them. This task enters a loop, during which it processes commands from the command queue. If a termination
  command is received, it will break out of the loop.

* A synchronous publisher task creates a series of publish operations which it pushes to the command
  queue, which are then executed by the command task. This task uses synchronous publishing, which means it
  will wait for each publish operation to complete before scheduling the next one.

* An asynchronous publisher task creates a series of publish operations which it pushes to the command
  queue, which are then executed by the command task. The difference between this task and the previous
  one is that it will not wait for a publish operation to complete before scheduling the next publish
  operation, and it checks the status of each after all publish operations have been enqueued. Note that
  the distinction between synchronous and asynchronous publishing is only in the behavior of the task,
  not in the actual publish command.

* A subscriber task creates an MQTT subscription to a topic filter that matches the topics of all messages
  which the publisher tasks publish. It loops, waiting to receive back the messages published by the other
  tasks.

Tasks can have queues to hold received messages, and the command task will push incoming messages to the
queue of each task that is subscribed to the incoming topic.

The basic Multithreaded demo can be configured to use either a TLS connection with mutual authentication,
or a plaintext TCP connection. By default, the demo uses TLS. If the network unexpectedly disconnects
during the demo, then the client will attempt to reconnect with exponential backoff logic. Additionally,
if the reconnection succeeds, but the broker cannot resume the prior session, then the client will resubscribe
to the previously subscribed topics.


## Source Code Organization

The Visual Studio solution for the Multithreaded MQTT demo is
called [`mqtt_multitask_demo.sln`](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Multitask/mqtt_multitask_demo.sln)
and is located in
the [/FreeRTOS-Plus/Demo/coreMQTT\_Windows\_Simulator/MQTT\_Multitask](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Multitask)
directory of the [main FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) download.


[![](/media/2020/coreMQTT-Source-Code-Organization.png)](/media/2020/coreMQTT-Source-Code-Organization.png)
*Click to enlarge*


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:

1. Open the '`mqtt_multitask_demo.sln`' Visual Studio solution file from within the Visual Studio IDE.

2. Select '`Build Solution`' from the IDE's '`Build`' menu.

**Note**: If you are using Microsoft Visual Studio 2017 or earlier, then you must select a '`Platform
Toolset`' compatible with your version: '`Project -> RTOSDemos Properties -> Platform Toolset`'.


## Configuring the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so
follow the instructions provided for
the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) to ensure
you:

1. Have the [pre-requisite components installed](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
   (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   on your host machine.

5. ...and **importantly** [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test)
   before attempting to run the MQTT demo.

All of these settings should be changed in the MQTT LTS rc1 demo project, not the TCP/IP starter project
referred to in the pages linked to above! As delivered, the TCP/IP stack is configured to use a dynamic
IP address.


## Configuring the MQTT Broker Connection

### Option 1: TLS with Mutual Authentication (default):

This demo supports the same configuration options as the [MQTT Mutual Auth](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)
demo. Please see that demo's documentation for all of the available options.


### Option 2: Plaintext:

To enable quick setup with no certificate configuration required, the basic Multithreaded demo allows
plaintext TCP connections to be used in lieu of mutually authenticated TLS. To disable TLS, The
macro '`democonfigUSE_TLS`' should be set to `0` in '`demo_config`', or simply not defined at all. Then,
the demo may be used with any unencrypted MQTT broker (for example, Eclipse Mosquitto) by following the
same instructions as the [Plaintext demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo).


## Functionality

The demo creates four tasks in total: three that request MQTT API calls, and one that processes those
requests (the primary task). In this demo, the primary task loops through creating the three subtasks,
calling the processing loop, and cleaning up afterwards. This primary task creates a single MQTT connection
to the broker that is then shared among the subtasks. Two of the tasks publish messages to the broker, and
the third receives the messages back using an MQTT subscription to a topic filter that matches all of
those published.


## Typedefs

The demo defines the following structures, enums, and function pointers:


**Commands**

Rather than making the MQTT API calls directly, the tasks use '`Command_t`' structures to create commands
that instruct the main task to call the appropriate API for them. Commands may be of type '`PROCESSLOOP`',
'`PUBLISH`', '`SUBSCRIBE`', '`UNSUBSCRIBE`', '`PING`', '`DISCONNECT`', '`RECONNECT`', or '`TERMINATE`'.
The '`TERMINATE`' command does not have a corresponding MQTT API; it is used in the demo to instruct the
main task to stop processing commands and begin cleanup operations. Because some additional information (for
example, publish or subscribe info) is required for some MQTT commands ('`MQTT_Publish`', '`MQTT_Subscribe`',
and '`MQTT_Unsubscribe`') we use the '`CommandContext_t`' field. This field is required for those three
commands just mentioned, but optional for the others.

Since this context is required for these commands, it MUST NOT be changed once the command has been
enqueued, and until the command has completed. When a command completes, an optional callback may be invoked.
In this demo, we use a callback that creates a task notification to inform the calling task that the command
has completed. For MQTT operations that require acknowledgments (subscribes, unsubscribes, and publishes with
QoS greater than 0), the command is considered completed once the acknowledgment has been received. Otherwise,
the command is completed once the corresponding MQTT API call has returned.

```c
/**
 * @brief A command for interacting with the MQTT API.
 */
typedef struct Command
{
    CommandType_t xCommandType;
    CommandContext_t * pxCmdContext;
    CommandCallback_t vCallback;
} Command_t;
```

```c
/**
 * @brief Struct containing context for a specific command.
 *
 * @note An instance of this struct and any variables it points to MUST stay
 * in scope until the associated command is processed, and its callback called.
 * The command callback will set the `xIsComplete` flag, and notify the calling task.
 */
typedef struct CommandContext
{
    MQTTPublishInfo_t * pxPublishInfo;
    MQTTSubscribeInfo_t * pxSubscribeInfo;
    size_t ulSubscriptionCount;
    MQTTStatus_t xReturnStatus;
    bool xIsComplete;

    /* The below fields are specific to this FreeRTOS implementation. */
    TaskHandle_t xTaskToNotify;
    uint32_t ulNotificationBit;
    QueueHandle_t pxResponseQueue;
} CommandContext_t;
```

```c
/**
 * @brief A type of command for interacting with the MQTT API.
 */
typedef enum CommandType
{
    PROCESSLOOP, /**< @brief Call MQTT_ProcessLoop(). */
    PUBLISH,     /**< @brief Call MQTT_Publish(). */
    SUBSCRIBE,   /**< @brief Call MQTT_Subscribe(). */
    UNSUBSCRIBE, /**< @brief Call MQTT_Unsubscribe(). */
    PING,        /**< @brief Call MQTT_Ping(). */
    DISCONNECT,  /**< @brief Call MQTT_Disconnect(). */
    RECONNECT,   /**< @brief Reconnect a broken connection. */
    TERMINATE    /**< @brief Exit the command loop and stop processing commands. */
} CommandType_t;
```

```c
/**
 * @brief Callback function called when a command completes.
 */
typedef void (* CommandCallback_t )( CommandContext_t * );
```

**Acknowledgments**

As some MQTT operations require an acknowledgment, an array of '`AckInfo_t`' is used that contains the
packet identifier of the expected acknowledgment, and the original command that is expecting it (so that
its completion callback may be invoked).

```c
typedef struct ackInfo
{
    uint16_t usPacketId;
    Command_t xOriginalCommand;
} AckInfo_t;
```

**Subscriptions**

This demo is able to track subscriptions for each task. In order to do so, each task that requests a
subscription must provide a message queue where it will receive back the published messages. Multiple
tasks may subscribe to the same topic filter, as they are expected to use separate response queues.

```c
/**
 * @brief An element in the list of subscriptions maintained in the demo.
 *
 * @note This demo allows multiple tasks to subscribe to the same topic.
 * In this case, another element is added to the subscription list, differing
 * in the destination response queue.
 */
typedef struct subscriptionElement
{
    char pcSubscriptionFilter[ mqttexampleDEMO_BUFFER_SIZE ];
    uint16_t usFilterLength;
    QueueHandle_t pxResponseQueue;
} SubscriptionElement_t;
```


**Received Published Messages**

Since tasks execute in parallel with the main task, it would be difficult and time consuming for the main task to have to
wait for each subscribed task to read a received published message. Therefore, each message received is copied to the response
queue of any task subscribed to the published message's topic. Since publish packets received from the MQTT client contain
pointers to the client's network buffer, the payload and topic name of the incoming message are copied into separate buffers
before insertion into a response queue. This way, the subscribed task may still read the received information after the MQTT
client has cleared its network buffer.

```c
/**
 * @brief An element for a task's response queue for received publishes.
 *
 * @note Since elements are copied to queues, this struct needs to hold
 * buffers for the payload and topic of incoming publishes, as the original
 * pointers are out of scope. When processing a publish from this struct,
 * the `pcTopicNameBuf` and `pcPayloadBuf` pointers need to be set to point to the
 * static buffers in this struct.
 */
typedef struct publishElement
{
    MQTTPublishInfo_t xPublishInfo;
    uint8_t pcPayloadBuf[ mqttexampleDEMO_BUFFER_SIZE ];
    uint8_t pcTopicNameBuf[ mqttexampleDEMO_BUFFER_SIZE ];
} PublishElement_t;
```

## Main Task

The main application task establishes a persistent MQTT session, creates three subtasks, and executes the processing loop
until a termination command is received. A persistent session is used, so if the network unexpectedly disconnects, the demo
will reconnect to the broker in the background, without losing subscriptions or any incoming published messages from the
broker. In order to create a new persistent session for every run, the demo connects to the broker with the "clean session"
flag set, then disconnects and reconnects with the flag unset. After the processing loop has terminated, it disconnects from
the broker, and loops again from the network reconnection. The structure of the main task is shown here:

```c
static void prvMQTTDemoTask( void * pvParameters )
{
    BaseType_t xNetworkStatus = pdFAIL;
    MQTTStatus_t xMQTTStatus;
    BaseType_t xResult = pdFALSE;
    uint32_t ulNotification = 0;
    uint32_t ulExpectedNotifications = mqttexamplePUBLISHER_SYNC_COMPLETE_BIT |
                                       mqttexampleSUBSCRIBE_TASK_COMPLETE_BIT |
                                       mqttexamplePUBLISHER_ASYNC_COMPLETE_BIT;

    ( void ) pvParameters;

    ulGlobalEntryTimeMs = prvGetTimeMs();

    /* Create command queue for processing MQTT commands. */
    xCommandQueue = xQueueCreate( mqttexampleCOMMAND_QUEUE_SIZE, sizeof( Command_t ) );
    /* Create response queues for each task. */
    xSubscriberResponseQueue = xQueueCreate( mqttexamplePUBLISH_QUEUE_SIZE, sizeof( PublishElement_t ) );

    /* In this demo, send publishes on non-subscribed topics to this queue.
     * Note that this value is not meant to be changed after `prvCommandLoop` has
     * been called, since access to this variable is not protected by thread
     * synchronization primitives. */
    xDefaultResponseQueue = xQueueCreate( 1, sizeof( PublishElement_t ) );

    /* This demo uses a persistent session that can be re-connected if disconnected.
     * Clean any lingering sessions that may exist from previous executions of the
     * demo. */
    prvCleanExistingPersistentSession();

    for( ; ; )
    {
        /* Clear the lists of subscriptions and pending acknowledgments. */
        memset( pxPendingAcks, 0x00, mqttexamplePENDING_ACKS_MAX_SIZE * sizeof( AckInfo_t ) );
        memset( pxSubscriptions, 0x00, mqttexampleSUBSCRIPTIONS_MAX_COUNT * sizeof( SubscriptionElement_t ) );

        /* Connect to the broker. */
        xNetworkStatus = prvSocketConnect( &xNetworkContext );
        configASSERT( xNetworkStatus == pdPASS );
        /* Form an MQTT connection with a persistent session. */
        xMQTTStatus = prvMQTTConnect( &globalMqttContext, false );
        configASSERT( xMQTTStatus == MQTTSuccess );
        configASSERT( globalMqttContext.connectStatus == MQTTConnected );

        /* Give subscriber task higher priority so the subscribe will be processed before the first publish.
         * This must be less than or equal to the priority of the main task. */
        xResult = xTaskCreate( prvSubscribeTask, "Subscriber", democonfigDEMO_STACKSIZE, NULL, tskIDLE_PRIORITY + 1, &xSubscribeTask );
        configASSERT( xResult == pdPASS );
        xResult = xTaskCreate( prvSyncPublishTask, "SyncPublisher", democonfigDEMO_STACKSIZE, NULL, tskIDLE_PRIORITY, &xSyncPublisherTask );
        configASSERT( xResult == pdPASS );
        xResult = xTaskCreate( prvAsyncPublishTask, "AsyncPublisher", democonfigDEMO_STACKSIZE, NULL, tskIDLE_PRIORITY, &xAsyncPublisherTask );
        configASSERT( xResult == pdPASS );

        LogInfo( ( "Running command loop" ) );
        prvCommandLoop();

        /* Delete created queues. Wait for tasks to exit before cleaning up. */
        LogInfo( ( "Waiting for tasks to exit." ) );
        ( void ) prvNotificationWaitLoop( &ulNotification, ulExpectedNotifications, false );

        configASSERT( ( ulNotification & ulExpectedNotifications ) == ulExpectedNotifications );

        /* Reset queues. */
        xQueueReset( xCommandQueue );
        xQueueReset( xDefaultResponseQueue );
        xQueueReset( xSubscriberResponseQueue );

        /* Clear task notifications. */
        ulNotification = ulTaskNotifyValueClear( NULL, ~( 0U ) );

        /* Disconnect. */
        xNetworkStatus = prvSocketDisconnect( &xNetworkContext );
        configASSERT( xNetworkStatus == pdPASS );

        LogInfo( ( "\r\n\r\nprvMQTTDemoTask() completed an iteration successfully. Total free heap is %u.\r\n", xPortGetFreeHeapSize() ) );
        LogInfo( ( "Demo completed successfully.\r\n" ) );
        LogInfo( ( "Short delay before starting the next iteration.... \r\n\r\n" ) );
        vTaskDelay( mqttexampleDELAY_BETWEEN_DEMO_ITERATIONS );
    }
}
```

[![](/media/2020/Screen-Shot-2020-10-30-at-5.51.54-AM.png)](/media/2020/Screen-Shot-2020-10-30-at-5.51.54-AM.png)
Click to enlarge


**Command loop**

The command loop waits for commands to be enqueued, and then calls the appropriate MQTT API. Note that all commands except
for '`DISCONNECT`' and '`TERMINATE`' will result in '`MQTT_ProcessLoop`' being called as well.
This demo sets a socket wakeup callback to add a '`PROCESSLOOP`' command to the queue when data is available on the
socket. However, there may be many commands ahead of it in the queue at that point. So, to ensure that we do not neglect
incoming data while other commands are processed, '`MQTT_ProcessLoop`' is called for a single iteration after each
command.

```c
static void prvCommandLoop( void )
{
    Command_t xCommand;
    Command_t xNewCommand;
    MQTTStatus_t xStatus = MQTTSuccess;
    static int lNumProcessed = 0;
    bool xTerminateReceived = false;
    BaseType_t xCommandAdded = pdTRUE;

    /* Loop until we receive a terminate command. */
    for( ; ; )
    {
        /* If there is no command in the queue, try again. */
        if( xQueueReceive( xCommandQueue, &xCommand, mqttexampleDEMO_TICKS_TO_WAIT ) == pdFALSE )
        {
            LogInfo( ( "No commands in the queue. Trying again." ) );
            continue;
        }

        xStatus = prvProcessCommand( &xCommand );

        /* Add connect operation to front of queue if status was not successful. */
        if( xStatus != MQTTSuccess )
        {
            LogError( ( "MQTT operation failed with status %s\n",
                        MQTT_Status_strerror( xStatus ) ) );
            prvCreateCommand( RECONNECT, NULL, NULL, &xNewCommand );
            xCommandAdded = xQueueSendToFront( xCommandQueue, &xNewCommand, mqttexampleDEMO_TICKS_TO_WAIT );
            /* Ensure the command was added to the queue. */
            configASSERT( xCommandAdded == pdTRUE );
        }

        /* Keep a count of processed operations, for debug logs. */
        lNumProcessed++;

        /* Delay after sending a subscribe. This is to so that the broker
         * creates a subscription for us before processing our next publish,
         * which should be immediately after this. */
        if( xCommand.xCommandType == SUBSCRIBE )
        {
            LogDebug( ( "Sleeping for %d ms after sending SUBSCRIBE packet.", mqttexampleSUBSCRIBE_TASK_DELAY_MS ) );
            vTaskDelay( mqttexampleSUBSCRIBE_TASK_DELAY_MS );
        }

        /* Terminate the loop if we receive the termination command. */
        if( xCommand.xCommandType == TERMINATE )
        {
            xTerminateReceived = true;
            break;
        }

        LogDebug( ( "Processed %d operations.", lNumProcessed ) );
    }

    /* Make sure we exited the loop due to receiving a terminate command and not
     * due to the queue being empty. */
    configASSERT( xTerminateReceived == true );

    LogInfo( ( "Creating Disconnect operation." ) );
    MQTT_Disconnect( &globalMqttContext );
    LogInfo( ( "Disconnected from broker." ) );
}
```


**Processing commands**

```c
static MQTTStatus_t prvProcessCommand( Command_t * pxCommand )
{
    MQTTStatus_t xStatus = MQTTSuccess;
    uint16_t usPacketId = MQTT_PACKET_ID_INVALID;
    bool xAddAckToList = false, xAckAdded = false;
    BaseType_t xNetworkResult = pdFAIL;
    MQTTPublishInfo_t * pxPublishInfo;
    MQTTSubscribeInfo_t * pxSubscribeInfo;

    switch( pxCommand->xCommandType )
    {
        case PROCESSLOOP:

            /* The process loop will run at the end of every command, so we don't
             * need to call it again here. */
            LogDebug( ( "Running Process Loop." ) );
            break;

        case PUBLISH:
            configASSERT( pxCommand->pxCmdContext != NULL );
            pxPublishInfo = pxCommand->pxCmdContext->pxPublishInfo;
            configASSERT( pxPublishInfo != NULL );

            if( pxPublishInfo->qos != MQTTQoS0 )
            {
                usPacketId = MQTT_GetPacketId( &globalMqttContext );
            }

            LogDebug( ( "Publishing message to %.*s.", ( int ) pxPublishInfo->topicNameLength, pxPublishInfo->pTopicName ) );
            xStatus = MQTT_Publish( &globalMqttContext, pxPublishInfo, usPacketId );
            pxCommand->pxCmdContext->xReturnStatus = xStatus;

            /* Add to pending ack list, or call callback if QoS 0. */
            xAddAckToList = ( pxPublishInfo->qos != MQTTQoS0 ) && ( xStatus == MQTTSuccess );
            break;

        case SUBSCRIBE:
        case UNSUBSCRIBE:
            configASSERT( pxCommand->pxCmdContext != NULL );
            pxSubscribeInfo = pxCommand->pxCmdContext->pxSubscribeInfo;
            configASSERT( pxSubscribeInfo != NULL );
            configASSERT( pxSubscribeInfo->pTopicFilter != NULL );
            usPacketId = MQTT_GetPacketId( &globalMqttContext );

            if( pxCommand->xCommandType == SUBSCRIBE )
            {
                /* Even if some subscriptions already exist in the subscription list,
                 * it is fine to send another subscription request. A valid use case
                 * for this is changing the maximum QoS of the subscription. */
                xStatus = MQTT_Subscribe( &globalMqttContext,
                                          pxSubscribeInfo,
                                          pxCommand->pxCmdContext->ulSubscriptionCount,
                                          usPacketId );
            }
            else
            {
                xStatus = MQTT_Unsubscribe( &globalMqttContext,
                                            pxSubscribeInfo,
                                            pxCommand->pxCmdContext->ulSubscriptionCount,
                                            usPacketId );
            }

            pxCommand->pxCmdContext->xReturnStatus = xStatus;
            xAddAckToList = ( xStatus == MQTTSuccess );
            break;

        case PING:
            xStatus = MQTT_Ping( &globalMqttContext );

            if( pxCommand->pxCmdContext != NULL )
            {
                pxCommand->pxCmdContext->xReturnStatus = xStatus;
            }
            break;

        case DISCONNECT:
            xStatus = MQTT_Disconnect( &globalMqttContext );

            if( pxCommand->pxCmdContext != NULL )
            {
                pxCommand->pxCmdContext->xReturnStatus = xStatus;
            }
            break;

        case RECONNECT:
            /* Reconnect TCP. */
            xNetworkResult = prvSocketDisconnect( &xNetworkContext );
            configASSERT( xNetworkResult == pdPASS );
            xNetworkResult = prvSocketConnect( &xNetworkContext );
            configASSERT( xNetworkResult == pdPASS );

            /* MQTT Connect with a persistent session. */
            xStatus = prvMQTTConnect( &globalMqttContext, false );
            break;

        case TERMINATE:
            LogInfo( ( "Terminating command loop." ) );

        default:
            break;
    }

    if( xAddAckToList )
    {
        xAckAdded = prvAddAwaitingOperation( usPacketId, pxCommand );

        /* Set the return status if no memory was available to store the operation
         * information. */
        if( !xAckAdded )
        {
            LogError( ( "No memory to wait for acknowledgment for packet %u\n", usPacketId ) );

            /* All operations that can wait for acks (publish, subscribe, unsubscribe)
             * require a context. */
            configASSERT( pxCommand->pxCmdContext != NULL );
            pxCommand->pxCmdContext->xReturnStatus = MQTTNoMemory;
        }
    }

    if( !xAckAdded )
    {
        /* The command is complete, call the callback. */
        if( pxCommand->vCallback != NULL )
        {
            pxCommand->vCallback( pxCommand->pxCmdContext );
        }
    }

    /* Run a single iteration of the process loop if there were no errors and
     * the MQTT connection still exists. */
    if( ( xStatus == MQTTSuccess ) && ( globalMqttContext.connectStatus == MQTTConnected ) )
    {
        xStatus = MQTT_ProcessLoop( &globalMqttContext, mqttexamplePROCESS_LOOP_TIMEOUT_MS );
    }

    return xStatus;
}
```


## Synchronous Publisher Task

The synchronous publisher task creates '`PUBLISH`' operations synchronously, waiting for each operation to
complete before scheduling the next one. This demo uses QoS 1 to publish messages, which means that these operations are not
considered completed until the publish acknowledgment packet has been received.

```c
void prvSyncPublishTask( void * pvParameters )
{
    ( void ) pvParameters;
    Command_t xCommand;
    MQTTPublishInfo_t xPublishInfo = { 0 };
    char payloadBuf[ mqttexampleDEMO_BUFFER_SIZE ];
    char topicBuf[ mqttexampleDEMO_BUFFER_SIZE ];
    CommandContext_t xContext;
    uint32_t ulNotification = 0U;
    BaseType_t xCommandAdded = pdTRUE;

    /* We use QoS 1 so that the operation won't be counted as complete until we
     * receive the publish acknowledgment. */
    xPublishInfo.qos = MQTTQoS1;
    xPublishInfo.pTopicName = topicBuf;
    xPublishInfo.pPayload = payloadBuf;

    /* Synchronous publishes. In case mqttexamplePUBLISH\_COUNT is odd, round up. */
    for( int i = 0; i < ( ( mqttexamplePUBLISH_COUNT + 1 ) / 2 ); i++ )
    {
        snprintf( payloadBuf, mqttexampleDEMO_BUFFER_SIZE, mqttexamplePUBLISH_PAYLOAD_FORMAT, "Sync", i + 1 );
        xPublishInfo.payloadLength = ( uint16_t ) strlen( payloadBuf );
        snprintf( topicBuf, mqttexampleDEMO_BUFFER_SIZE, mqttexamplePUBLISH_TOPIC_FORMAT_STRING, "sync", i + 1 );
        xPublishInfo.topicNameLength = ( uint16_t ) strlen( topicBuf );

        memset( ( void * ) &xContext, 0x00, sizeof( &xContext ) );
        xContext.xTaskToNotify = xTaskGetCurrentTaskHandle();
        xContext.ulNotificationBit = 1 << i;
        xContext.pxPublishInfo = &xPublishInfo;
        LogInfo( ( "Adding publish operation for message %s \non topic %.*s", payloadBuf, xPublishInfo.topicNameLength, xPublishInfo.pTopicName ) );
        prvCreateCommand( PUBLISH, &xContext, prvCommandCallback, &xCommand );
        xCommandAdded = prvAddCommandToQueue( &xCommand );
        /* Ensure command was added to queue. */
        configASSERT( xCommandAdded == pdTRUE );
        LogInfo( ( "Waiting for publish %d to complete.", i + 1 ) );

        if( prvNotificationWaitLoop( &ulNotification, ( 1U << i ), true ) != true )
        {
            LogError( ( "Synchronous publish loop iteration %d"
                        " exceeded maximum wait time.\n", ( i + 1 ) ) );
        }

        configASSERT( ( ulNotification & ( 1U << i ) ) == ( 1U << i ) );

        LogInfo( ( "Publish operation complete. Sleeping for %d ms.\n", mqttexamplePUBLISH_DELAY_SYNC_MS ) );
        vTaskDelay( pdMS_TO_TICKS( mqttexamplePUBLISH_DELAY_SYNC_MS ) );
    }

    LogInfo( ( "Finished sync publishes.\n" ) );

    /* Clear this task's notifications. */
    xTaskNotifyStateClear( NULL );
    ulNotification = ulTaskNotifyValueClear( NULL, ~( 0U ) );

    /* Notify main task this task has completed. */
    xTaskNotify( xMainTask, mqttexamplePUBLISHER_SYNC_COMPLETE_BIT, eSetBits );

    /* Delete this task. */
    LogInfo( ( "Deleting Sync Publisher task." ) );
    vTaskDelete( NULL );
}
```


## Asynchronous Publisher Task

The asynchronous publisher does not wait for a publish to complete before it enqueues the next one. This demonstrates that
a task does not need to wait for an MQTT operation to complete before it resumes execution. Instead, it waits only when
necessary. Because each publish command requires its own context struct, this task cannot reuse a single context structure
as the synchronous publisher task does, as a previous command may still need it. Therefore, it allocates memory for each
context structure, and then waits to free all allocated memory after all messages to be published have been enqueued.

```c
void prvAsyncPublishTask( void * pvParameters )
{
    ( void ) pvParameters;
    Command_t xCommand;
    MQTTPublishInfo_t pxPublishes[ mqttexamplePUBLISH_COUNT / 2 ];
    uint32_t ulNotification = 0U;
    uint32_t ulExpectedNotifications = 0U;
    BaseType_t xCommandAdded = pdTRUE;

    /* The following arrays are used to hold pointers to dynamically allocated memory. */
    char * payloadBuffers[ mqttexamplePUBLISH_COUNT / 2 ];
    char * topicBuffers[ mqttexamplePUBLISH_COUNT / 2 ];
    CommandContext_t * pxContexts[ mqttexamplePUBLISH_COUNT / 2 ] = { 0 };

    /* Add a delay. The main task will not be sending publishes for this interval
     * anyway, as we want to give the broker ample time to process the
     * subscription. */
    vTaskDelay( mqttexampleSUBSCRIBE_TASK_DELAY_MS );

    /* Asynchronous publishes. Although not necessary, we use dynamic
     * memory here to avoid declaring many static buffers. */
    for( int i = 0; i < mqttexamplePUBLISH_COUNT / 2; i++ )
    {
        pxContexts[ i ] = ( CommandContext_t * ) pvPortMalloc( sizeof( CommandContext_t ) );
        memset( ( void * ) pxContexts[ i ], 0x00, sizeof( CommandContext_t ) );
        pxContexts[ i ]->xTaskToNotify = xTaskGetCurrentTaskHandle();

        /* Set the notification bit to be the publish number. This prevents this demo
         * from having more than 32 publishes. If many publishes are desired, semaphores
         * can be used instead of task notifications. */
        pxContexts[ i ]->ulNotificationBit = 1U << i;
        ulExpectedNotifications |= 1U << i;
        payloadBuffers[ i ] = ( char * ) pvPortMalloc( mqttexampleDYNAMIC_BUFFER_SIZE );
        topicBuffers[ i ] = ( char * ) pvPortMalloc( mqttexampleDYNAMIC_BUFFER_SIZE );
        snprintf( payloadBuffers[ i ], mqttexampleDYNAMIC_BUFFER_SIZE, mqttexamplePUBLISH_PAYLOAD_FORMAT, "Async", i + 1 );
        snprintf( topicBuffers[ i ], mqttexampleDYNAMIC_BUFFER_SIZE, mqttexamplePUBLISH_TOPIC_FORMAT_STRING, "async", i + 1 );

        /* Set publish info. */
        memset( &( pxPublishes[ i ] ), 0x00, sizeof( MQTTPublishInfo_t ) );
        pxPublishes[ i ].pPayload = payloadBuffers[ i ];
        pxPublishes[ i ].payloadLength = strlen( payloadBuffers[ i ] );
        pxPublishes[ i ].pTopicName = topicBuffers[ i ];
        pxPublishes[ i ].topicNameLength = ( uint16_t ) strlen( topicBuffers[ i ] );
        pxPublishes[ i ].qos = MQTTQoS1;
        pxContexts[ i ]->pxPublishInfo = &( pxPublishes[ i ] );
        LogInfo( ( "Adding publish operation for message %s \non topic %.*s",
                   payloadBuffers[ i ],
                   pxPublishes[ i ].topicNameLength,
                   pxPublishes[ i ].pTopicName ) );
        prvCreateCommand( PUBLISH, pxContexts[ i ], prvCommandCallback, &xCommand );
        xCommandAdded = prvAddCommandToQueue( &xCommand );

        /* Ensure command was added to queue. */
        configASSERT( xCommandAdded == pdTRUE );

        /* Short delay so we do not bombard the broker with publishes. */
        LogInfo( ( "Publish operation queued. Sleeping for %d ms.\n", mqttexamplePUBLISH_DELAY_ASYNC_MS ) );
        vTaskDelay( pdMS_TO_TICKS( mqttexamplePUBLISH_DELAY_ASYNC_MS ) );
    }

    LogInfo( ( "Finished async publishes.\n" ) );

    /* Receive all task notifications. We may receive notifications in a
     * different order, so we have two loops. If all notifications have been
     * received, we can break early. */
    ( void ) prvNotificationWaitLoop( &ulNotification, ulExpectedNotifications, false );

    for( int i = 0; i < mqttexamplePUBLISH_COUNT / 2; i++ )
    {
        configASSERT( ( ulNotification & ( 1U << i ) ) == ( 1U << i ) );

        LogInfo( ( "Freeing publish context %d.", i + 1 ) );
        vPortFree( pxContexts[ i ] );
        vPortFree( topicBuffers[ i ] );
        vPortFree( payloadBuffers[ i ] );
        LogInfo( ( "Publish context %d freed.", i + 1 ) );
        pxContexts[ i ] = NULL;
    }

    /* Clear this task's notifications. */
    xTaskNotifyStateClear( NULL );
    ulNotification = ulTaskNotifyValueClear( NULL, ~( 0U ) );

    /* Notify main task this task has completed. */
    xTaskNotify( xMainTask, mqttexamplePUBLISHER_ASYNC_COMPLETE_BIT, eSetBits );

    /* Delete this task. */
    LogInfo( ( "Deleting Async Publisher task." ) );
    vTaskDelete( NULL );
}
```


## Subscriber Task

This task subscribes to a topic filter that matches all the topics of the messages published from the synchronous and
asynchronous tasks. It then waits to receive back all those published messages before it unsubscribes. This task is also
responsible for creating the '`TERMINATE`' operation that signals the main task to end the command loop.

```c
void prvSubscribeTask( void * pvParameters )
{
    ( void ) pvParameters;
    MQTTSubscribeInfo_t xSubscribeInfo;
    Command_t xCommand;
    BaseType_t xCommandAdded = pdTRUE;
    MQTTPublishInfo_t * pxReceivedPublish = NULL;
    uint16_t usNumReceived = 0;
    uint32_t ulNotification = 0;
    CommandContext_t xContext;
    PublishElement_t xReceivedPublish;
    uint32_t ulWaitCounter = 0;

    /* The QoS does not affect when subscribe operations are marked completed
     * as it does for publishes. However, we still use QoS 1 here so that the
     * broker will resend publishes if there is a network disconnect. */
    xSubscribeInfo.qos = MQTTQoS1;
    xSubscribeInfo.pTopicFilter = mqttexampleSUBSCRIBE_TOPIC_FILTER;
    xSubscribeInfo.topicFilterLength = ( uint16_t ) strlen( xSubscribeInfo.pTopicFilter );
    LogInfo( ( "Topic filter: %.*s", xSubscribeInfo.topicFilterLength, xSubscribeInfo.pTopicFilter ) );

    /* Create the context and subscribe command. */
    memset( &xContext, 0x00, sizeof( xContext ) );
    xContext.pxResponseQueue = xSubscriberResponseQueue;
    xContext.xTaskToNotify = xTaskGetCurrentTaskHandle();
    xContext.ulNotificationBit = mqttexampleSUBSCRIBE_COMPLETE_BIT;
    xContext.pxSubscribeInfo = &xSubscribeInfo;
    xContext.ulSubscriptionCount = 1;
    LogInfo( ( "Adding subscribe operation" ) );
    prvCreateCommand( SUBSCRIBE, &xContext, prvCommandCallback, &xCommand );
    xCommandAdded = prvAddCommandToQueue( &xCommand );

    /* Ensure command was added to queue. */
    configASSERT( xCommandAdded == pdTRUE );

    /* This demo relies on the server processing our subscription before any publishes.
     * Since this demo uses multiple tasks, we do not retry failed subscriptions, as the
     * server has likely already processed our first publish, and so this demo will not
     * complete successfully. */
    LogInfo( ( "Waiting for subscribe operation to complete." ) );
    ( void ) prvNotificationWaitLoop( &ulNotification, mqttexampleSUBSCRIBE_COMPLETE_BIT, true );

    configASSERT( ( ulNotification & mqttexampleSUBSCRIBE_COMPLETE_BIT ) == mqttexampleSUBSCRIBE_COMPLETE_BIT );
    configASSERT( xContext.xReturnStatus == MQTTSuccess );

    LogInfo( ( "Operation wait complete.\n" ) );

    for( ; ; )
    {
        /* It is possible that there is nothing to receive from the queue, and
         * this is expected, as there are delays between each publish. For this
         * reason, we keep track of the number of publishes received, and break
         * from the outermost while loop when we have received all of them. If
         * the queue is empty, we add a delay before checking it again. */
        while( xQueueReceive( xSubscriberResponseQueue, &xReceivedPublish, mqttexampleDEMO_TICKS_TO_WAIT ) != pdFALSE )
        {
            pxReceivedPublish = &( xReceivedPublish.xPublishInfo );
            pxReceivedPublish->pTopicName = ( const char * ) xReceivedPublish.pcTopicNameBuf;
            pxReceivedPublish->pPayload = xReceivedPublish.pcPayloadBuf;
            LogInfo( ( "Received publish on topic %.*s\nMessage payload: %.*s\n",
                       pxReceivedPublish->topicNameLength,
                       pxReceivedPublish->pTopicName,
                       ( int ) pxReceivedPublish->payloadLength,
                       ( const char * ) pxReceivedPublish->pPayload ) );
            usNumReceived++;

            /* Reset the wait counter every time a publish is received. */
            ulWaitCounter = 0;
        }

        /* Since this is an infinite loop, we want to break if all publishes have
         * been received. */
        if( usNumReceived >= mqttexamplePUBLISH_COUNT )
        {
            break;

        }

        /* Break if we have been stuck in this loop for too long. The total wait
         * here will be ( (loop delay + queue check delay) * `mqttexampleMAX\_WAIT\_ITERATIONS` ).
         * For example, with a 1000 ms queue delay, a 400 ms loop delay, and a
         * maximum iteration of 20, this will wait 28 seconds after receiving
         * the last publish. */
        if( ++ulWaitCounter > mqttexampleMAX_WAIT_ITERATIONS )
        {
            LogError( ( "Publish receive loop exceeded maximum wait time.\n" ) );
            break;
        }


        /* Delay a bit to give more time for publish messages to be received. */
        LogInfo( ( "No messages queued, received %u publish%s, sleeping for %d ms\n",
                   usNumReceived,
                   ( usNumReceived == 1 ) ? "" : "es",
                   mqttexampleSUBSCRIBE_TASK_DELAY_MS ) );
        vTaskDelay( pdMS_TO_TICKS( mqttexampleSUBSCRIBE_TASK_DELAY_MS ) );
    }

    LogInfo( ( "Finished receiving\n" ) );
    prvCreateCommand( UNSUBSCRIBE, &xContext, prvCommandCallback, &xCommand );
    memset( &xContext, 0x00, sizeof( xContext ) );
    xContext.pxResponseQueue = xSubscriberResponseQueue;
    xContext.xTaskToNotify = xTaskGetCurrentTaskHandle();
    xContext.ulNotificationBit = mqttexampleUNSUBSCRIBE_COMPLETE_BIT;
    xContext.pxSubscribeInfo = &xSubscribeInfo;
    xContext.ulSubscriptionCount = 1;
    LogInfo( ( "Adding unsubscribe operation\n" ) );
    xCommandAdded = prvAddCommandToQueue( &xCommand );

    /* Ensure command was added to queue. */
    configASSERT( xCommandAdded == pdTRUE );


    LogInfo( ( "Waiting for unsubscribe operation to complete." ) );
    ( void ) prvNotificationWaitLoop( &ulNotification, mqttexampleUNSUBSCRIBE_COMPLETE_BIT, true );

    configASSERT( ( ulNotification & mqttexampleUNSUBSCRIBE_COMPLETE_BIT ) == mqttexampleUNSUBSCRIBE_COMPLETE_BIT );
    LogInfo( ( "Operation wait complete.\n" ) );


    /* Create command to stop command loop. */
    LogInfo( ( "Beginning command queue termination." ) );
    prvCreateCommand( TERMINATE, NULL, NULL, &xCommand );
    xCommandAdded = prvAddCommandToQueue( &xCommand );

    /* Ensure command was added to queue. */
    configASSERT( xCommandAdded == pdTRUE );

    /* Notify main task this task has completed. */
    xTaskNotify( xMainTask, mqttexampleSUBSCRIBE_TASK_COMPLETE_BIT, eSetBits );

    /* Delete this task. */
    LogInfo( ( "Deleting Subscriber task." ) );
    vTaskDelete( NULL );
}
```
