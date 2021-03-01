from socket import *
from select import select


class WebServer:
    def __init__(self, host="", port=8080, html=""):
        self.host = host
        self.port = port
        self.html = html
        self.sock = self._create_socket()
        self._rlist = []
        self._wlist = []
        self._xlist = []

    # 创建好套接字
    def _create_socket(self):
        sock = socket()
        sock.bind((self.host, self.port))
        sock.setblocking(False)
        return sock

    # 处理浏览器连接行为
    def _connect(self):
        connfd, addr = self.sock.accept()
        connfd.setblocking(False)
        self._rlist.append(connfd)

    # 启动整个服务
    def start(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        self._rlist.append(self.sock)
        # 循环监控浏览器请求(连接,http请求)
        while True:
            rs, ws, xs = select(self._rlist, self._wlist, self._xlist)
            for r in rs:
                if r is self.sock:
                    self._connect()  # 处理浏览器连接
                else:
                    try:
                        self._handle(r)  # 处理浏览器发送http请求
                    except Exception as e:
                        print(e)
                    finally:
                        self._rlist.remove(r)
                        r.close()

    def _handle(self, connfd):
        # 接收浏览器http请求
        request = connfd.recv(1024)
        if not request:
            raise Exception
        info = request.decode().split(' ')[1]
        print("请求内容:", info)
        self._send_response(info, connfd)

    def _send_response(self, info, connfd):
        if info == "/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + info

        try:
            fr = open(filename, "rb")
        except Exception:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:html\r\n"
            response += "\r\n"
            with open(self.html + "/404.html", "rb") as f:
                data = f.read()
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:html\r\n"
            response += "\r\n"
            data = fr.read()
            fr.close()
        finally:
            response = response.encode() + data
            connfd.send(response)


if __name__ == '__main__':
    httpd = WebServer(host="0.0.0.0", port=8090, html="./static")
    httpd.start()
