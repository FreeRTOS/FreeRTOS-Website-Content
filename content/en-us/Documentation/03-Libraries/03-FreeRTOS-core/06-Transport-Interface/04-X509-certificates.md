---
title: X.509 Certificates
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

When communicating securely across the internet, the client (IoT device) and the server must provide
proof of their identity prior to establishing a mutually authenticated [TLS](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction)
connection. In a [public key infrastructure](https://en.wikipedia.org/wiki/Public_key_infrastructure), [digital (or identity) certificates](https://en.wikipedia.org/wiki/Public_key_certificate)
are exchanged to verify each entity's identity. The [X.509 certificate](https://en.wikipedia.org/wiki/X.509)
is the most common digital certificate format and is widely used across the internet and in IoT use cases.
The X.509 certificate is exchanged during
the [TLS handshake process](https://en.wikipedia.org/wiki/Transport_Layer_Security#Client-authenticated_TLS_handshake),
making it a critical piece of establishing a TLS connection. In IoT use cases, data transfer over communication
protocols such as [HTTPS](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP) or [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) should occur only after a TLS connection has
been established.

In PKI, a signature’s authenticity is established through a key pair: a public key and a private key.
Public keys are disseminated widely, while private keys are known only to the owner; this is done to maintain
security across the system. When data is signed or encrypted with a private key, any recipient of the data
can authenticate and/or decrypt the data using the matching public key. Data encrypted using a public key
can only be decrypted by the holder of the private key.

Once a key pair has been generated, a client will apply to a certificate authority for an X.509 certificate,
using a certificate signing request (CSR). The X.509 certificate is either signed by a
CA ([certificate authority](https://en.wikipedia.org/wiki/Certificate_authority)) or is self-signed. In most
use cases, the X.509 certificate is only self-signed when it is
the [certificate of the root CA](https://en.wikipedia.org/wiki/Root_certificate). In IoT use cases, it is
more common (and better practice!) for an intermediate CA (instead of the root CA) to sign each end-entity’s
certificate. This prevents the risk of exposing the root certificate. Using intermediate certificates creates
a [chain of trust](https://en.wikipedia.org/wiki/Chain_of_trust) that can be traced from the root CA to each
end-entity.

Additional details can be found here: [X.509 RFC5280](https://tools.ietf.org/html/rfc5280).
