---
title: PKCS #11 Functions
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[PKCS #11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) includes many functions and supports a variety of use cases. The FreeRTOS PKCS #11
library only implements a small subset of functions for the use cases first describe.  Each function is
fully documented in the [PKCS #11 standard](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html). 
The terminology can be difficult for the first reader, so we also provide examples code below.

PKCS #11 operational functions:
* C\_Random.  Random numbers are required by the TCP/IP stack (for example, when selecting an initial
  sequence number), within cryptographic algorithms, and during
  the [TLS handshake](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_handshake).

* C\_Sign.  Signing a message sent to another network node allows that node to identify the messages
  true origin.

* C\_FindObject.  Finds an object managed by PKCS #11, for example the [client certificate](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/04-X509-certificates).

* C\_GetAttributeValue.  This API gets the value of an object's attribute, for example if the object is
  a key type or a certificate type.


PKCS #11 administrative functions:
* C\_Initialize.  Initializes the crypto libraries.
* C\_Finalize.  Cleans up resources used by the crypto libraries.
* C\_OpenSession. Opens a session (or connection) between a software application and a particular crypto token.
* C\_CloseSession.  Closes the session opened by C\_OpenSession.
* C\_Login.  Logs into a token.
* C\_GetFunctionList.  Obtains a struct containing function pointers for use in calling the PKCS #11 APIs.
* C\_GetSlotList. Obtains the list of slots, which can be used to access any token in a slot.


### Code Samples

Here are some example code snippets that showcase how one might use the PKCS #11 API.


#### Using C\_GenerateRandom:

This code snippet shows how to use PKCS #11 to get a random number. For example, this function can be
used for FreeRTOS-Plus-TCP to generate random TCP numbers.

```c
CK_RV xGetRandomNumber( uint8_t * pRandomNumber,
                        size_t xNumBytes )
{
    CK_RV xResult = CKR_OK;
    CK_SESSION_HANDLE xSession;
    CK_FUNCTION_LIST_PTR pxFunctionList;

    if( ( pRandomNumber == NULL ) || ( xNumBytes == 0 ) )
    {
        xResult = CKR_ARGUMENTS_BAD;
    }
    if( xResult == CKR_OK )
    {
        xResult = C_GetFunctionList( &pxFunctionList );
    }

    if( xResult == CKR_OK )
    {
        xResult = prvGetRandomnessSession( &xSession );
    }

    if( xResult == CKR_OK )
    {
        xResult = pxFunctionList->C_GenerateRandom( xSession, pRandomNumber, xNumBytes );
    }
    return xResult;
}
```


#### Using C\_GetAttributeValue to acquire the value of an object's attribute:

```c
static int prvReadCertificateIntoContext( TLSContext_t * pxTlsContext,
                                          const char * pcLabelName,
                                          CK_OBJECT_CLASS xClass,
                                          mbedtls_x509_crt * pxCertificateContext )
{
    BaseType_t xResult = CKR_OK;
    CK_ATTRIBUTE xTemplate = { 0 };
    CK_OBJECT_HANDLE xCertObj = 0;

    /* Get the handle of the certificate. */
    xResult = xFindObjectWithLabelAndClass( pxTlsContext->xP11Session,
                                            pcLabelName,
                                            xClass,
                                            &xCertObj );

    if ( ( CKR_OK == xResult ) && ( xCertObj == CK_INVALID_HANDLE ) )
    {
        xResult = CKR_OBJECT_HANDLE_INVALID;
    }

    /* Query the certificate size. */
    if ( 0 == xResult )
    {
        xTemplate.type = CKA_VALUE;
        xTemplate.ulValueLen = 0;
        xTemplate.pValue = NULL;
        xResult = ( BaseType_t ) pxTlsContext->
                  pxP11FunctionList->C_GetAttributeValue( pxTlsContext->xP11Session,
                                                          xCertObj,
                                                          &xTemplate,
                                                          1 );
    }

     /* Create a buffer for the certificate. */
    if ( 0 == xResult )
    {
        xTemplate.pValue = pvPortMalloc( xTemplate.ulValueLen );

        if ( NULL == xTemplate.pValue )
        {
            xResult = ( BaseType_t ) CKR_HOST_MEMORY;
        }
    }

     /* Export the certificate. */
    if ( 0 == xResult )
    {
        xResult = ( BaseType_t ) pxTlsContext->
                    pxP11FunctionList->C_GetAttributeValue( pxTlsContext->xP11Session,
                                                            xCertObj,
                                                            &xTemplate,
                                                            1 );
    }

     /* Decode the certificate. */
    if ( 0 == xResult )
    {
        xResult = mbedtls_x509_crt_parse( pxCertificateContext,
                                          ( const unsigned char * ) xTemplate.pValue,
                                          xTemplate.ulValueLen );
    }

     /* Free memory. */
    if ( NULL != xTemplate.pValue )
    {
        vPortFree( xTemplate.pValue );
    }

    return xResult;
}
```


#### Using C\_Sign to add our private key's signature to our message:

This is a snippet from the TLS layer of our code that uses PKCS #11 for the C_Sign operation. In this
example, just before we send a TLS message, we call into the PKCS #11 layer and ask it to sign our message
with our private key.

```c
static int prvPrivateKeySigningCallback( void * pvContext,
                                         mbedtls_md_type_t xMdAlg,
                                         const unsigned char * pucHash,
                                         size_t xHashLen,
                                         unsigned char* pucSig,
                                         size_t * pxSigLen,
                                         int ( *piRng ) ( void *, unsigned char *, size_t ),
                                         void * pvRng )
{
    CK_RV xResult = CKR_OK;
    int lFinalResult = 0;
    TLSContext_t * pxTLSContext = ( TLSContext_t* ) pvContext;
    CK_MECHANISM xMech = { 0 };
    CK_BYTE xToBeSigned[ 256 ];
    CK_ULONG xToBeSignedLen = sizeof( xToBeSigned );

    /* Unreferenced parameters. */
    ( void )( piRng );
    ( void )( pvRng );
    ( void )( xMdAlg);

    /* Sanity check buffer length. */
    if ( xHashLen > sizeof( xToBeSigned ) )
    {
        xResult = CKR_ARGUMENTS_BAD;
    }

    /* Format the hash data to be signed. */
    if ( CKK_RSA == pxTLSContext->xKeyType )
    {
        xMech.mechanism = CKM_RSA_PKCS;

        /* mbedTLS expects hashed data without padding, but PKCS #11 C\_Sign
         * function performs a hash & sign if hash algorithm is specified. This
         * helper function applies padding indicating data was hashed with
         * SHA-256 while still allowing pre-hashed data to be provided. */
        xResult = vAppendSHA256AlgorithmIdentifierSequence( ( uint8_t * ) pucHash, xToBeSigned );
        xToBeSignedLen = pkcs11RSA_SIGNATURE_INPUT_LENGTH;
    }
    else if ( CKK_EC == pxTLSContext->xKeyType )
    {
        xMech.mechanism = CKM_ECDSA;
        memcpy( xToBeSigned, pucHash, xHashLen );
        xToBeSignedLen = xHashLen;
    }
    else
    {
         xResult = CKR_ARGUMENTS_BAD;
    }

    if ( CKR_OK == xResult )
    {
        /* Use the PKCS#11 module to sign. */
        xResult = pxTLSContext->
                  pxP11FunctionList->C_SignInit( pxTLSContext->xP11Session,
                                                 &xMech,
                                                 pxTLSContext->xP11PrivateKey );
    }

    if ( CKR_OK == xResult )
    {
        *pxSigLen = sizeof( xToBeSigned );
        xResult = pxTLSContext->
                  pxP11FunctionList->C_Sign( ( CK_SESSION_HANDLE ) pxTLSContext->xP11Session,
                                             xToBeSigned,
                                             xToBeSignedLen,
                                             pucSig,
                                             ( CK_ULONG_PTR ) pxSigLen );
    }

    if ( ( xResult == CKR_OK ) && ( CKK_EC == pxTLSContext->xKeyType ) )
    {
         /* PKCS #11 for P256 returns a 64-byte signature with 32 bytes for R and
          * 32 bytes for S. This must be converted to an ASN.1 encoded array. */
          if (*pxSigLen != pkcs11ECDSA_P256_SIGNATURE_LENGTH)
          {
              xResult = CKR_FUNCTION_FAILED;
          }

          if ( xResult == CKR_OK )
          {
            PKI_pkcs11SignatureTombedTLSSignature( pucSig, pxSigLen );
          }
    }

    if ( xResult != CKR_OK )
    {
        TLS_PRINT( ( "ERROR: Failure in signing callback: %d \r\n", xResult ) );
        lFinalResult = TLS_ERROR_SIGN;
    }

    return lFinalResult;
}
```
