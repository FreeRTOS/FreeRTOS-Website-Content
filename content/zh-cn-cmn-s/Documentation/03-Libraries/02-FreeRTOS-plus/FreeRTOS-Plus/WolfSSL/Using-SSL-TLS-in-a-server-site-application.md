---
title: 简单 WolfSSL 服务器端示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


![在客户端 FreeRTOS 应用程序中使用 WolfSSL 的三个步骤](/media/2018/Server-Side-SSL-Usage.png)
*在服务器端应用程序中使用 WolfSSL 的三个步骤*


### 简介

此页面介绍了如何通过几个简单的步骤使用 WolfSSL 库，
来确保服务器端网络应用程序的安全性和完整性。

此页面上的信息与
[简单 WolfSSL 客户端示例](Using-SSL-TLS-in-a-client-site-application)
页面上的信息几乎相同。为保持一致，在这里重复这些内容，
并突出显示了存在的差异。


### 头文件

wolfssl/ssl.h 包含 WolfSSL 结构体、数据定义和函数
原型。该文件必须包含在所有使用
WolfSSL 库的源文件中。

```c
#include "wolfssl/ssl.h"

```
*所有使用 WolfSSL 库的源文件都必须包含的头文件*


### 初始化库并创建 WolfSSL 上下文

wolfSSL_Init() 准备 WolfSSL 库以供使用，并且必须
在任何其他 WolfSSL API 函数之前调用。

接下来，需要 WOLFSSL_CTX 类型的变量来存储上下文信息，
并且可使用 wolfSSL_CTX_new() 创建。要使用的 SSL 或 TLS 协议
在使用函数的参数创建上下文时
指定。选项包括 SSLv3、TLSv1、TLSv1.1、TLSv1.2  或 DTLS。
此示例演示了正在选择的 TLSv1 **服务器**协议（客户端
示例选择了 TLSv1 **客户端** ）。用户手册中
列出了用于选择其他协议选项的值。


客户端示例演示了将证书颁发机构 (CA) 文件
加载到 WolfSSL 上下文。除 CA 外，服务器上下文还必须
加载服务器证书和密钥文件。这允许服务器发送其
证书到客户端进行验证。
调用 wolfSSL_CTX_LOAD_VERIFY_LOCATIONS () 以加载 CA，
调用 wolfSSL_CTX_use_certificate_file () 以加载证书，
调用 wolfSSL_CTX_USE_PrivateKey_FILE 以加载私钥文件。

```c
/* Define a structure to hold the WolfSSL context. */
WOLFSSL_CTX* xWolfSSL_Context;

    /* Initialise WolfSSL. This must be done before any other WolfSSL functions
 are called. */
    wolfSSL_Init();

    /* Attempt to create a context that uses the TLS V1 server protocol. */
    xWolfSSL_Context = wolfSSL_CTX_new( CyaTLSv1_server_method() );

    if( xWolfSSL_Context != NULL )
    {
        /* Load the CA certificate. Real applications should ensure that
 wolfSSL_CTX_load_verify_locations() returns SSL_SUCCESS before proceeding. */
        wolfSSL_CTX_load_verify_locations( xWolfSSL_Context, "ca-cert.pem", 0 );

        /* Again, checking of the return values is omitted from this example,
 just for clarity. Real applications must ensure the following two
 functions return SSL_SUCCESS. */
        wolfSSL_CTX_use_certificate_file( xWolfSSL_Context, "server-cert.pem", SSL_FILETYPE_PEM );
        wolfSSL_CTX_use_PrivateKey_file( xWolfSSL_Context, "server-key.pem", SSL_FILETYPE_PEM );
    }

```
*库初始化、协议选择，以及将 CA 证书、
服务器证书和私钥加载到 WolfSSL 上下文中。*


### 将 WolfSSL 对象与已连接的套接字关联

每个可接受的连接必须与 WolfSSL 对象关联。
使用 wolfSSL_new() 创建 WolfSSL 对象，
使用 wolfSSL_set_fd() 将其与 TCP 套接字相关联。

```c
WOLFSSL* xWolfSSL_Object;

    /* A connection has been accepted by the server. Create a WolfSSL
       object for use with the newly connected socket. */
    xWolfSSL_Object = wolfSSL_new( xWolfSSL_Context );

    if( xWolfSSL_Object != NULL )
    {
        /* Associate the created WolfSSL object with the connected socket
           (sockfd). */
        wolfSSL_set_fd( xWolfSSL_Object, sockfd );
    }

```
*创建 WolfSSL 对象，并将其与已接受的连接关联起来*



### 使用套接字

如今要通过套接字实现通信安全，可以通过使用
wolfSSL_write() 代替标准套接字 write() 或 send() 函数，
以及使用 wolfSSL_read() 代替标准套接字 read() 或 recv()。

请注意，wolfSSL_write () 和 wolfSSL_read () 的第一个参数
不是套接字描述符，而是与套接字描述符关联的 WolfSSL
对象。

```c
char ucTxBuf[ MAXLINE ], ucRxBuf[ MAXLINE ];

    if( wolfSSL_write( xWolfSSL_Object, ucTxBuf, strlen( ucTxBuf ) ) != strlen( ucTxBuf ) )
    {
        /* Send failed. */
    }

    if( wolfSSL_read( xWolfSSL_Object, ucRxBuf, MAXLINE ) <= 0 )
    {
        /* Read failed. */
    }

```
*使用 WolfSSL API 写入和读取套接字*


### 删除分配的资源

导致动态资源分配的 WolfSSL API 函数有一个对应的函数，
不再需要资源时，应调用该函数来释放资源。
下述代码片段显示了应该如何释放在此小示例中创建的对象。

```c
    /* WolfSSL objects should be deleted when they are no longer required. */
    wolfSSL_free( xWolfSSL_Object );

    /* The WolfSSL context should be deleted if it is no longer required. However,
       because most deeply embedded applications will keep the context for the lifetime
       of the application, and only ever be restarted when the system is rebooted, it
       might be that the context is never explicitly freed. */
    wolfSSL_CTX_free( xWolfSSL_Context );

    /* The library itself should be shut down cleanly if it too is no longer
       required. Again, because most deeply embedded applications will require the
       library for the lifetime of the application, and only ever be restarted when
       the system is rebooted, it might be that the library is never explicitly closed. */
    wolfSSL_Cleanup();

```
*删除本示例中动态分配的对象*
