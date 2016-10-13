from threading import Thread
from time import sleep
import socket
import sys

class ClientSocket():

    """def threaded_function(self):
        #print ('recv_thread start')
        while True:
            if self.isConnected:
                try:
                    data = self.sock.recv(1024)
                    self.recv_buf.extend(data)
                    self.recv_len += len(data)
                except:
                    #print ('except')
                    break"""

    def recv_thread_function(self, next_step):
        if self.isConnected:
            while True:
                try:
                    data = self.sock.recv(1024)
                    data = data.decode("utf-8")
                    if len(data) != 0:
                        self.recv_buf += data
                        self.recv_len += len(data)
                        print ('block data = %s' % data)
                        print ('block data len = %d' % len(data))
                        next_step(data)
                        break
                    else:
                        #print ('recv none')
                        pass
                except:
                    pass
            print ('recv_thread_function while end')
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.stderr = 0
        self.recv_len = 0
        self.recv_buf = ''
        self.isConnected = False
        self.socket = None
        self.recv_thread = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.ip, self.port)
        self.sock.connect(server_address)
        self.isConnected = True
        #self.recv_thread = Thread(target = self.threaded_function)
        #self.recv_thread.start()

    def recv(self, callback):
        self.recv_thread = Thread(target = self.recv_thread_function, args = (callback,))
        self.recv_thread.start()
        
    """def check_recv(self):
        if self.recv_len == 0:
            return False
        else:
            return True"""

    #should not use
    def recv_block(self):
        while True:
            data = self.sock.recv(1024)
            #self.recv_buf += data
            #self.recv_len += len(data)
            if len(data) != 0:
                print ('block data = %s' % data)
                print ('block data len = %d' % len(data))
                break
            
    def send(self, data):
        self.sock.sendall(bytes(data, "utf8"))

    def close(self):
        self.isConnected = False
        self.sock.close()
        
