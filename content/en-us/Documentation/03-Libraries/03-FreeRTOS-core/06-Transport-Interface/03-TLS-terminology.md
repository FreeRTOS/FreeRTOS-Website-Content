---
title: TLS Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

- *Basic TLS Handshake*

  The [basic TLS Handshake](https://en.wikipedia.org/wiki/Transport_Layer_Security#Basic_TLS_handshake) is 
  a negotiation between the client and server to verify the server's authentication and negotiate the details 
  on how to communicate. During this handshake process, the client and the server decide on the TLS version (the 
  highest mutually supported) and cipher suite. Only the server is authenticated in the basic TLS handshake.


- *TLS Handshake*

  The [full TLS Handshake](https://en.wikipedia.org/wiki/Transport_Layer_Security#Client-authenticated_TLS_handshake) 
  requires mutual authentication between the client and the server. During this process, the client must 
  also prove the authenticity of its identity to the server before a connection can be established.


- *Cipher Suite*

  A [cipher suite](https://en.wikipedia.org/wiki/Cipher_suite) is the set of algorithms used for encrypting 
  and authenticating data during secure communications between the client and server. The client and server 
  must agree on the cipher suite before proceeding to communicate past the handshake.


- *PKI (Public Key Infrastructure)*

  PKI ([Public Key Infrastructure](https://en.wikipedia.org/wiki/Public_key_infrastructure)) defines a 
  set of roles and procedures for the management of digital certificates. This system is responsible for 
  ensuring the authenticity of each certificate issued by the server and client. Within PKI, the 
  CA (Certificate Authority) is responsible for issuing digital certificates. These certificates are used 
  to verify the authenticity of the owner (server/client).


- *Public and Private Key*

  [Public key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) is a system in which 
  a mathematically-related pair of keys are used for encrypting and signing data. Each pair of keys in 
  public key cryptography includes a widely disseminated public key and a private key known only to one 
  party. By signing or encrypting data with a private key, any recipient can authenticate and/or decrypt 
  the data using the matching public key. Data encrypted using a public key can only be decrypted by the 
  holder of the private key. TLS uses public key cryptography during the TLS handshake.


- *Root CA Certificate*

  The [root CA certificate](https://en.wikipedia.org/wiki/Root_certificate) establishes the authenticity of 
  the Certificate Authority. This root certificate is the top-most certificate and is used to the sign the 
  certificates issued by the certificate authority. As an example, in the MQTT with TLS demo, the root CA 
  certificate could be configured to use a public MQTT broker (e.g. [test.mosquitto.org](http://test.mosquitto.org/)), 
  or when using AWS IoT Core, the root CA certificate would be one of 
  the [recommended IoT Core CA certificates](https://docs.aws.amazon.com/iot/latest/developerguide/server-authentication.html).


- *mbed TLS*

  [mbed TLS](https://en.wikipedia.org/wiki/Mbed_TLS) is an implementation of TLS that is specifically designed 
  for memory constrained embedded IoT devices. It utilizes a minimal subset of the TLS stack.
