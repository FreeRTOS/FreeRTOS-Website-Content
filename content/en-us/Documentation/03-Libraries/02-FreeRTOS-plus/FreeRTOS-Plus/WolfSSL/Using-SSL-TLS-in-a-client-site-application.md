---
title: Simple WolfSSL Client Side Example
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

![The three steps to using WolfSSL in a client side FreeRTOS application](/media/2018/Client-Side-SSL-Usage.png)   
*The three steps to using WolfSSL in a client side application*


### Introduction

This page describes how, in just a few easy steps, the WolfSSL library can be used to
to ensure the security and integrity of a client side networking application.
 
  
### Header files

wolfssl/ssl.h contains the WolfSSL structures, data definitions, and function
prototypes. It must be included in all the source files that use the
WolfSSL library.

```c
#include "wolfssl/ssl.h"  
```
*The header file that must be included in all source files that use the WolfSSL library*


### Initialising the library and creating a WolfSSL context

wolfSSL\_Init() prepares the WolfSSL library for use, and must be
called before any other WolfSSL API functions.
 
Next, a variable of type WOLFSSL\_CTX is required to store context information,
and can be created using wolfSSL\_CTX\_new(). The SSL or TLS protocol
to use is specified as the context is created using the function's
parameter. Options include SSLv3, TLSv1, TLSv1.1, TLSv1.2, or DTLS.
This example demonstrates the TLSv1 client protocol being selected. The values
to use to select the other protocol options are listed in the user manual.
 
The final initialisation step is loading a
Certificate Authority (CA) into the WolfSSL context. This allows authentication with the server
the client will connect to. wolfSSL\_CTX\_load\_verify\_locations()
is used for this purpose. In the example below, the first function parameter
specifies the context into which the
CA is loaded, and the second the CA certificate that is used. The third
parameter can be used to specify a file path that will be searched for
certificates, but in this case the file path is not necessary and so set to 0.

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
*Library initialisation, protocol selection, and loading the CA certificate*


### Associating a WolfSSL object with a connected socket

Each TCP connection must be associated with a WolfSSL object.
WolfSSL objects are created using wolfSSL\_new(), and associated
with a TCP socket using wolfSSL\_set\_fd().

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
*Creating a WolfSSL object, and associating it with a connected socket*


### Using the socket

Secure communication can now be made through the socket by using
wolfSSL\_write() in place of the standard sockets write() or send() functions,
and wolfSSL\_read() in place of the standard sockets read() or recv().

Note that the first parameter to both wolfSSL\_write() and wolfSSL\_read()
is not the socket descriptor, but the WolfSSL object that is associated with
the socket descriptor.

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
*Writing to and reading from a socket using the WolfSSL API*


### Deleting allocated resources

WolfSSL API functions that result in dynamic resource allocation have a counterpart
function that should be called to free the resource when it is no longer required.
The code snippet below shows how the objects created in this small example should be freed.

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
*Deleting objects that were dynamically allocated in this example*
