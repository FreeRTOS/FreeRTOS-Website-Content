---
title: "coreMQTT Demo (Mutual Authentication)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**Note: We recommend to always use mutual authentication in building any Internet of Things (IoT) application.**

The [coreMQTT demo (Mutual Authentication)](https://github.com/FreeRTOS/FreeRTOS/tree/202012.00/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth)
described on this page uses MBEDTLS to perform the encryption functions. An additional demo that uses
WolfSSL can be found on
our [Github](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth_wolfSSL)
along with [instructions to convert](https://github.com/FreeRTOS/FreeRTOS-SESIP/blob/main/docs/wolfSSL-migration-guide/migrating_to_wolfssl.md)
the demo from MBEDTLS to WolfSSL. This new demo will be available in an upcoming release of FreeRTOS.

## Single Threaded Vs Multi Threaded

There are two coreMQTT usage models, _single threaded_ and _multithreaded_ (multitasking). Using the
MQTT library solely from one thread within an otherwise multi-threaded application, as the demo documented
on this page does, is equivalent to the single threaded use case. Single threaded use cases require
the application writer to make repeated explicit calls into the MQTT library. Multithreaded use cases
can instead execute the MQTT protocol in the background within [an agent (or daemon) task](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo).
Executing the MQTT protocol in an agent task removes the need for the application writer to explicitly
manage any MQTT state or call the `MQTT_ProcessLoop()` API function. Using an agent task also enables
multiple application tasks to share a single MQTT connection without the need for synchronization primitives
such as mutexes.

## Demo Introduction

This example project is one of three that introduce the concepts described on
the ["TLS Introduction"](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction) page one at a time. The [first example](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo) 
demonstrates unencrypted MQTT communication, the [second example](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/02-coreMQTT-demo-LTS) builds on the first to introduce server authentication (where the IoT client authenticates the MQTT server
it connects to). The third example (on this page) builds on the second to introduce strong mutual authentication (where
the MQTT server also authenticates the client connecting to it).

The demo uses a [network transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) that uses mbedTLS to establish a
mutually authenticated connection between an IoT device client running coreMQTT and an MQTT broker.
It can be used with any MQTT broker capable of mutually authenticated connections - the instructions
below describe how to connect to [Amazon Web Services (AWS) IoT message broker](https://aws.amazon.com/iot-core/)
or to an MQTT server running locally on the host.

Once connected the demo subscribes to an MQTT topic, then publishes to the same MQTT topic before waiting
for the message back from the MQTT server (the message is received back because the MQTT client is subscribed
to the same topic to which it publishes). It repeats the publish and receive cycle indefinitely.

This demo uses [QoS 1](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology) publishes and subscriptions - meaning each MQTT message is received at least once.

The coreMQTT (Mutual Authentication) demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
enabling it to be built and evaluated with
the [free Community version of Visual Studios](https://visualstudio.microsoft.com/vs/community/) on
Windows, so without the need for any particular MCU hardware.

## Source Code Organization

The demo project is called mqtt_mutual_auth_demo.sln and is located in
the `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth` directory of the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) (links
to Github are also on the download page).

The source code is organized as per the [basic MQTT demo (without TLS).](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo)

## Configuring the MQTT Broker Connection

### Option 1: Using the AWS IoT message broker (web hosted):

The Mutual Authentication MQTT demo requires client authentication in addition to the server authentication
required in the [MQTT with TLS (Server Auth)](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/02-coreMQTT-demo-LTS) demo. As most public
 brokers do not authenticate the client, this demo will showcase a connection to AWS (Amazon Web Services)
 IoT.  Additional steps are required to acquire and set up credentials using existing tools provided by
 AWS. After you complete the setup steps below, the configuration can be reused with other AWS IoT related
 demos such as [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/04-Device-shadow-demo). For enhanced security, AWS IoT does
 not support plaintext and server side only authentication.
 See [Security in AWS](https://docs.aws.amazon.com/freertos/latest/userguide/security.html) for more details.

Follow the steps below for configuring your connection to AWS.

1. Set up an Amazon Web Services (AWS) account:

   - If you have not already, [create and activate an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
     (which includes a [free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)).

2. Accounts and permissions are set using AWS Identity and Access Management (IAM). IAM allows you to
   manage the permissions for each user. By default, no users have permissions until granted by the root
   owner.

   - To add an IAM user to your AWS account, see the [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/).
   - Set permissions for your AWS account to access FreeRTOS and AWS IoT by adding the policies below:

     - `AmazonFreeRTOSFullAccess`
     - `AWSIoTFullAccess`

     To attach the AmazonFreeRTOSFullAccess policy to your IAM user:

     1. Browse to the [IAM console](https://console.aws.amazon.com/iam/home), and from the navigation pane, choose **Users**.
     2. Enter your user name in the search text box, and then choose it from the list.
     3. Choose **Add permissions**.
     4. Choose **Attach existing policies directly**.
     5. In the search box, enter **`AmazonFreeRTOSFullAccess`**, choose it from the list, and then choose **Next: Review**.
     6. Choose **Add permissions**.

     To attach the AWSIoTFullAccess policy to your IAM user:

     1. Browse to the [IAM console](https://console.aws.amazon.com/iam/home) and, from the navigation pane, choose **Users**.
     2. Enter your user name in the search text box, and then choose it from the list.
     3. Choose **Add permissions**.
     4. Choose **Attach existing policies directly**.
     5. In the search box, enter **`AWSIoTFullAccess`**, choose it from the list, and then choose **Next: Review**.
     6. Choose **Add permissions**.

3. Register a device as an AWS IoT thing with the AWS Command Line Interface (CLI) or AWS IoT Console. 
   AWS CLI allows you to perform configurations through the command line instead of through the AWS IoT
   Console interface.  For more information on setting up CLI, please view additional documentation here. 
   The AWS IoT console provides a user interface for you to setup a device manually.

   - **Option 1 (recommended):** Set up through the AWS Command-Line Interface (CLI):

     1. [Download and Install](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) the
        AWS CLI on your computer.
     2. Install boto3 with pip: `pip install boto3`
     3. Continue with the steps in [Quickly Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration)
        to set it up with your AWS account information
     4. Register a device with the provided python script. The script sets up the MQTT broker (using
        the "thing" name you entered), downloads the private key, and writes the credentials
        to `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/demo_config.h.`.

        1. In the file `{FreeRTOS-root-directory}/tools/aws_config_quick_start/configure.json` change the `"$thing_name"` to your
           MQTT client ID. The thing name you enter should be enclosed within double quotes (`""`), and contain
           a combination of letters, numbers, semicolons (`:`), underscores (`_`), and hyphens (`-`) only.

        2. To finish setup, open a terminal, navigate to the `{FreeRTOS-root-directory}/tools/aws_config_quick_start` directory and
           run: `python SetupAWS.py setup`

        3. If you used python3 for AWS CLI installation, run: `python3 SetupAWS.py setup`

   - **Option 2:** Manually setup a thing through the AWS IoT Console:

     1. Add a device to AWS IoT Console

        Follow the [steps](https://docs.aws.amazon.com/iot/latest/developerguide/create-iot-resources.html)
        in creating an IoT thing, private key, and certificate for your device to register an AWS IoT. Take
        note of your thing name and AWS IoT endpoint, and download the certificate and key associated with
        your thing. To find your AWS IoT endpoint:

        1. Browse to the [AWS IoT console](https://console.aws.amazon.com/iotv2/).
        2. In the navigation pane, choose **Settings**.

        Your AWS IoT endpoint is displayed as the **Endpoint**. It should look
        like `*`\<account-number>`*-ats.iot.*`\<us-east-1>`*.amazonaws.com`.

     2. Once you have completed the setup on the service side, you need to configure credentials for AWS
        IoT credentials on the client side. The file `aws_iot_demo_profile.h` holds the information you need
        to connect your FreeRTOS project to AWS IoT, including endpoints, credentials, and keys set to the
        appropriate values.  Setup the credentials through the Certificate Configurator by following the steps
        below:

        1. In a browser window, open `{FreeRTOS-root-directory}/tools/aws_config_offline/CertificateConfigurator.html`.
        2. Under **Thing Name**, enter the Thing name you registered on AWS IoT.
        3. Under **AWS IoT Thing Endpoint**, enter your AWS IoT endpoint.
        4. Under **Certificate PEM file**, choose the `*`\<ID>`*-certificate.pem.crt` that you downloaded from
           the AWS IoT console.
        5. Under **Private Key PEM file**, choose the `*`\<ID>`*-private.pem.key` that you downloaded from the
           AWS IoT console.
        6. Choose **Generate** and save `demo_config.h`, and then save the file
           in `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/demo_config.h`. This overwrites
           the existing file in the directory.

    **Note: Make sure that the final `demo_config` file being used contains the macro `democonfigUSE_TLS` set to `1` in order to enable TLS**

#### Client authentication with AWS IoT with MQTT username and password (Additional Option)

In addition to the Certificate and Private Key based client authentication, AWS IoT Message broker supports
a [custom client authentication](https://docs.aws.amazon.com/iot/latest/developerguide/custom-authentication.html)
method using MQTT username and password. Only one of these two client authentication methods is required for
client authentication. If the Certificate and Private Key based client authentication is sufficient for your
configuration, **you can ignore this section**. If username and password based authentication is used,
Thing’s Certificate and Private key configured as per the steps above, will be ignored by the demo application.

Follow the steps below for configuring your custom authentication in AWS IoT and configure the demo.

1. Create a custom authorizer in AWS IoT by following the instructions
   in [AWS documentation](https://docs.aws.amazon.com/iot/latest/developerguide/config-custom-auth.html).
2. Update the config `democonfigCLIENT_USERNAME` in `demo_config.h` file to the username configured in
   AWS IoT authorizer in step 1.
3. Update the `config democonfigCLIENT_PASSWORD` in `demo_config.h` file to the password configured in
   AWS IoT authorizer in step 1.
4. Custom authentication is supported only on port 443 in AWS IoT Message broker as mentioned in
   the [AWS documentation](https://docs.aws.amazon.com/iot/latest/developerguide/custom-auth.html). Update
   the config `democonfigMQTT_BROKER_PORT` in `demo_config.h` file to ( 443 ).

### Option 2: Using a locally hosted Mosquitto MQTT message broker (host machine):

A Mosquitto MQTT broker can be run locally and this demo can be connected with a mutually authenticated
connection. This broker can be run either on your host machine (the machine used to build the demo application),
or another machine on your local network. To do this, follow the steps listed
in [mqtt_broker_setup.txt](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/mqtt_broker_setup.txt)
to configure a Mosquitto MQTT message broker locally and configure the demo to work with that broker.

### Build the Demo Project

You build this demo project in the same way as the [basic MQTT demo (without TLS)](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#source_code).
The demo project uses the free community edition of [Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build this demo:

- Open the `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/mqtt_mutual_auth_demo.sln` Visual
  Studio solution file from within the Visual Studio IDE
- Select Build Solution from the IDE’s Build menu

**NOTE:** If you are using Microsoft Visual Studio 2017 or earlier, then you must select a Platform
Toolset compatible with your version: Project -> RTOSDemos Properties -> Platform Toolset


### Functionality

The demo provides the same functionality as the basic MQTT demo with the addition of secure connection to your AWS IoT.  For details on the additional functionality (Subscribing to a MQTT Topic, Publishing to a MQTT topic, Receiving incoming messages, Processing Incoming MQTT Publish Packets, and Unsubscribing from a Topic) please view the [basic MQTT demo (without TLS).](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo#functionality)

The demo creates a single application task that loops through a set of examples that demonstrate how to connect to the broker, subscribe to a topic on the broker, publish to a topic on the broker, then finally, disconnect from the broker. The demo application both subscribes to and publishes to the same topic. Each time the demo publishes a message to the MQTT broker the broker sends the same message back to the demo application. The structure of the demo is shown below:

```c
static void prvMQTTDemoTask( void * pvParameters )
{
    uint32_t ulPublishCount = 0U, ulTopicCount = 0U;
    const uint32_t ulMaxPublishCount = 5UL;
    NetworkContext_t xNetworkContext = { 0 };
    NetworkCredentials_t xNetworkCredentials = { 0 };
    MQTTContext_t xMQTTContext = { 0 };
    MQTTStatus_t xMQTTStatus;
    TlsTransportStatus_t xNetworkStatus;

    /* Remove compiler warnings about unused parameters. */
    ( void ) pvParameters;

    /* Set the entry time of the demo application. This entry time will be used
     * to calculate relative time elapsed in the execution of the demo
     * application, by the timer utility function that is provided to the MQTT
     * library. */
    ulGlobalEntryTimeMs = prvGetTimeMs();

    for( ; ; )
    {
        /************************** Connect. ****************************/

        /* Attempt to establish TLS session with MQTT broker. If connection
         * fails, retry after a timeout. Timeout value will be exponentially
         * increased until  the maximum number of attempts are reached or the
         * maximum timeout value is reached. The function returns a failure
         * status if the TCP connection cannot be established to the broker
         * after the configured number of attempts. */
        xNetworkStatus = prvConnectToServerWithBackoffRetries(
                                                     &xNetworkCredentials,
                                                     &xNetworkContext );
        configASSERT( xNetworkStatus == TLS_TRANSPORT_SUCCESS );

        /* Sends an MQTT Connect packet over the already established TLS
        connection and waits for connection acknowledgment (CONNACK) packet. */

        LogInfo( ( "Creating an MQTT connection to %s.\r\n", democonfigMQTT_BROKER_ENDPOINT ) );
        prvCreateMQTTConnectionWithBroker( &xMQTTContext, &xNetworkContext );

        /************************* Subscribe. ***************************/

        /* If server rejected the subscription request, attempt to resubscribe
         * to topic. Attempts are made according to the exponential backoff
         * retry strategy implemented in retryUtils. */
        prvMQTTSubscribeWithBackoffRetries( &xMQTTContext );

        /*************** Publish and Keep Alive Loop ********************/
        /* Publish messages with QoS1, send and process Keep alive messages. */
        for( ulPublishCount = 0; ulPublishCount < ulMaxPublishCount;
            ulPublishCount++ )
        {
            LogInfo( ( "Publish to the MQTT topic %s.\r\n",
                        mqttexampleTOPIC ) );
            prvMQTTPublishToTopic( &xMQTTContext );

            /* Process incoming publish echo, since application subscribed to
             * the same topic, the broker will send publish message back to the
             * application. */
            LogInfo( ( "Attempt to receive publish message from broker.\r\n" )
            );
            xMQTTStatus = MQTT_ProcessLoop( &xMQTTContext,
            mqttexamplePROCESS_LOOP_TIMEOUT_MS );
            configASSERT( xMQTTStatus == MQTTSuccess );

            /* Leave Connection Idle for some time. */
            LogInfo( ( "Keeping Connection Idle...\r\n\r\n" ) );
            vTaskDelay( mqttexampleDELAY_BETWEEN_PUBLISHES_TICKS );
        }

        /***************** Unsubscribe from the topic. ******************/
        LogInfo( ( "Unsubscribe from the MQTT topic %s.\r\n", mqttexampleTOPIC
        ) );
        prvMQTTUnsubscribeFromTopic( &xMQTTContext );

        /* Process incoming UNSUBACK packet from the broker. */
        xMQTTStatus = MQTT_ProcessLoop( &xMQTTContext,
                                        mqttexamplePROCESS_LOOP_TIMEOUT_MS );
        configASSERT( xMQTTStatus == MQTTSuccess );

        /************************* Disconnect. **************************/

        /* Send an MQTT Disconnect packet over the already connected TLS over
         * TCP connection. There is no corresponding response for the
         * disconnect packet. After sending disconnect, client must close the
         * network connection. */
        LogInfo( ( "Disconnecting the MQTT connection with %s.\r\n",
                    democonfigMQTT_BROKER_ENDPOINT ) );
        xMQTTStatus = MQTT_Disconnect( &xMQTTContext );
        configASSERT( xMQTTStatus == MQTTSuccess );

        /* Close the network connection.  */
        TLS_FreeRTOS_Disconnect( &xNetworkContext );

        /* Reset SUBACK status for each topic filter after completion of
         * subscription request cycle. */
        for( ulTopicCount = 0; ulTopicCount < mqttexampleTOPIC_COUNT;
        ulTopicCount++ )
        {
            xTopicFilterContext[ ulTopicCount ].xSubAckStatus =
            MQTTSubAckFailure;
        }

        /* Wait for some time between two iterations to ensure that we do not
         * bombard the broker. */
        LogInfo( ( "prvMQTTDemoTask() completed an iteration successfully. "
                   "Total free heap is %u.\r\n",
                    xPortGetFreeHeapSize() ) );
        LogInfo( ( "Demo completed successfully.\r\n" ) );
        LogInfo( ( "Short delay before starting the next iteration....
                    \r\n\r\n" ) );
        vTaskDelay( mqttexampleDELAY_BETWEEN_DEMO_ITERATIONS_TICKS );
    }
}
```

### Connect to the MQTT Broker (with mutual authentication)

The function `prvConnectToServerWithBackoffRetries()` attempts to make a mutually authenticated TLS connection to the MQTT broker. If the connection fails, it retries after a timeout. The timeout value will exponentially increase until the maximum number of attempts are reached or the maximum timeout value is reached. The function `RetryUtils_BackoffAndSleep()` provides exponentially increasing timeout value and returns `RetryUtilsRetriesExhausted` when the maximum number of attempts have been reached. `prvConnectToServerWithBackoffRetries()` returns a failure status if the TLS connection cannot be established to the broker after the configured number of attempts.

```c
static TlsTransportStatus_t prvConnectToServerWithBackoffRetries(
                                NetworkCredentials_t * pxNetworkCredentials,
                                NetworkContext_t * pxNetworkContext )
{
    TlsTransportStatus_t xNetworkStatus;
    RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;
    RetryUtilsParams_t xReconnectParams;

    #ifdef democonfigUSE_AWS_IOT_CORE_BROKER

        /* ALPN protocols must be a NULL-terminated list of strings. Therefore,
         * the first entry will contain the actual ALPN protocol string while
         * the second entry must remain NULL. */
        char * pcAlpnProtocols[] = { NULL, NULL };

        /* The ALPN string changes depending on whether username/password
        authentication is used. */
        #ifdef democonfigCLIENT_USERNAME
            pcAlpnProtocols[ 0 ] = AWS_IOT_CUSTOM_AUTH_ALPN;
        #else
            pcAlpnProtocols[ 0 ] = AWS_IOT_MQTT_ALPN;
        #endif
        pxNetworkCredentials->pAlpnProtos = pcAlpnProtocols;
    #endif /* ifdef democonfigUSE_AWS_IOT_CORE_BROKER */

    pxNetworkCredentials->disableSni = democonfigDISABLE_SNI;
    /* Set the credentials for establishing a TLS connection. */
    pxNetworkCredentials->pRootCa = ( const unsigned char * )
    democonfigROOT_CA_PEM;
    pxNetworkCredentials->rootCaSize = sizeof( democonfigROOT_CA_PEM );
    #ifdef democonfigCLIENT_CERTIFICATE_PEM
        pxNetworkCredentials->pClientCert = ( const unsigned char * )
                                    democonfigCLIENT_CERTIFICATE_PEM;
        pxNetworkCredentials->clientCertSize = sizeof(
                                    democonfigCLIENT_CERTIFICATE_PEM );
        pxNetworkCredentials->pPrivateKey = ( const unsigned char * )
        democonfigCLIENT_PRIVATE_KEY_PEM;
        pxNetworkCredentials->privateKeySize = sizeof(
        democonfigCLIENT_PRIVATE_KEY_PEM );
    #endif
    /* Initialize reconnect attempts and interval. */
    RetryUtils_ParamsReset( &xReconnectParams );
    xReconnectParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;

    /* Attempt to connect to MQTT broker. If connection fails, retry after
     * a timeout. Timeout value will exponentially increase till maximum
     * attempts are reached.*/
    do
    {
        /* Establish a TLS session with the MQTT broker. This example connects
         * to the MQTT broker as specified in democonfigMQTT_BROKER_ENDPOINT
         * and democonfigMQTT_BROKER_PORT at the top of this file. */
        LogInfo( ( "Creating a TLS connection to %s:%u.\r\n",
                   democonfigMQTT_BROKER_ENDPOINT,
                   democonfigMQTT_BROKER_PORT ) );
        /* Attempt to create a mutually authenticated TLS connection. */
        xNetworkStatus = TLS_FreeRTOS_Connect(
                                    pxNetworkContext,
                                    democonfigMQTT_BROKER_ENDPOINT,
                                    democonfigMQTT_BROKER_PORT,
                                    pxNetworkCredentials,
                                    mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS,
                                    mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS
                                              );

        if( xNetworkStatus != TLS_TRANSPORT_SUCCESS )
        {
            LogWarn( ( "Connection to the broker failed. Retrying connection
            with backoff and jitter." ) );
            xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xReconnectParams
            );
        }

        if( xRetryUtilsStatus == RetryUtilsRetriesExhausted )
        {
            LogError( ( "Connection to the broker failed, all attempts
            exhausted." ) );
            xNetworkStatus = TLS_TRANSPORT_CONNECT_FAILURE;
        }
    } while( ( xNetworkStatus != TLS_TRANSPORT_SUCCESS ) &&
             ( xRetryUtilsStatus == RetryUtilsSuccess ) );

    return xNetworkStatus;
}
```

The function `prvCreateMQTTConnectionWithBroker()` demonstrates how to establish an MQTT connection to an MQTT broker with a clean session. It uses the TLS transport interface which is implemented in the file `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/tls_freertos.c`. The definition of `prvCreateMQTTConnectionWithBroker()` is shown below. Keep in mind that we are setting the keep-alive seconds for the broker in `xConnectInfo`.

The function below shows how TLS transport interface and time function are set in MQTT Context using `MQTT_Init()`. It also shows how event callback function pointer `( prvEventCallback )` is set. This callback is used for reporting incoming messages.

```c
static void prvCreateMQTTConnectionWithBroker(
                                    MQTTContext_t * pxMQTTContext,
                                    NetworkContext_t * pxNetworkContext )
{
    MQTTStatus_t xResult;
    MQTTConnectInfo_t xConnectInfo;
    bool xSessionPresent;
    TransportInterface_t xTransport;

    /***
     * For readability, error handling in this function is restricted to the
     * use of asserts().
     ***/

    /* Fill in Transport Interface send and receive function pointers. */
    xTransport.pNetworkContext = pxNetworkContext;
    xTransport.send = TLS_FreeRTOS_send;
    xTransport.recv = TLS_FreeRTOS_recv;

    /* Initialize MQTT library. */
    xResult = MQTT_Init( pxMQTTContext, &xTransport, prvGetTimeMs,
                         prvEventCallback, &xBuffer );
    configASSERT( xResult == MQTTSuccess );

    /* Some fields are not used in this demo so start with everything at 0. */
    ( void ) memset( ( void * ) &xConnectInfo, 0x00, sizeof( xConnectInfo ) );

    /* Start with a clean session i.e. direct the MQTT broker to discard any
     * previous session data. Also, establishing a connection with clean
     * session will ensure that the broker does not store any data when this
     * client gets disconnected. */
    xConnectInfo.cleanSession = true;

    /* The client identifier is used to uniquely identify this MQTT client to
     * the MQTT broker. In a production device the identifier can be something
     * unique, such as a device serial number. */
    xConnectInfo.pClientIdentifier = democonfigCLIENT_IDENTIFIER;
    xConnectInfo.clientIdentifierLength = ( uint16_t ) strlen(
                                                democonfigCLIENT_IDENTIFIER );

    /* Set MQTT keep-alive period. If the application does not send packets at
     * an interval less than the keep-alive period, the MQTT library will send
     * PINGREQ packets. */
    xConnectInfo.keepAliveSeconds = mqttexampleKEEP_ALIVE_TIMEOUT_SECONDS;

    /* Append metrics when connecting to the AWS IoT Core broker. */
    #ifdef democonfigUSE_AWS_IOT_CORE_BROKER
        #ifdef democonfigCLIENT_USERNAME
            xConnectInfo.pUserName = CLIENT_USERNAME_WITH_METRICS;
            xConnectInfo.userNameLength = ( uint16_t ) strlen(
                                        CLIENT_USERNAME_WITH_METRICS );
            xConnectInfo.pPassword = democonfigCLIENT_PASSWORD;
            xConnectInfo.passwordLength = ( uint16_t ) strlen(
            democonfigCLIENT_PASSWORD );
        #else
            xConnectInfo.pUserName = AWS_IOT_METRICS_STRING;
            xConnectInfo.userNameLength = AWS_IOT_METRICS_STRING_LENGTH;
            /* Password for authentication is not used. */
            xConnectInfo.pPassword = NULL;
            xConnectInfo.passwordLength = 0U;
        #endif
    #else /* ifdef democonfigUSE_AWS_IOT_CORE_BROKER */
        #ifdef democonfigCLIENT_USERNAME
            xConnectInfo.pUserName = democonfigCLIENT_USERNAME;
            xConnectInfo.userNameLength = ( uint16_t ) strlen(
                                            democonfigCLIENT_USERNAME );
            xConnectInfo.pPassword = democonfigCLIENT_PASSWORD;
            xConnectInfo.passwordLength = ( uint16_t ) strlen(
                                            democonfigCLIENT_PASSWORD );
        #endif /* ifdef democonfigCLIENT_USERNAME */
    #endif /* ifdef democonfigUSE_AWS_IOT_CORE_BROKER */

    /* Send MQTT CONNECT packet to broker. LWT is not used in this demo, so it
     * is passed as NULL. */
    xResult = MQTT_Connect( pxMQTTContext,
                            &xConnectInfo,
                            NULL,
                            mqttexampleCONNACK_RECV_TIMEOUT_MS,
                            &xSessionPresent );
    configASSERT( xResult == MQTTSuccess );

    /* Successfully established and MQTT connection with the broker. */
    LogInfo( ( "An MQTT connection is established with %s.",
                democonfigMQTT_BROKER_ENDPOINT ) );
}
```
