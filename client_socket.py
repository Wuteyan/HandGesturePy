from threading import Thread
from time import sleep
import socket
import sys

class client_socket():

    def threaded_function(self):
        print ('recv_thread start')
        while True:
            if self.isConnected:
                try:
                    data = self.sock.recv(1024)
                    self.recv_buf.extend(data)
                    self.recv_len += len(data)
                except:
                    #print ('except')
                    break

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.stderr = 0
        self.recv_len = 0
        self.recv_buf = []
        self.isConnected = False
        self.socket = None
        self.recv_thread = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.ip, self.port)
        self.sock.connect(server_address)
        self.isConnected = True
        self.recv_thread = Thread(target = self.threaded_function)
        self.recv_thread.start()

    def recv(self, buf_len):
        print ('recv_len = %d' % self.recv_len)
        print ('recv_buf = "%s"' % self.recv_buf)
        if (buf_len < self.recv_len):
            result = self.recv_buf[0 : buf_len]
            self.recv_buf = self.recv_buf[buf_len : recv_len]
            recv_len -= buf_len
            return result
        else:
            result = self.recv_buf
            self.recv_len = 0
            self.recv_buf = []
            return result
        
    def check_recv(self):
        if self.recv_len == 0:
            return False
        else:
            return True
    
    def send(self, data):
        self.sock.sendall(bytes(data, "utf8"))

    def close(self):
        self.isConnected = False
        self.sock.close()
        
