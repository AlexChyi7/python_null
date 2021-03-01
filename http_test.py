"""
http请求响应
"""
from socket import *

sock = socket()
sock.bind(("0.0.0.0", 8080))
sock.listen(5)

connfd, addr = sock.accept()
print("Connect from", addr)

request = connfd.recv(1024)
print(request.decode())

response = """HTTP/1.1 200 OK
Content-Type:test/html

Hello World
"""

connfd.send(response.encode())
connfd.close()
sock.close()
