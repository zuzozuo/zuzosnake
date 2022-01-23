import socket
import sys
import time

PORT=20001
BUFF_SIZE = 1024


try:
    if(len(sys.argv) < 2):
        raise IndexError

    server_ip = sys.argv[1]


except IndexError:
    print("No ip addr given!")


s = socket.socket()

try:
    s.connect((server_ip, PORT))

    while True:
        data = "ping".encode()
        s.send(data)
        time.sleep(1)
        resp = s.recv(BUFF_SIZE)
        time.sleep(1)
        print(resp.decode())
    
except socket.error:
    print(socket.error)