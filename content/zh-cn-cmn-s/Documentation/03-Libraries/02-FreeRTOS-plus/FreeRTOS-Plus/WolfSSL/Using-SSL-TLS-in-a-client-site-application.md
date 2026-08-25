---
title: 简单 WolfSSL 客户端示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

![在客户端 FreeRTOS 应用程序中使用 WolfSSL 的三个步骤](/media/2018/Client-Side-SSL-Usage.png)   
*在客户端应用程序中使用 WolfSSL 的三个步骤*

### 引言

此页面介绍了如何通过几个简单的步骤使用 WoldSSL 库，
来确保客户端网络应用程序的安全性和完整性。
 
  
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
此示例演示了待选择的 TLSv1 客户端协议。用户手册中
列出了用于选择其他协议选项的值。

最后的初始化步骤是向 WolfSSL 上下文中加载一个
证书颁发机构 (CA)。这使得客户端能够与将要连接的服务器进行身份验证。
为此，可以使用 wolfSSL_CTX_load_verify_locations()
。在下面的示例中，第一个函数参数
指定上下文，CA 将加载到
该上下文中，第二个则是要使用 CA 证书的参数。第三个
参数可以用于指定将用来搜索证书的文件
路径，但在这种情况下，文件路径是不必要的，因此设置为 0。

```c
/* Define a structure to hold the WolfSSL context. */  
WOLFSSL_CTX* xWolfSSL_Context;  
  
    /* Initialise WolfSSL. This must be done before any other WolfSSL functions  
       are called. */  
    wolfSSL_Init();  
  
    /* Attempt to create a context that uses the TLS V1 client protocol. */  
    xWolfSSL_Context = wolfSSL_CTX_new( CyaTLSv1_client_method() );  
  
    if( xWolfSSL_Context != NULL )  
    {  
        /* Load the CA certificate. Real applications should ensure that  
           wolfSSL_CTX_load_verify_locations() returns SSL_SUCCESS before proceeding. */  
        wolfSSL_CTX_load_verify_locations( xWolfSSL_Context, "ca-cert.pem", 0 );  
    }  
  
```
*库初始化、协议选择和 CA 证书加载*


### 将 WolfSSL 对象与已连接的套接字关联

每个 TCP 连接必须与一个 WolfSSL 对象关联。
使用 wolfSSL_new() 创建 WolfSSL 对象，
使用 wolfSSL_set_fd() 将其与 TCP 套接字相关联。

```c
WOLFSSL* xWolfSSL_Object;  
  
    /* Standard Berkeley sockets connect function. */  
    if( connect( sockfd, (SA *) &servaddr, sizeof( servaddr ) ) == 0 )  
    {  
        /* The connect was successful. Create a WolfSSL object to associate with  
           this connection. The context created during initialisation is passed as  
           the function parameter. */  
        xWolfSSL_Object = wolfSSL_new( xWolfSSL_Context );  
  
        if( xWolfSSL_Object != NULL )  
        {  
            /* Associate the created WolfSSL object with the connected socket. */  
            wolfSSL_set_fd( xWolfSSL_Object, sockfd );  
        }  
    }  
  
```
*创建 WolfSSL 对象并将其与已连接的套接字关联*


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
