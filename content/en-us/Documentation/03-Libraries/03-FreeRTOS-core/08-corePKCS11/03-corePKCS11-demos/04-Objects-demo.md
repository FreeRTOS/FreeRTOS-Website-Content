---
title: corePKCS11 Objects Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

* On this Page
	+ [Source Code Organization](#source-code-organization)
	+ [Configuring the Demo](#configuring-the-demo-project)
	+ [Building the Demo](#building-the-demo-project)
	+ [Functionality](#functionality)


## Introduction

This demo is the third in the corePKCS11 demo series. It introduces the section of the PKCS #11 API
used for managing objects. An object is defined as "An item that is stored on a token. May be data, a
certificate, or a key." This demo will give an overview of how PKCS #11 can be used to abstract some
commonly used objects. This interface is particularly useful because it is very portable and flexible.
Using PKCS #11 to manipulate these objects benefits security because it reduces the scope of attack on
the objects to a module that is specialized for cryptographic operations and protecting objects.

**Note:** This demo will write a public and private EC key to the Windows file system. They will both be
 contained in a binary formatted file called "`FreeRTOS_P11_Key.dat`". The sign and verify demo has a direct
 dependency on this file, and will not work without it.

The PKCS #11 standard can be found [here](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html).

The corePKCS11 demo projects use the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so they can be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on Windows
without the need for any particular MCU hardware.

The set of functions presented in this demo are categorized as:

* Object Management Functions


## Source Code Organization

The Visual Studio solution for the PKCS #11 based mutual authentication demo is called `pkcs11\_demo.sln`
and is located in the `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\` directory of the main
FreeRTOS download.

[![](/media/2020/PKCS11-Source-Code-Organization.png)](/media/2020/PKCS11-Source-Code-Organization.png)
*Click to enlarge*


## Configuring the Demo Project

To configure the demo project, set `configPKCS11\_OBJECT\_DEMO` to 1 in `pkcs11\_demo\_config.h`. This
is enabled by default. After you complete this, the demo can be run, there are no other configuration
steps required for this demo.


## Building the Demo Project

The demo project uses the  [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).

1. Open the `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11_Windows_Simulator\pkcs11_demo.sln` Visual Studio
   solution file from within the Visual Studio IDE.
2. Select '`build solution`' from the IDE's '`build`' menu.


## Functionality

Once enabled, this demo's entry point is `vPKCS11ObjectDemo`. Currently, the demo is split into two
smaller demos: `prvObjectImporting` shows how to import an object into a PKCS #11 module
and `prvObjectGeneration` shows how to generate objects within the PKCS #11 module.

It is more secure to generate credentials directly on the IoT device because the credentials will not
be exposed to any external system. It is even more secure if the IoT device has a secure element. Secure
elements are specialty chips that protect sensitive data such as private keys. They provide extra protection
against attackers who might attempt to extract an IoT device's private key. Simply storing a private key
in flash memory is not safe.

The demo shows how to import a certificate into a PKCS #11 stack. This is useful because it allows you
to store certificates from any server your application wishes to trust. A template is an array of CK\_ATTRIBUTE's
that describes an object.


### Creating an X.509 certificate template:

```c
/* The PKCS11_CertificateTemplate_t is a custom struct defined in "iot\_pkcs11.h"
 * in order to make it easier to import a certificate. This struct will be
 * populated with the parameters necessary to import the certificate into the
 * Cryptoki library.
 */
PKCS11_CertificateTemplate_t xCertificateTemplate;

/* The object class is specified as a certificate to help the Cryptoki library
 * parse the arguments.
 */
CK_OBJECT_CLASS xCertificateClass = CKO_CERTIFICATE;

/* The certificate type is x509, which is the only type
 * supported by this stack. To read more about x509 certificates, use
 * the following links:
 *
 * https://en.wikipedia.org/wiki/X.509
 * https://www.ssl.com/faqs/what-is-an-x-509-certificate/
 *
 */
CK_CERTIFICATE_TYPE xCertificateType = CKC_X_509;

/* The label will help the application identify which object it wants
 * to access.
 */
CK_BYTE pucLabel[] = pkcs11configLABEL_DEVICE_CERTIFICATE_FOR_TLS;

/* Specify certificate class. */
xCertificateTemplate.xObjectClass.type = CKA_CLASS;
xCertificateTemplate.xObjectClass.pValue = &xCertificateClass;
xCertificateTemplate.xObjectClass.ulValueLen = sizeof( xCertificateClass );

/* Specify certificate subject. */
xCertificateTemplate.xSubject.type = CKA_SUBJECT;
xCertificateTemplate.xSubject.pValue = xSubject;
xCertificateTemplate.xSubject.ulValueLen = strlen( ( const char * ) xSubject );

/* Point to contents of certificate. */
xCertificateTemplate.xValue.type = CKA_VALUE;
xCertificateTemplate.xValue.pValue = ( CK_VOID_PTR ) pkcs11demo_RSA_CERTIFICATE;
xCertificateTemplate.xValue.ulValueLen = ( CK_ULONG ) sizeof( pkcs11demo_RSA_CERTIFICATE );

/* Specify certificate label. */
xCertificateTemplate.xLabel.type = CKA_LABEL;
xCertificateTemplate.xLabel.pValue = ( CK_VOID_PTR ) pucLabel;
xCertificateTemplate.xLabel.ulValueLen = strlen( ( const char * ) pucLabel );

/* Specify certificate type as x509. */
xCertificateTemplate.xCertificateType.type = CKA_CERTIFICATE_TYPE;
xCertificateTemplate.xCertificateType.pValue = &xCertificateType;
xCertificateTemplate.xCertificateType.ulValueLen = sizeof( CK_CERTIFICATE_TYPE );

/* Specify that the certificate should be on a token. */
xCertificateTemplate.xTokenObject.type = CKA_TOKEN;
xCertificateTemplate.xTokenObject.pValue = &xTokenStorage;
xCertificateTemplate.xTokenObject.ulValueLen = sizeof( xTokenStorage );
```

After the template has been created it can be passed to `C_CreateObject`, along with the number of entries
in the array. The PKCS #11 module will parse the arguments and return `CKR_OK` if it is able to create the
x509 certificate. This method is a good way to import well known certificates into the PKCS #11 module.


### Creating a X.509 certificate:

```c
/* Once the Cryptoki library has finished importing the new certificate
 * a CK_OBJECT_HANDLE is associated with it. The application can now use this
 * to refer to the object in following operations.
 *
 * xCertHandle in the below example will have its value modified to
 * be the CK_OBJECT_HANDLE.
 *
 * To compare the hard coded x509, in PEM format, with the DER formatted
 * x509 certificate that is created by the Cryptoki library, use the following
 * OpenSSL command:
 * "$ openssl x509 -in FreeRTOS_P11_Certificate.dat -inform der -text"
 *
 * See this explanation for the difference between the PEM format and the
 * DER format:
 * <https://stackoverflow.com/questions/22743415/what-are-the-differences-between-pem-cer-and-der/22743616>
 *
 */
xResult = pxFunctionList->C_CreateObject( hSession,
                                          ( CK_ATTRIBUTE_PTR ) &xCertificateTemplate,
                                          sizeof( xCertificateTemplate ) / sizeof( CK_ATTRIBUTE ),
                                          &xCertHandle );

configASSERT( xResult == CKR_OK );
configASSERT( xCertHandle != CK_INVALID_HANDLE );
```

The second half of the demo covers how to generate a key pair using PKCS #11. This method is preferable
because the application is never exposed to the memory that contains the private key. This reduces the
potential ways an attacker could extract the private key, since it was never actually stored outside of
the PKCS #11 module.

Once again, a template is used to generate the keys in the following code.


### Creating a key pair generation template:

```c
/* CK_ATTTRIBUTE's contain an attribute type, a value, and the length of
 * the value. An array of CK_ATTRIBUTEs is called a template. They are used
 * to create, search for, and manipulate objects. The order of the
 * template does not matter.
 *
 * In the below template we create a public key:
 * Specify the key type as EC.
 * The key will be able to verify a message.
 * Specify the EC Curve.
 * Assign a label to the object that will be created.
 */
CK_ATTRIBUTE xPublicKeyTemplate[] =
{
    { CKA_KEY_TYPE, &xKeyType, sizeof( xKeyType ) },
    { CKA_VERIFY, &xTrue, sizeof( xTrue ) },
    { CKA_EC_PARAMS, xEcParams, sizeof( xEcParams ) },
    { CKA_LABEL, pucPublicKeyLabel, sizeof( pucPublicKeyLabel ) - 1 }
};

/* In the below template we create a private key:
 * The key type is EC.
 * The key is a token object.
 * The key will be a private key.
 * The key will be able to sign messages.
 * Assign a label to the object that will be created.
 */
CK_ATTRIBUTE xPrivateKeyTemplate[] =
{
    { CKA_KEY_TYPE, &xKeyType, sizeof( xKeyType ) },
    { CKA_TOKEN, &xTrue, sizeof( xTrue ) },
    { CKA_PRIVATE, &xTrue, sizeof( xTrue ) },
    { CKA_SIGN, &xTrue, sizeof( xTrue ) },
    { CKA_LABEL, pucPrivateKeyLabel, sizeof( pucPrivateKeyLabel ) - 1 }
};
```

Finally, this template is created and when it is passed it to `C_GenerateKeyPair` a new key pair will be
created by the PKCS #11 module.


### Creating a key pair:

```c
/* This function will generate a new EC private and public key pair. You can
 * use " $openssl ec -inform der -in FreeRTOS_P11_Key.dat -text " to see
 * the structure of the keys that were generated.
 */
xResult = pxFunctionList->C_GenerateKeyPair( hSession,
                                             &xMechanism,
                                             xPublicKeyTemplate,
                                             sizeof( xPublicKeyTemplate ) / sizeof( CK_ATTRIBUTE ),
                                             xPrivateKeyTemplate,
                                             sizeof( xPrivateKeyTemplate ) / sizeof( CK_ATTRIBUTE ),
                                             &xPublicKeyHandle,
                                             &xPrivateKeyHandle );
configASSERT( xResult == CKR_OK );
```
