---
title: corePKCS11 Management And Random Numbers Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


* On this Page
    + [Introduction](#introduction)
    + [Source Code Organization](#source-code-organization)
    + [Configuring the Demo Project](#configuring-the-demo-project)
    + [Building the Demo Project](#building-the-demo-project)
    + [Functionality](#functionality)


## Introduction

This demo is the first in the corePKCS11 demo series. It covers the section of the PKCS #11 API that
manages the PKCS #11 stack, and shows how PKCS #11 can be used to generate random numbers. The PKCS #11
standard can be found [here](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html).

These demos and their associated web pages use the terms defined by PKCS #11 interchangeably with the
terms PKCS #11 API, stack, standard, etc. To summarize the terminology defined in the standard, "Cryptoki"
refers to the Cryptographic Token Interface that is defined in the PKCS #11 standard, that is, the PKCS #11
API or functions. An implementation of Cryptoki is referred to as a "Cryptoki library"; this would be
equivalent to the terms "PKCS #11 implementation" or "PKCS #11 stack".

The PKCS #11 specification is distributed as three header files:


**pkcs11.h**
This is the main header file, and is the only one an application needs to include. It requires some
macros to be defined before it is included, and those definitions can be found
in "core\_pkcs11.h" (see `<freertos>/libraries/freertos_plus/source/corepkcs11/include/core_pkcs11.h`).
So, when you include the PKCS #11 library, include "core\_pkcs11.h" first, and then "pkcs11.h".

**pkcs11f.h**
This contains function prototypes.

**pkcs11t.h**
This contains the various types as defined in the PKCS #11 specification.

The PKCS #11 demo projects use
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so they can be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on Windows
without the need for any particular MCU hardware.

The set of functions presented in this demo are categorized as:

+ General Purpose Functions
  + Slot and Token Management Functions
  + Session Management Functions
  + Random Number Generation Functions


## Source Code Organization

The Visual Studio solution for the PKCS #11 based mutual authentication demo is called `pkcs11_demo.sln`
and is located in the `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11_Windows_Simulator\` directory of the main
FreeRTOS download.

[![](/media/2020/PKCS11-Source-Code-Organization.png)](/media/2020/PKCS11-Source-Code-Organization.png)
*Click to enlarge*


## Configuring the Demo Project

To configure the demo project, set `configPKCS11\_MANAGEMENT\_AND\_RNG\_DEMO` to 1 in `pkcs11\_demo\_config.h`.


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).

1. In the Visual Studio IDE, open the Visual Studio solution
   file `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11_Windows_Simulator\pkcs11_demos.sln`.
2. Select '**build solution**' from the IDE's '**build**' menu.


## Functionality

The entry point for this demo is **vPKCS11ManagementAndRNGDemo**. This function outlines the basics of
how to start up a PKCS #11 session and use it to generate a random number.

The first step is to acquire a function pointer structure that contains pointers to those functions
the PKCS #11 stack has implemented. Functions that are not implemented are always NULL. This is useful
because some PKCS #11 implementations may not define every function. The demos will assert on functions
that are not implemented. It may be useful in a real application to account for this situation in order
to make a library compatible between different PKCS #11 implementations.


### Getting a PKCS #11 function list:

```c
/* The CK\_FUNCTION\_LIST is a structure that contains the Cryptoki version
 * and a function pointer to each function in the Cryptoki API. If the
 * function pointer is NULL it is unimplemented.
 */
CK_FUNCTION_LIST_PTR pxFunctionList = NULL;

/* We use the function list returned by C\_GetFunctionList to see what functions
 * the Cryptoki library supports. We use asserts to ensure that all the
 * functionality needed in this demo is available.
 */
xResult = C_GetFunctionList( &pxFunctionList );
configASSERT( xResult == CKR_OK );
configASSERT( pxFunctionList != NULL );
configASSERT( pxFunctionList->C_Initialize != NULL );
configASSERT( pxFunctionList->C_GetSlotList != NULL );
configASSERT( pxFunctionList->C_OpenSession != NULL );
configASSERT( pxFunctionList->C_Login != NULL );
configASSERT( pxFunctionList->C_GenerateRandom != NULL );
configASSERT( pxFunctionList->C_CloseSession != NULL );
configASSERT( pxFunctionList->C_Finalize != NULL );
```

After the functions are acquired from the PKCS #11 implementation, the PKCS#11 implementation can be
initialized with a call to `C_Initialize`. This function makes no guarantees about thread safety, and
you should be careful to consider concurrency when making this call. The PKCS #11 stack used by the
demo does not implement the thread safety mechanisms that are in the specification. So it may be worth
revisiting any code that calls `C_Initialize` when using a different PKCS #11 stack, to ensure concurrency
is handled properly.


### Initializing the PKCS #11 stack:

```c
/* This Cryptoki library does not implement any initialization arguments. At the time of
 * writing this demo, the purpose of these optional arguments is to provide
 * function pointers for mutex operations.
 */
CK_C_INITIALIZE_ARGS xInitArgs = { 0 };

/* C_Initialize will initialize the Cryptoki library and the hardware it
 * abstracts.
 */
xResult = pxFunctionList->C_Initialize( &xInitArgs );
configASSERT( xResult == CKR_OK );
```

When initialized, we query for a slot that can be used by the application. A slot is defined by PKCS #11
as "A logical reader that potentially contains a token". The demo will always use the first slot returned
by `C_GetSlotList`, because the implementation that it was written for only has one slot. The slot allows
the application to specify which token to use. Many implementations vary in the relationship of slots to
tokens. The main point is that the SlotID will specify which token we would like to use for the application
session.


### Selecting a slot:

```c
/* A slot ID is an integer that defines a slot. The Cryptoki definition of
 * a slot is "A logical reader that potentially contains a token."
 *
 * Essentially it is an abstraction for accessing the token. The reason for
 * this is some tokens are a physical "card' that needs to be inserted into
 * a slot for the device to read.
 *
 * A concrete example of a slot could be a USB Hardware Security Module (HSM),
 * which generally appears as a singular slot, and abstracts it's internal "token".
 *
 * Some implementations have multiple slots mapped to a single token, or maps
 * a slot per token.
 */
CK_SLOT_ID * pxSlotId = NULL;

/* CK_ULONG is a long unsigned integer as defined by PKCS #11. */
CK_ULONG xSlotCount = 0;

/* C_GetSlotList will retrieve an array of CK_SLOT_IDs.
 * This Cryptoki library does not implement slots, but it is important to
 * highlight how Cryptoki can be used to interface with real hardware.
 *
 * By setting the first argument "tokenPresent" to true, we only retrieve
 * slots that have a token. If the second argument "pSlotList" is NULL, the
 * third argument "pulCount" will be modified to contain the total slots.
 */
xResult = pxFunctionList->C_GetSlotList( CK_TRUE,
                                         NULL,
                                         &xSlotCount );
configASSERT( xResult == CKR_OK );

/* Since C_GetSlotList does not allocate the memory itself for getting a list
 * of CK_SLOT_ID, we allocate one for it to populate with the list of
 * slot ids.
 */
pxSlotId = pvPortMalloc( sizeof( CK_SLOT_ID ) * ( xSlotCount ) );
configASSERT( pxSlotId != NULL );

/* Now since pSlotList is not NULL, C_GetSlotList will populate it with the
 * available slots.
 */
xResult = pxFunctionList->C_GetSlotList( CK_TRUE,
                                         pxSlotId,
                                         &xSlotCount );
configASSERT( xResult == CKR_OK );
```

The next step is to create a session that connects the application to the slot returned by the PKCS #11
stack. The specification defines a session to be "The logical connection between an application and a token."
Once again, this is explained further in the source code and the PKCS #11 specification. The session is
established by calling `C_OpenSession`, and specifying which slot the application would like to use.


### Opening a PKCS #11 session:

```c
/* A session is defined to be "The logical connection between an application
 * and a token."
 *
 * The session can either be private or public, and differentiates
 * your application from the other users of the token.
 */
CK_SESSION_HANDLE hSession = CK_INVALID_HANDLE;

/* Since this Cryptoki library does not actually implement the concept of slots,
 * but we will use the first available slot, so the demo code conforms to
 * Cryptoki.
 *
 * C_OpenSession will establish a session between the application and
 * the token and we can then use the returned CK_SESSION_HANDLE for
 * cryptographic operations with the token.
 *
 * For legacy reasons, Cryptoki demands that the CKF_SERIAL_SESSION bit
 * is always set.
 */
xResult = pxFunctionList->C_OpenSession( pxSlotId[0],
                                         CKF_SERIAL_SESSION | CKF_RW_SESSION,
                                         NULL, /* Application defined pointer. */
                                         NULL, /* Callback function. */
                                         &hSession );
configASSERT( xResult == CKR_OK );
```

Now that the session is established, we can use it to generate a random number. Random numbers are used
heavily in cryptographic operations, and many algorithms used in cryptography rely on the "randomness"
of a random number generator to make sure the cipher isn't broken.


### Generating a buffer of random numbers:

```c
/* CK_BYTE is a PKCS #11 type that is defined as an unsigned char. */
CK_BYTE xRandomData[ 10 ] = { 0 };

/* C_GenerateRandom generates random or pseudo random data. As arguments it
 * takes the application session, and a pointer to a byte buffer, as well as
 * the length of the byte buffer. Then it will fill this buffer with random
 * bytes.
 */
xResult = pxFunctionList->C_GenerateRandom( hSession,
                                            xRandomData,
                                            sizeof( xRandomData ) );
configASSERT( xResult == CKR_OK );

for( ulIndex = 0; ulIndex < sizeof( xRandomData ); ulIndex++ )
{
    configPRINTF( ( "Generated random number: %x\r\n", xRandomData[ ulIndex ] ) );
}
```

Since the cryptographic operation is now complete, the demo cleans up the resources with these steps:

1. close the active session,
2. call `C_Finalize` to de-initialize the PKCS #11 stack.


### Cleaning up:

```c
/* C_CloseSession closes the session that was established between the
 * application and the token. This will clean up the resources that maintained
 * the link between the application and the token. If the application wishes
 * to use the token again, it will need to open a new session.
 */
xResult = pxFunctionList->C_CloseSession( hSession );
configASSERT( xResult == CKR_OK );

/* C_Finalize signals to the Cryptoki library that the application is done
 * using it. It should always be the last call to the Cryptoki library.
 * NULL should always be passed as the argument, as the parameter is currently
 * just reserved for future revisions.
 *
 * Calling this function in a multi threaded environment can lead to undefined
 * behavior if other threads are accessing the Cryptoki library.
 */
xResult = pxFunctionList->C_Finalize( NULL );
configASSERT( xResult == CKR_OK );
```
