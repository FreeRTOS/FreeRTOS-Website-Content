---
title: coreHTTP Basic MultiThreaded Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---
## Introduction

This demo uses [FreeRTOS's thread-safe queues](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement) to hold requests and responses awaiting
processing. There are three tasks to note of, in this demo:

* The main task waits for requests in the request queue. It will send those requests over the network, then
  place the response into the response queue.

* A request task creates HTTP library request objects to send to the server and places them into the request queue. Each
  request object specifies a byte range of the S3 file that the application configured for download.

* A response task waits for responses in the response queue. It will log every response it receives.

This basic multithreaded demo is configured to use a TLS connection with server authentication only, this
is required by the S3 HTTP server. Application layer authentication is done using
the [Signature Version 4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) parameters
in the [presigned URL query](https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-query-string-auth.html).

The coreHTTP Basic Multithreaded demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so you can build and evaluate it with
the [free Community version of Visual Studios](https://visualstudio.microsoft.com/vs/community/) on Windows,
without the need for any particular MCU hardware.


## Source Code Organization

The Visual Studio solution for the multithreaded HTTP S3 demo is
called [`http_s3_download_multithreaded_demo.sln`](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/http_s3_download_multithreaded_demo.sln)
and is located in the [/FreeRTOS-Plus/Demo/coreHTTP\_Windows\_Simulator/HTTP\_S3\_Download\_Multithreaded](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded)
directory of the [main FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) download.


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:

1. Open the '`mqtt_multitask_demo.sln`' Visual Studio solution file from within the Visual Studio IDE.

2. Select '`Build Solution`' from the IDE's '`Build`' menu.

**Note**: If you are using Microsoft Visual Studio 2017 or earlier, then you must select a '`Platform
Toolset`' compatible with your version: '`Project -> RTOSDemos Properties -> Platform Toolset`'.


## Configuring the Demo Project

The demo uses
the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so follow the instructions
provided for the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
to ensure you:

1. Have the [pre-requisite components installed](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface) on your host machine.

5. ...and **importantly** [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test) before attempting to run the HTTP demo.


## Configuring the AWS S3 HTTP Server Connection

This demo supports the same configuration options as
the [coreHTTP Basic S3 Download](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/04-Basic-S3-download-demo) demo. Please see that demo's
documentation instructions on configuring the AWS S3 HTTP server connection.


## Functionality

The demo creates three tasks in total:

* One that sends requests and receives responses over the network
* One that creates requests to send
* One that processes the received responses.

In this demo, the primary task creates the request and response queues, create the connection to the server,
creates the request and response tasks, waits on the request queue to send requests over the network, and
places responses received over the network into the response queue. The request task creates each of the
range requests and response task processes each of the responses received.


## Typedefs

The demo defines the following structures to support multithreading:

**Request Items**
The following structures defines a request item to place into the request queue. It is copied into the
queue after the request task creates an HTTP request.

```c
/**
 * @brief Data type for the request queue.
 *
 * Contains the request header struct and its corresponding buffer, to be
 * populated and enqueued by the request task, and read by the main task. The
 * buffer is included to avoid pointer inaccuracy during queue copy operations.
 */
typedef struct RequestItem
{
    HTTPRequestHeaders_t xRequestHeaders;
    uint8_t ucHeaderBuffer[ democonfigUSER_BUFFER_LENGTH ];
} RequestItem_t;
```

**Response Item**
The following structures defines a response item to place into the response queue. It is copied into
the queue after the main HTTP task receives a response over the network.

```c
/**
 * @brief Data type for the response queue.
 *
 * Contains the response data type and its corresponding buffer, to be enqueued
 * by the main task, and interpreted by the response task. The buffer is
 * included to avoid pointer inaccuracy during queue copy operations.
 */
typedef struct ResponseItem
{
    HTTPResponse_t xResponse;
    uint8_t ucResponseBuffer[ democonfigUSER_BUFFER_LENGTH ];
} ResponseItem_t;
```

## Main HTTP Send Task

The main application task starts by parsing the presigned URL for the host address to establishes a
connection with the AWS S3 HTTP server. It also parses the presigned URL for the path to the objects
in the S3 bucket. It then connects to the AWS HTTP S3 server using TLS with server authentication.
Next, the request and response queues are created, and the request and response tasks are created.
The function '`prvHTTPDemoTask()`' does this set up and gives demo status.

The source code for this function can be found in
the [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L471-L650)
file on GitHub.

In the function '`prvDownloadLoop()`', the main task blocks and waits on requests from the queue.
When it receives a request it will send it using API function '`HTTPClient_Send()`'. If the API function
was successful, then it places the response into the response queue.

The source code for '`prvDownloadLoop()`' can be found in
the [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L1071-L1174)
file on GitHub.


## HTTP Request Task

The request task is specified in function '`prvRequestTask`'.

The source code for this function can be found in
the [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L777-L878)
file on GitHub.

The request task starts by retrieving the size of the object in S3. This retrieval is done in the
function '`prvGetS3ObjectFileSize`'. It retrieves the size of the file in the S3 bucket. The "Connection: keep-alive"
header is added to this request to S3 to keep the connection open after the response is sent. The S3 HTTP
server does not currently support HEAD requests using a presigned URL, so the 0th byte is requested. The
size of the file is contained in the response's `Content-Range` header field. A `206 Partial Content`
response is expected from the server; any other response status-code received is an error.

The source code for '`prvGetS3ObjectFileSize`' can be found in
the [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L757-L775)
file on GitHub.

After retrieving the file size, the request task continuously requests each range of the file. Each range
request is placed into the request queue for the main task to send. The file ranges are configured by the
demo user in macro `democonfigRANGE_REQUEST_LENGTH`. Range requests are natively supported in the HTTP
client library API using function '`HTTPClient_AddRangeHeader()`'. The function '`prvRequestS3ObjectRange()`'
demonstrates usage of '`HTTPClient_AddRangeHeader()`'.

The source code for '`prvRequestS3ObjectRange()`' can be found in
the [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L757-L775)
file on GitHub.


## HTTP Response task

The response tasks waits on the response queue for responses received over the network. The main task
populates the response queue when successfully receiving an HTTP response. This task processes the responses
by logging the status-code, headers, and body. A real-world application may process the response by writing
the response body to flash memory, for example. If the response status-code is not `206 partial content`,
then the task notifies the main task that the demo should fail. The response task is specified in
function '`prvResponseTask()`'.

The source code for this function can be found in
the [S3DownloadMultithreadedHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download_Multithreaded/DemoTasks/S3DownloadMultithreadedHTTPExample.c#L961-L1048)
file on GitHub.
