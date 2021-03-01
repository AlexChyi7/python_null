"""
http请求响应
"""
from socket import *


def handle(connfd):
    request = connfd.recv(1024)
    print(request.decode())
    info = request.decode().split(" ")[1]
    if info == "/1":
        filename = "1.jpg"
    elif info == "/2":
        filename = "2.jpg"
    else:
        filename = "3.jpg"

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type:image/jpeg\r\n"
    response += "\r\n"

    with open(filename, "rb") as f:
        data = f.read()
    response = response.encode() + data
    connfd.send(response)


def main():
    sock = socket()
    sock.bind(("0.0.0.0", 8080))
    sock.listen(5)

    while True:
        connfd, addr = sock.accept()
        print("Connect from", addr)

        handle(connfd)
        connfd.close()

    sock.close()


if __name__ == '__main__':
    main()
