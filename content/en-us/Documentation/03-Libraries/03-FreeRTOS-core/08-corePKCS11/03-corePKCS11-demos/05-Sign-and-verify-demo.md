---
title: corePKCS11 Sign And Verify Demo
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


## Introduction

This demo is the fourth in the corePKCS11 demo series. It introduces the section of the PKCS #11 API
that is used to sign messages and verify the signature of messages. The PKCS #11 standard can be
found [here](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html).

The corePKCS11 demo projects use
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so they can be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on Windows
without the need for any particular MCU hardware.

The set of functions presented in this demo are categorized as:

* Object Management Functions
* Signing and MACing Functions


### Source Code Organization

The Visual Studio solution for the PKCS #11 based mutual authentication demo is called `pkcs11\_demos.sln`
and is located in the `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\` directory of the main
FreeRTOS download.

[![](/media/2020/PKCS11-Source-Code-Organization.png)](/media/2020/PKCS11-Source-Code-Organization.png)
*Click to enlarge*


## Configuring the Demo Project

To configure the demo project, set `configPKCS11_SIGN_AND_VERIFY_DEMO` to 1 in `pkcs11_demo_config.h`.
This is enabled by default. Once you complete this, the demo can be run, there is no other configuration
required for this demo.


## Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).

1. Open the `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\pkcs11\_demos.sln`
   Visual Studio solution file from within the Visual Studio IDE.
2. Select **'build solution'** from the IDE's **'build'** menu.


## Functionality

The entry point for this demo is `vPKCS11SignVerifyDemo`. Note that this demo requires the public and
private key pair created by the `prvObjectGeneration` function in the objects demo.

The demo will use this key pair to sign a message's digest. (See the Mechanisms and Digests demo for how
to create a digest.) The demo will also introduce some helpful functions, found in the "core\_pkcs11.h"
header file, that can be used to streamline some of the functionality demonstrated in the previous demos.

The first step is to find the object handles for the private and public keys that were generated in the Objects demo.


### Finding the proper object handles

```c
/* This function will:
 * Find an object, given it's label.
 *
 * This is done using the FindObjects group of functions defined as
 * "Object Management Functions" in PKCS #11.
 *
 * This will acquire the object handle for the private key created in the
 * "objects.c" demo.
 */

xResult = xFindObjectWithLabelAndClass( hSession,
                                        pkcs11configLABEL_DEVICE_PRIVATE_KEY_FOR_TLS,
                                        CKO_PRIVATE_KEY,
                                        &xPrivateKeyHandle );
configASSERT( xResult == CKR_OK );
configASSERT( xPrivateKeyHandle != CK_INVALID_HANDLE );

/* Acquire the object handle for the public key created in the "objects.c"
 * demo. */
xResult = xFindObjectWithLabelAndClass( hSession,
                                        pkcs11configLABEL_DEVICE_PUBLIC_KEY_FOR_TLS,
                                        CKO_PRIVATE_KEY,
                                        &xPublicKeyHandle );
configASSERT( xResult == CKR_OK );
configASSERT( xPublicKeyHandle != CK_INVALID_HANDLE );
```
Now that the object handles have been found, they can be used to sign a message digest and verify the
signature. A private key should always be protected because it can be used to sign a message, which allows
the recipient to verify that the holder of the private key was really the one who wrote the message. Anyone
who has a public key generated from the private key, and uses it to validate a message, must be able to
assume that it is, in fact, a valid message from a known sender.


### Creating a signature

```c
/* Initializes the sign operation and sets what mechanism will be used
 * for signing the message digest. Specify what object handle to use for this
 * operation, in this case the private key object handle.
 */

xResult = pxFunctionList->C_SignInit( hSession,
                                      &xMechanism,
                                      xPrivateKeyHandle );
configASSERT( xResult == CKR_OK );

/* Sign the message digest that was created with the C\_Digest series of
 * functions. A signature will be created using the private key specified in
 * C_SignInit and put in the byte buffer xSignature. */

xResult = pxFunctionList->C_Sign( hSession,
                                  xDigestResult,
                                  pkcs11SHA256_DIGEST_LENGTH,
                                  xSignature,
                                  &xSignatureLength );
configASSERT( xResult == CKR_OK );
configASSERT( xSignatureLength == pkcs11ECDSA_P256_SIGNATURE_LENGTH );
```

The next step is to use the public key to make sure the PKCS #11 stack can trust that the message we
received was from the sender. (The public key was derived from the private key that was used to create
the message signature.) This will be done by using the PKCS #11 stack to verify the buffer that contains
the signature.


### Verifying a signature

```c
/* Verify the signature created by C_Sign. First we will verify that the
 * same Cryptoki library was able to trust itself.
 *
 * C_VerifyInit will begin the verify operation, by specifying what mechanism
 * to use (CKM_ECDSA, the same as the sign operation) and then specifying
 * which public key handle to use.
 */

xResult = pxFunctionList->C_VerifyInit( hSession,
                                        &xMechanism,
                                        xPublicKeyHandle );

configASSERT( xResult == CKR_OK );

/* Given the signature and its length, the Cryptoki will use the public key
 * to see if the sender can be trusted. If C_Verify returns CKR_OK, it means
 * that the sender of the message has the same private key as the private key
 * that was used to generate the public key, and we can trust that the
 * message we received was from that sender.
 *
 * Note that we are not using the actual message, but the digest that we
 * created earlier of the message, for the verification.
 */

xResult = pxFunctionList->C_Verify( hSession,
                                    xDigestResult,
                                    pkcs11SHA256_DIGEST_LENGTH,
                                    xSignature,
                                    xSignatureLength );

if( xResult == CKR_OK )
{
    configPRINTF( ( "The signature of the digest was verified with the" \
                    " public key and can be trusted.\r\n" ) );
} else
{
    configPRINTF( ( "Unable to verify the signature with the given public" \
                    " key, the message cannot be trusted.\r\n" ) );
}
```


### How to Verify the signature in the terminal

The demo will output the contents of the signature buffer, and the hex format of the public key that
can be used to verify the signature.

![](/media/2020/pkcs11_sign_verify_demo-300x224.png)


### Extracting the public key

Follow these steps to export the public key from the binary file it is contained in.

1. Export the public key as hex bytes and print the hex representation of the public key. The demo will
   print the hex bytes to the console.

2. Create an empty text file called "`DevicePublicKeyAsciiHex.txt`".

3. Copy and paste the hex value of the public key into this text file.

4. Convert the hex file to binary using the xxd tool:

   ```c
   $ xxd -r -ps DevicePublicKeyAsciiHex.txt DevicePublicKeyDer.bin
   ```

   xxd will take a text file that contains hex data and output a binary of the hex in the file. See "`$ man xxd`"
   for more information about xxd.

5. Convert the binary encoding of the public key to PEM format:

   ```c
   $ openssl ec -inform der -in DevicePublicKeyDer.bin -pubin -pubout -outform pem -out public_key.pem
   ```

   We now have extracted the public key and can use it to verify signatures generated by the PKCS #11 stack.


### Extracting the signature

1. Create an empty text file called "`signature.txt`".

2. Copy and paste the signature buffer that was written to the console by the demo.

3. Convert the signature to a binary format.

   ```c
   $ xxd -r -ps signature.txt signature.bin
   ```

**WARNING: Running the object generation demo will create a new key pair and make it necessary to redo these steps!**


#### Verifying the Signature using OpenSSL

OpenSSL can be used to verify that the signature is trustworthy, and that the PKCS #11 stack is behaving
as expected. OpenSSL is a widely used crypto kit that provides much helpful functionality. The command below
uses the extracted public key to verify the binary signature created by the PKCS #11 stack.

```c
$ openssl dgst -sha256 -verify public_key.pem -signature signature.bin msg.txt
```
