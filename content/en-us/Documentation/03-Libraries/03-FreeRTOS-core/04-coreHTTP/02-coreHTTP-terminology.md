---
title: HTTP Client Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


+ *Server*

  The HTTP server is the central server to which HTTP clients can connect. The HTTP server receives HTTP 
  requests and sends only HTTP responses. An HTTP response is sent only when an HTTP request is received 
  and interpreted.


+ *Client*

  The HTTP client connects to an HTTP server. The HTTP client sends only HTTP requests to the server 
  and receives HTTP responses.


+ *Request*

  The type of HTTP message that the client sends to the server. It includes a Request-Line, a variable 
  number of header lines, and an optional request body.

  Example HTTP request:

  ```
  GET /site-image.jpg HTTP/1.1\r\n
  
  Host: FreeRTOS.org\r\n
  
  Connection: keep-alive\r\n`  
  
  \r\n
  
  Optional request body.`
  ```

+ *Response*

  The type of HTTP message that the server sends back to the client in reply to an HTTP request. It includes 
  a Status-Line, a variable number of header lines, and an optional response body.

  Example HTTP response:

  ```
  HTTP/1.1 403 Not found\r\n
  
  Accept-Ranges: bytes\r\n
  
  Content-Length: 1024\r\n
  
  Connection: close\r\n
  
  \r\n
  
  <html lang="en-US"> . . .
  ```

+ *Request-Line*

  The first line in a request message. It includes the request method token, the request path, and the 
  protocol version. This line ends with a carriage return and line feed. 

  Example:

  ```
  GET /path_to_item.txt?optional_query=search HTTP/1.1\r\n
  ```


+ *Status-Line*

  The first line in a response message. It includes the protocol version, the response status code, and 
  a response status phrase. This line ends with a carriage return and line feed.

  Example:

  ```
  HTTP/1.1 200 OK\r\n
  ```


+ *Method*

  The HTTP request method token is an indication of what should be done with the path in the HTTP request. 
  Currently the IoT HTTPS Client Library supports 
  methods: [GET, HEAD, PUT, POST](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html) (Sections 9.3 - 9.6).  
  These tokens are the first characters in the Request-Line. 


+ *Path*

  The path in the Request-Line is a Uniform Resource Locator Identifier (URLI) that identifies the resource 
  to apply the request to. It is contained in the Request-Line of the request.


+ *Status Code*

  The response status code is a three digit integer noting the result of the attempt to understand and 
  satisfy the request. The phrase following the status code gives human readable reasons for the status 
  code. For example a request to GET a page from an invalid address path results in the status code 404 
  and the phrase "not found" being returned. The response status is contained in the Status-Line. Status 
  codes are well defined in the HTTP/1.1 standard please 
  see [RFC2616 Section 10](https://tools.ietf.org/html/rfc2616#section-10).


+ *Header Line*

  In both the response and request messages there are header lines after the Status-Line or the Request-Line. 
  Each header line consists of a header field and header value separated by a colon and space. Each header 
  line ends with a carriage return and line feed. The last header line in an HTTP message is followed by 
  an extra carriage return and line feed.

  Example header lines:

  ```
  Host: FreeRTOS.org\r\n
  
  Content-Length: 512\r\n
  ```


+ *Header Field*

  The header field is the name of the header in a header line. The header field precedes a colon ":" in the header line.

  In the example header line below "Content-Length" is the header field.

  ```
  Content-Length: 256\r\n
  ```


+ *Header Value*

  The header value follows the colon and space in the header line.

  In the example header line below "256" is the header value.

  ```
  Content-Length: 256\r\n
  ```


+ *Persistent Connection*

  In a persistent HTTP connection, the server does not close the connection from the client after sending 
  its response to the client's request message. The connection persisted when the client sends the "Connection: 
  keep-alive" header line to the server in each request. Typically web servers will close a connection after 
  60 seconds if there are not requests received. The client will needs to send "Connection: keep-alive" 
  before the server closes the connection. Servers are not required to honor a "Connection: keep-alive" request.


+ *Non-Persistent Connection*

  In a non-persistent HTTP connection, the server closes the connection from the client after sending a 
  response to the client's request message. The client can request a non-persistent connection with a "Connection: 
  close" header in the request.
