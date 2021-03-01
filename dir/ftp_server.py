"""
文件服务器 服务端代码
"""
import os
import sys
from socket import *
from threading import Thread
from time import sleep

FTP = "/home/tarena/alex/month02/ftp/"


# 　处理具体客户端请求
class Handle:
    def __init__(self, connfd):
        self.connfd = connfd

    def do_list(self):
        filelist = os.listdir(FTP)
        if filelist:
            self.connfd.send(b"OK")
            sleep(0.1)
            # 将文件列表拼接为一个大字符串发送
            files = '\n'.join(filelist)
            self.connfd.send(files.encode())
        else:
            self.connfd.send(b"FAIL")

    def do_put(self, filename):
        if os.path.exists(FTP + filename):
            self.connfd.send(b"EXISTS")
        else:
            self.connfd.send(b"OK")
            file = open(FTP + filename, "wb+")
            while True:
                data = self.connfd.recv(1024)
                if data == b"##":
                    break
                file.write(data)
            file.close()

    def do_get(self, filename):
        try:
            file = open(FTP + filename, 'rb')
        except FileNotFoundError:
            self.connfd.send(b"NULL")
        else:
            self.connfd.send(b"OK")
            sleep(0.1)
            while True:
                data = file.read(1024)
                if not data:
                    break
                self.connfd.send(data)
            file.close()
            sleep(0.1)
            self.connfd.send(b"##")  # 发送完毕

    # 不断接收请求，分情况讨论
    def request(self):
        while True:
            data = self.connfd.recv(1024).decode()
            # 简单按照协议解析
            tmp = data.split(" ")
            if not data or tmp[0] == "EXIT":
                break
            elif tmp[0] == "LIST":
                self.do_list()
            elif tmp[0] == "STOR":
                self.do_put(tmp[1])
            elif tmp[0] == "RETR":
                self.do_get(tmp[1])


# 线程类
class ThreadServer(Thread):
    def __init__(self, connfd):
        self.connfd = connfd
        self.handle = Handle(connfd)
        super().__init__(daemon=True)

    def run(self):
        self.handle.request()
        self.connfd.close()


# tcp模型
class TcpServer:
    """
    ｔｃｐ　套接字创建
    """

    def __init__(self, host="", port=0):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.sock = self._create_socket()

    def _create_socket(self):
        sock = socket()
        sock.bind(self.address)
        return sock

    # 启动函数
    def serve_forever(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        while True:
            connfd, addr = self.sock.accept()
            print("Connect from", addr)
            # 为客户端创建线程
            t = ThreadServer(connfd)
            t.start()


if __name__ == '__main__':
    server = TcpServer(host="0.0.0.0", port=8888)
    server.serve_forever()
