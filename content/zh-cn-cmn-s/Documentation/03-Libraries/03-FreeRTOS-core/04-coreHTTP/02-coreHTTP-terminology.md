---
title: HTTP 客户端术语
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


+ *服务器*

  HTTP 服务器是 HTTP 客户端可连接的中央服务器。HTTP 服务器接收 HTTP 
  请求，且只发送 HTTP 响应。只有在收到并解释 HTTP 请求时，才发送 HTTP 响应 
  。


+ *客户端*

  连接到 HTTP 服务器的 HTTP 客户端。HTTP 客户端仅向服务器发送 HTTP 请求 
  并接收 HTTP 响应。


+ *请求*

  客户端发送到服务器的 HTTP 消息的类型。它包括请求行、 
  数量不定的报头行和可选请求正文。

  HTTP 请求示例：

  ```
  GET /site-image.jpg HTTP/1.1\r\n
  
  Host: FreeRTOS.org\r\n
  
  Connection: keep-alive\r\n`  
  
  \r\n
  
  Optional request body.`
  ```

+ *响应*

  服务器发送回客户端以回复 HTTP 请求的 HTTP 消息的类型。它包括 
  状态行、数量不定的报头行和可选响应正文。

  HTTP 响应示例：

  ```
  HTTP/1.1 403 Not found\r\n
  
  Accept-Ranges: bytes\r\n
  
  Content-Length: 1024\r\n
  
  Connection: close\r\n
  
  \r\n
  
  <html lang="en-US"> . . .
  ```

+ *请求行*

  请求消息中的第一行。它包括请求方法令牌、请求路径 
  和协议版本。状态行以回车和换行结束。 

  示例：

  ```
  GET /path_to_item.txt?optional_query=search HTTP/1.1\r\n
  ```


+ *状态行*

  响应消息中的第一行。它包括协议版本、响应状态代码和 
  响应状态短语 (phrase)。状态行以回车和换行结束。

  示例：

  ```
  HTTP/1.1 200 OK\r\n
  ```


+ *方法*

  HTTP 请求方法令牌指示应如何处理 HTTP 请求中的路径。 
  目前，IoT HTTPS 客户端库支持的方法： 
  [GET、HEAD、PUT、POST](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html) （9.3 - 9.6节）。  
  这些令牌是各请求行中的第一个字符。 


+ *路径*

  请求行中的路径是一个统一资源定位符标识符（URLI）， 
  用于识别应用该请求的资源。它包含在请求的请求行中。


+ *状态代码*

  响应状态代码是一个三位整数， 
  表示尝试理解和满足请求的结果。状态代码后面的短语使人们可以读懂状态代码 
  。例如，从无效地址路径请求 GET 页面时，会返回状态代码 404 
  和 “not found” 短语。响应状态包含在状态行中。状态 
  代码在 HTTP/1.1 标准中有明确定义， 
  请参阅 [RFC2616 第 10 节](https://tools.ietf.org/html/rfc2616#section-10)。


+ *标头行*

  在响应消息和请求消息中，状态行或请求行后面都有标头行。 
  每个标头行由一个标头字段和标头值组成，用冒号和空格分隔。每个标头行 
  以回车和换行结束。HTTP 消息的最后一个标头行 
  后有一个额外的回车和换行符。

  标头行示例：

  ```
  Host: FreeRTOS.org\r\n
  
  Content-Length: 512\r\n
  ```


+ *标头字段*

  标头字段是标头行中的标头的名称。标头字段位于标头行中的冒号“:”之前。

  在下面的标头行示例中，“Content-Length” 表示标头字段。

  ```
  Content-Length: 256\r\n
  ```


+ *标头值*

  标头值位于标头行的冒号和空格后。

  在下面的标头行示例中，“256” 表示标头值。

  ```
  Content-Length: 256\r\n
  ```


+ *永久连接*

  在永久性 HTTP 连接中，服务器在向客户端的请求消息发送响应后 
  不会关闭来自客户端的连接。当客户端在每次请求中向服务器发送 “Connection: 
  keep-alive” 标头行时，连接就会持续。如果没有收到请求， 
  网络服务器通常会在 60 秒后关闭连接。客户端需要在服务器关闭连接前发送 “Connection: keep-alive” 
  。服务器不需要执行 "Connection: keep-alive" 请求。


+ *非永久性连接*

  在非永久性 HTTP 连接中，服务器在对客户端的请求消息发送响应后 
  关闭来自客户端的连接。客户端可以用请求中的 "Connection: 
  close" 标头来请求一个非永久性连接。

