from threading import Thread
from time import sleep
import socket
import sys

class ClientSocket():

    def recvThreadFunc(self):
        #print ('recvThreadFunc start')
        while True:
            if self.isConnected:
                try:
                    data = self.sock.recv(1024)
                    data = data.decode("utf-8")
                    self.recvBuf += data
                    self.recvLen += len(data)
                except:
                    print ('close recvThreadFunc')
                    break

    def recvThreadCallback(self, nextStep):
        if self.isConnected:
            while True:
                try:
                    data = self.sock.recv(1024)
                    data = data.decode("utf-8")
                    if len(data) != 0:
                        self.recvBuf += data
                        self.recvLen += len(data)
                        print ('block data = %s' % data)
                        print ('block data len = %d' % len(data))
                        nextStep(data)
                        break
                    else:
                        #print ('recv none')
                        pass
                except:
                    pass
            print ('recvThreadCallback while end')
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.stderr = 0
        self.recvLen = 0
        self.recvBuf = ''
        self.isConnected = False
        self.socket = None
        self.recvThread = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddress = (self.ip, self.port)
        self.sock.connect(serverAddress)
        self.isConnected = True
        self.recvThread = Thread(target = self.recvThreadFunc)
        self.recvThread.start()

    """def recv(self, callback):
        self.recvThread = Thread(target = self.recvThreadCallback, args = (callback,))
        self.recvThread.start()"""

    def recv(self, bufLen):
        if (bufLen < self.recvLen):
            result = self.recvBuf[0 : bufLen]
            self.recvBuf = self.recvBuf[bufLen : self.recvLen]
            self.recvLen -= bufLen
        else:
            result = self.recvBuf
            self.recvLen = 0
            self.recvBuf = ''
        return result

    def recvAll(self):
        result = self.recvBuf
        self.recvLen = 0
        self.recvBuf = ''
        return result
    
    def recvCmd(self):
        return self.recv(1)
    
    def checkRecv(self):
        if self.recvLen == 0:
            return False
        else:
            return True

    #should not use
    def recvBlock(self):
        while True:
            data = self.sock.recv(1024)
            #self.recvBuf += data
            #self.recvLen += len(data)
            if len(data) != 0:
                print ('block data = %s' % data)
                print ('block data len = %d' % len(data))
                break
            
    def send(self, data):
        self.sock.sendall(bytes(data, "utf8"))

    def close(self):
        self.isConnected = False
        self.sock.close()
        
if __name__ == '__main__':
    print ('OK')
