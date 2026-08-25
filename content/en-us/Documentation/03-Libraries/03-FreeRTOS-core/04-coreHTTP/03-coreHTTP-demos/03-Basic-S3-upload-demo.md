---
title: coreHTTP Basic S3 Upload Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---
## Single Threaded Vs Multi Threaded

There are two coreHTTP usage models, *single threaded* and *multithreaded* (multitasking). Although the
demo on this page runs the HTTP library in a thread, it is actually demonstrating how to use coreHTTP in
a single threaded environment (only one task uses the HTTP API in the demo). Whereas single threaded
applications must repeatedly call the HTTP library, multithreaded applications instead can execute sending
HTTP requests in the background within an agent (or daemon) task.


## Introduction

This example demonstrates sending a PUT request to the AWS S3 HTTP server and uploading a small file.
It also performs a GET request to verify the size of the file after the upload. This example uses
a [network transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) that uses mbedTLS to establish a mutually authenticated
connection between an IoT device client running coreHTTP and AWS S3 HTTP server.

The core HTTP S3 upload demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so you can build and evaluate it with
the [free Community version of Visual Studios](https://visualstudio.microsoft.com/vs/community/) on Windows,
without the need for any particular MCU hardware.


## Source Code Organization

The demo project is called http\_s3\_upload\_demo.sln and can be found in
the FreeRTOS-Plus/Demo/coreHTTP\_Windows\_Simulator/HTTP\_S3\_Upload  directory of
the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) (and in
the [coreHTTP\_Windows\_Simulator](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator)
repository on Github)


## Configuring the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so follow the
instructions provided for the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
to ensure you:

1. Have the [pre-requisite components installed](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites) (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface) on your host machine.

5. ...and **importantly** [test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test) before attempting to run the HTTP demo.

As delivered, the TCP/IP stack is configured to use a dynamic IP address.


## Configuring the AWS S3 HTTP Server Connection

This demo uses a presigned URL to connect the AWS S3 HTTP server and authorize access to the object
to download. The AWS S3 HTTP server's TLS connection uses server authentication only. At the application
level, access to the object is authenticated with parameters in the presigned URL query. Follow the steps
below for configuring your connection to AWS.

1. Set up an Amazon Web Services (AWS) account:

   * If you have not already, [create and activate an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) (which
     includes a [free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)).

   * Accounts and permissions are set using AWS Identity and Access Management (IAM). IAM allows you to
     manage the permissions for each user. By default, no users have permissions until granted by the
     root owner.

     + To add an IAM user to your AWS account, see the [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/).

     + Set permissions for your AWS account to access FreeRTOS and AWS IoT by adding the policies below:

       - AmazonS3FullAccess

2. Create a bucket in S3 by following the steps provided on [AWS Docs](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)

3. Update a file to S3 by following the steps provided on [AWS Docs](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html)

4. Generate a presigned URL using the script located at `FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator/presigned_urls_gen.py`.
   See [FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator/README.md](https://github.com/FreeRTOS/FreeRTOS/tree/p3_rel_wip/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/presigned_url_generator)
   for usage instructions.


## Functionality

The demo first connects to the AWS S3 HTTP server with TLS server authentication. Then it creates an HTTP
request to upload the data specified in `democonfigDEMO_HTTP_UPLOAD_DATA`. After uploading the file, it
checks that file was successfully uploaded by requesting for the size of the file. The structure of the
demo can be found
in [S3UploadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Upload/DemoTasks/S3UploadHTTPExample.c#L317-L480)
on Github.


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:

1. Open the '`http_s3_upload_demo.sln`' Visual Studio solution file from within the Visual Studio IDE.

2. Select '`Build Solution`' from the IDE's '`Build`' menu.

**Note**: If you are using Microsoft Visual Studio 2017 or earlier, then you must select a '`Platform
Toolset`' compatible with your version: '`Project -> RTOSDemos Properties -> Platform Toolset`'.


## Connecting to the AWS S3 HTTP Server

The function `connectToServerWithBackoffRetries()` attempts to make a TCP connection to the HTTP server.
If the connection fails, it retries after a timeout. The timeout value will exponentially increase until
the maximum number of attempts are reached or the maximum timeout value is reached. `connectToServerWithBackoffRetries()`
returns a failure status if the TCP connection cannot be established to the server after the configured number
of attempts. The source code for `connectToServerWithBackoffRetries()` can be found
in [http\_demo\_utils.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/Common/http_demo_utils.c#L76-L129)
 on Github.

The function '`prvConnectToServer()`' demonstrates how to establish a connection to the AWS S3 HTTP server
using server authentication only. It uses the mbedTLS-based transport interface that is implemented in the
file '`FreeRTOS-Plus/Source/Application-Protocols/network_transport/freertos_plus_tcp/using_mbedtls/using_mbedtls.c`'.
The definition of '`prvConnectToServer()`' can be found
in [S3UploadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Upload/DemoTasks/S3UploadHTTPExample.c#L483-L536)
on Github.


## Upload data

The function '`prvUploadS3ObjectFile`' demonstrates how to create a PUT request and specify the file to
upload. The AWS S3 bucket to upload to and the name of file upon upload is specified in the presigned
URL. To save memory, the same buffer is used for both the request headers and the for receiving the
response. The response is received synchronously using API function '`HTTPClient_Send()`'. A `200 OK`
response status-code is expected from the AWS S3 HTTP server; any other status-code received is an error.

The source code for '`prvUploadS3ObjectFile`' can be found
in [S3UploadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Upload/DemoTasks/S3UploadHTTPExample.c#L706-L800)
on Github.


## Verifying upload

The function '`prvVerifyS3ObjectFileSize`' calls '`prvGetS3ObjectFileSize`' to retrieve the size of
the object in the S3 bucket. The S3 HTTP server does not currently support HEAD requests using a presigned
URL, so the 0th byte is requested. The size of the file is contained in the response's `Content-Range`
header field. A `206 Partial Content` response is expected from the server; any other response status-code
received is an error.

The source code for '`prvGetS3ObjectFileSize`' can be found
in [S3DownloadHTTPExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/coreHTTP_Windows_Simulator/HTTP_S3_Download/DemoTasks/S3DownloadHTTPExample.c#L491-L657)
on Github.
