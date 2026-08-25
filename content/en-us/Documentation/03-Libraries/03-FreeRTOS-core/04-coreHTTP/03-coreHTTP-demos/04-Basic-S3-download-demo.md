---
title: coreHTTP Basic S3 Download Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---
## Single Threaded Vs Multi Threaded

There are two coreHTTP usage models, *single threaded* and *multithreaded* (multitasking). Although
the demo on this page runs the HTTP library in a thread, it is actually demonstrating how to use coreHTTP
in a single threaded environment (only one task uses the HTTP API in the demo). Whereas single threaded
applications must repeatedly call the HTTP library, multithreaded applications instead can execute sending
HTTP requests in the background within an agent (or daemon) task.


## Introduction

This demo shows how to use [range requests](https://tools.ietf.org/html/rfc7233) to download files from
AWS S3 http server. Range requests are natively supported in the coreHTTP API when you use `HTTPClient_AddRangeHeader()`
to create the HTTP request. For a microcontroller environment, range requests are highly encouraged - by
downloading a large file in separate ranges, instead of in a single request, each section of the file can
be processed without blocking the network socket. Range requests lower the risk of having dropped packets,
which require retransmissions on the TCP connection, and so they improve the power consumption of the device.

This example uses a [network transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) that uses mbedTLS to establish a
mutually authenticated connection between an IoT device client running coreHTTP and AWS S3 HTTP server.

The core HTTP S3 download demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so you can build and evaluate it with
the [free Community version of Visual Studios](https://visualstudio.microsoft.com/vs/community/) on Windows,
without the need for any particular MCU hardware.


## Source Code Organization

The demo project is called `http_s3_download_demo.sln` and can be found in
the `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download` directory of
the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) (and in
the [coreHTTP\_Windows\_Simulator](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator)
repository on GitHub).


## Configuring the Demo Project

The demo uses
the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so follow the instructions
provided for the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
to ensure you:

1. Install the [pre-requisite components](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface) on your host machine.

5. ...and **importantly** [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test) before attempting to run the HTTP demo.

As delivered, the TCP/IP stack is configured to use a dynamic IP address.


## Configuring the AWS S3 HTTP Server Connection

This demo uses a presigned URL to connect to the AWS S3 HTTP server and authorize access to the object
to download. The AWS S3 HTTP server's TLS connection uses server authentication only. At the application
level, access to the object is authenticated with parameters in the presigned URL query. Follow the steps
below to configure your connection to AWS.

1. Set up an Amazon Web Services (AWS) account:

   * If you haven't already,
     [create and activate an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) (which
     includes a [free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)).

   * Accounts and permissions are set using AWS Identity and Access Management (IAM). IAM allows you to
     manage permissions for each user in your account. By default, a user doesn't have permissions until
     granted by the root owner.

     1. To add an IAM user to your AWS account, see the [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/).

     2. Grant permission to your AWS account to access FreeRTOS and AWS IoT by adding these policies:

        + AmazonS3FullAccess

2. Create a bucket in S3 by following the steps
   in [How do I create an S3 Bucket?](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)
   in the *Amazon Simple Storage Service Console User Guide*.

3. Upload a file to S3 by following the steps in [How do I upload files and folders to an S3 bucket?](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html).

4. Generate a presigned URL using the script located
   at `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator/presigned_urls_gen.py`.
   See [FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator/README.md](https://github.com/FreeRTOS/FreeRTOS/tree/p3_rel_wip/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator)
   for usage instructions.


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:

1. Open the `http_s3_download_demo.sln` Visual Studio solution file from within the Visual Studio IDE.

2. Select '**Build Solution**' from the IDE's '**Build**' menu.

**Note**: If you are using Microsoft Visual Studio 2017 or earlier, then you must select a '**Platform Toolset**'
compatible with your version: '**Project -> RTOSDemos Properties -> Platform Toolset**'.


## Functionality

The demo retrieves the size of the file first. Then it requests each byte range sequentially, in a loop,
with range sizes of `democonfigRANGE_REQUEST_LENGTH`.

Source code for the demo can be found
in [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L269-L430)
on GitHub.


### Connecting to the AWS S3 HTTP Server

The function `connectToServerWithBackoffRetries()` attempts to make a TCP connection to the HTTP server.
If the connection fails, it retries after a timeout. The timeout value will exponentially increase until
the maximum number of attempts are reached or the maximum timeout value is reached. `connectToServerWithBackoffRetries()`
returns a failure status if the TCP connection to the server cannot be established after the configured
number of attempts.

The source code for `connectToServerWithBackoffRetries()` can be found
in [http\_demo\_utils.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/http_demo_utils.c#L71-L120)
on GitHub.

The function `prvConnectToServer()` demonstrates how to establish a connection to the AWS S3 HTTP server
using server authentication only. It uses the mbedTLS-based transport interface that is implemented in the
file `FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp/using_mbedtls/using_mbedtls.c`.

prvConnectToServer() can be found
in [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L433-L488)
on GitHub.


### Creating a Range Request

The API function `HTTPClient_AddRangeHeader()` supports serializing a byte range into the HTTP request
headers to form a range request. Range requests are used in this demo to retrieve the file size and to
request each section of the file.

The function `prvGetS3ObjectFileSize()` retrieves the size of the file in the S3 bucket. The "Connection: keep-alive"
header is added in this first request to S3 to keep the connection open after the response is sent. The
S3 HTTP server does not currently support HEAD requests using a presigned URL, so the 0th byte is requested.
The size of the file is contained in the response's `Content-Range` header field. A `206 Partial Content`
response is expected from the server; any other response status-code received is an error.

The source code for `prvGetS3ObjectFileSize()` can be found
in [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L491)
on GitHub.

After it retrieves the file size, this demo creates a new range request for each byte range of the file to
download. It uses `HTTPClient_AddRangeHeader()` for each section of the file.

The source code can be found
in [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L732-L734)
on GitHub.


### Sending Range Requests and Receiving Responses

The function `prvDownloadS3ObjectFile()` sends the range requests in a loop until the entire file is downloaded.
The API function `HTTPClient_Send()` sends a request and receives the response synchronously. When the function
returns, the response is received in an `xResponse`. The status-code is then verified to be `206 Partial Content`
and the number of bytes downloaded so far is incremented by the `Content-Length` header value.

The source code for `prvDownloadS3ObjectFile()` can be found
on [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L660-L803)
on GitHub.
