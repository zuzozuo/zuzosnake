import socket
import os
import threading
import time

PORT=20001
BUFF_SIZE = 1024

socket_list = []
thread_list = []
start = 0
end = 0

def player_thread(conn, addr):
    while True:
        print(addr)
        data = conn.recv(BUFF_SIZE).decode()
        data = data + " pong"
        conn.send(data.encode())
        time.sleep(2)
    conn.close()


s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', PORT))
s.setblocking(0)
s.listen(4)

try:    
    start = time.time()

    while (len(socket_list) < 3) and ((end - start) < 10):
        print((end-start))
        end = time.time()
        try:
            conn, addr = s.accept()
        except socket.error:
            continue
        #conn.setblocking(0)
        socket_list.append((conn, addr))
        x = threading.Thread(target=player_thread, args=(conn, addr))
        thread_list.append(x)
        #x.start()

    for t in thread_list:
        t.start()
        
    s.close()           

except socket.error:
    print("Error occured")
    print(str(socket.error))
    s.close() 


