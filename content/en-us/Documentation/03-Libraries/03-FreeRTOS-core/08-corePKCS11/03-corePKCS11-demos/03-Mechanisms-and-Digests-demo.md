---
title: corePKCS11 Mechanisms And Digests Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

* On this Page
	+ [Source Code Organization](#source-code-organization)
	+ [Configuring the Demo Project](#configuring-the-demo-project)
	+ [Building the Demo Project](#building-the-demo-project)
	+ [Functionality](#functionality)

		- [Querying for digest capabilities](#querying-for-digest-capabilities)
		- [Creating a digest](#creating-a-digest)
		- [Using OpenSSL](#using-openssl)
		- [Using the Python3 shell](#using-the-python3-shell)


## Introduction

This demo is the second in the corePKCS11 demo series. It introduces the section of the PKCS #11 API
used to query the capabilities of a PKCS #11 slot and to create a message digest with that slot. The
PKCS #11 standard can be found [here](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html).
A slot is an interface that a token can be placed in. A token is a hardware device that is specialized
for cryptographic operations, such as holding keys, generating keys, and providing hardware acceleration
of common operations, such as creating an SHA digest.

The corePKCS11 demo projects use
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so they can be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on Windows
without the need for any particular MCU hardware.

The set of functions presented in this demo are categorized as:

* Slot and token management functions
* Message digest functions


### Source Code Organization

The Visual Studio solution for the corePKCS11 based mutual authentication demo is called `pkcs11\_demo.sln`
and is located in the `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\` directory of the main
FreeRTOS download.

[![](/media/2020/PKCS11-Source-Code-Organization.png)](/media/2020/PKCS11-Source-Code-Organization.png)
*Click to enlarge*


## Configuring the Demo Project

To configure the demo project, set `configPKCS11\_MECHANISMS\_AND\_DIGESTS\_DEMO` to 1 in `pkcs11\_demo\_config.h`.


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).

1. Open the `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\pkcs11\_demos.sln` Visual Studio
   solution file from within the Visual Studio IDE.

2. Select 'build solution' from the IDE's 'build' menu.


## Functionality

Once enabled, this demo's entry point is `vPKCS11MechanismsAndDigestDemo`. The purpose of this demo
is to query a slot for its capabilities and then use the slot to generate a digest. The ability to query
for a token's capabilities at run time allows for more flexibility when swapping tokens in and out of a
slot. Most of the time, the token will remain in the slot, but if it is removed then the capabilities
will potentially change. For this demo, the SHA-256 algorithm is used to create the digest.


### Querying for digest capabilities:

```c
/* The PKCS #11 standard defines a mechanism to be a "A process for
 * implementing a cryptographic operation." For example, the SHA-256 algorithm
 * will be the mechanism used in this demo to perform a digest (hash operation).
 *
 * The mechanism types are defined in "pkcs11t.h", and are prefixed CKM\_, to
 * provide a portable way to identify mechanisms.
 */
CK_MECHANISM_TYPE xMechanismType = 0;

/* The CK_MECHANISM_INFO allows the application to retrieve the minimum and
 * maximum key sizes supported by the mechanism (could be in bits or bytes).
 * The structure also has a flags field that is populated with bit flags
 * for what features the mechanism supports.
 */
CK_MECHANISM_INFO MechanismInfo = { 0 };

xResult = pxFunctionList->C_GetMechanismInfo( pxSlotId[ 0 ],
                                              CKM_SHA256,
                                              MechanismInfo );
configASSERT( CKR_OK == xResult );

if( 0 != ( CKF_DIGEST & MechanismInfo.flags ) )
{
    configPRINTF( ( "The Cryptoki library supports the " \
    "SHA-256 algorithm.\r\n" ) );
}
else
{
    configPRINTF( ( "The Cryptoki library doesn't support the " \
    "SHA-256 algorithm.\r\n" ) );
}
```

Creating a hash is a very common operation that serves many purposes. For example, Git uses hashes to
uniquely identify commits. A Python dictionary, which uses a hash of each key value for faster lookup,
is another example. Cryptographic operations use hashes to verify the integrity of a message or correspondence.
Usually, they are combined with a signature in order to verify the integrity of the message and the sender
of the message. Signatures will be covered in the Sign and Verify demo page.

Although digest operations don't require any particular hardware, they are still included in PKCS #11
to permit creation of an independent and full featured module for all cryptographic operations. This
helps reduce the scope of vulnerabilities and makes it easier to test the application. Since hashes are
commonly used in cryptographic operations, such as a TLS handshake, vulnerabilities in the hashing algorithm
can lead to leaked secrets and lost data. To help prevent that, PKCS #11 enables you to implement the entire
functionality needed for cryptographic operations in its own module. This allows you to create a standalone
module that is secure and whose security properties can be independently verified. And this allows an
application to protect sensitive data.

The process of generating a digest with PKCS #11 is broken up into three steps. First, the mechanism
for creating the digest is passed to PKCS #11 with `C\_DigestInit()`. Then, the buffer containing the
message, and its length is passed with `C\_DigestUpdate()`. Finally, the hash is created and placed in
a buffer with a call to `C\_DigestFinal()`.


### Creating a digest:

```c
/* Hash with SHA256 mechanism. */
xDigestMechanism.mechanism = CKM_SHA256;

/* Initializes the digest operation and sets what mechanism will be used
* for the digest. */
xResult = pxFunctionList->C_DigestInit( hSession,
                                        xDigestMechanism );
configASSERT( CKR_OK == xResult );

/* Pass a pointer to the buffer of bytes to be hashed, and its size. */
xResult = pxFunctionList->C_DigestUpdate( hSession,
                                          pxKownMessage,
                                          sizeof( pxKownMessage ) - 1 );
configASSERT( CKR_OK == xResult );

/* Retrieve the digest buffer. Since the mechanism is an SHA-256 algorithm,
* the size will always be 32 bytes. If the size cannot be known ahead of time,
* a NULL value to the second parameter xDigestResult, will set the third parameter,
* pulDigestLen to the number of required bytes. */
xResult = pxFunctionList->C_DigestFinal( hSession,
                                         xDigestResult,
                                         ulDigestLength );
configASSERT( CKR_OK == xResult );
```

An interesting exercise is to compare the hash generated by the PKCS #11 operation with one that is
generated by a different tool's implementation of SHA-256. OpenSSL is supported on most Linux distributions,
MacOS, and Windows. See the OpenSSL instructions for installation on your platform.

Generally, it is installed on most devices because it is commonly used to establish TLS connections.
Alternatively, the hashlib module is a part of the Python3 standard library, and can be used across
platforms on devices that support Python3.


### Using OpenSSL:

```c
#The "n" flag is set to strip new line characters.
$ echo -n "Hello world\ | openssl dgst -sha256
```


### Using the Python3 shell:

```c
>>> import hashlib
>>> hashlib.sha256("Hello world!".encode("utf8")).hexdigest()
```
The output of both, as well as the output of the demo, should
be: "c0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a". After you have generated the
hash values, they can be compared in order to verify the message is indeed "Hello world!".
