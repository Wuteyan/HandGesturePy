import socket               

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '10.0.1.21'# ip of raspberry pi 
port = 4001               
s.connect((host, port))
while 1:
    # print(s.recv(1024))
    s.sendall("676987\n")
s.close()