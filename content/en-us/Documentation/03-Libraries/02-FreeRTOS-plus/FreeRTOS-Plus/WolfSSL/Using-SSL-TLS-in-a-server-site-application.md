---
title: Simple WolfSSL Server Side Example
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


![The three steps to using WolfSSL in a client side FreeRTOS application](/media/2018/Server-Side-SSL-Usage.png)
*The three steps to using WolfSSL in a server side application*


### Introduction

This page describes how, in just a few easy steps, the WolfSSL library can be used to
to ensure the security and integrity of a server side networking application.

The information on this page is nearly identical to that found on
the [Simple WolfSSL Client Side Example](Using-SSL-TLS-in-a-client-site-application)
page. It is repeated here for consistency - with the differences highlighted
where they exist.


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
This example demonstrates the TLSv1 **server** protocol being selected (the client
side example selects TLSv1 **client**). The values
to use to select the other protocol options are listed in the user manual.


The client side example demonstrated a Certificate Authority (CA) file being
loaded into the WolfSSL context. In addition to the CA, the server context must also
be loaded with the server certificate, and a key file. This allows the server to send its
certificate to the client for verification.
wolfSSL\_CTX\_load\_verify\_locations() is called to load the CA,
wolfSSL\_CTX\_use\_certificate\_file() to load the certificate, and
wolfSSL\_CTX\_use\_PrivateKey\_file to load the private key file.

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
 wolfSSL\_CTX\_load\_verify\_locations() returns SSL\_SUCCESS before proceeding. */
        wolfSSL_CTX_load_verify_locations( xWolfSSL_Context, "ca-cert.pem", 0 );

        /* Again, checking of the return values is omitted from this example,
 just for clarity. Real applications must ensure the following two
 functions return SSL\_SUCCESS. */
        wolfSSL_CTX_use_certificate_file( xWolfSSL_Context, "server-cert.pem", SSL_FILETYPE_PEM );
        wolfSSL_CTX_use_PrivateKey_file( xWolfSSL_Context, "server-key.pem", SSL_FILETYPE_PEM );
    }
```
*Library initialisation, protocol selection, and loading the CA certificate,
server certificate and private key into the WolfSSL context.*


### Associating a WolfSSL object with a connected socket

Each accepted connection must be associated with a WolfSSL object.
WolfSSL objects are created using wolfSSL\_new(), and associated
with a TCP socket using wolfSSL\_set\_fd().

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
*Creating a WolfSSL object, and associating it with an accepted connection*


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
