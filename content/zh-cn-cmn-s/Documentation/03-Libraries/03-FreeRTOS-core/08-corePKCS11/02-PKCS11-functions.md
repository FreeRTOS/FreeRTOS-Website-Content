---
title: PKCS
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[PKCS #11](index.md) 包含许多函数，并支持各种用例。FreeRTOS PKCS #11 
库仅实现适用于第一个描述的用例的一小部分函数。 每个函数 
在 [PKCS #11 标准](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html)中都有完整的记录。  
这些术语对初读者来说可能比较困难，因此我们也在下面提供了示例代码。

PKCS #11 操作函数：
* C_Random。 TCP/IP 堆栈（例如，选择初始序列号时）、 
  加密算法中以及  
  [TLS 握手](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_handshake) 期间均需要随机数。

* C_Sign。 对发送到另一个网络节点的消息进行签名，使该节点能够识别消息的真正来源 
  。

* C_FindObject。  查找由 PKCS #11 管理的对象，例如[客户端证书](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/04-X509-certificates)。

* C_GetAttributeValue。  该 API 获取一个对象的属性值，例如，该对象是 
  密钥类型还是证书类型。


PKCS #11 管理函数：
* C_Initialize。 初始化加密库。
* C_Finalize。  清理加密库使用的资源。
* C_OpenSession。在一个软件应用程序和一个特定的加密令牌之间打开一个会话（或连接）。
* C_CloseSession。 关闭由 C_OpenSession 打开的会话。
* C_Login。 登录到令牌。
* C_GetFunctionList。 获取用于调用 PKCS #11 API 的包含函数指针的结构体。
* C_GetSlotList。 获取可用于访问插槽中的任何令牌的插槽列表。


### 代码示例

以下是一些示例代码段，展示了如何使用 PKCS #11 API。


#### Using C_GenerateRandom:

此代码段显示了如何使用 PKCS #11 获取随机数。例如，此函数可 
用于 FreeRTOS-Plus-TCP，以生成随机 TCP 数。

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


#### 使用 C_GetAttributeValue 获取对象的属性值：

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


#### 使用 C_Sign 将私钥的签名添加至我们的消息中：

这是我们 TLS 层代码的一个片段，它使用 PKCS #11 进行 C_Sign 操作。在该 
示例中，我们在发送 TLS 消息前调用 PKCS #11 层，并要求它使用我们的私钥对我们的消息进行签名 
。 

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

        /* mbedTLS expects hashed data without padding, but PKCS #11 C_Sign
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
        TLS_PRINT( ( "ERROR: Failure in signing callback: %d &bsol;r&bsol;n", xResult ) );
        lFinalResult = TLS_ERROR_SIGN;
    }

    return lFinalResult;
}

```

