import socket
import os
import threading
import time
from consts import PORT, BUFF_SIZE, STATE
import signal

socket_list = []
thread_list = []
start = 0
end = 0

def player_thread(conn, addr):
    conn.send(STATE["START_GAME"].encode())

    while True:
        print(addr)
        data = conn.recv(BUFF_SIZE).decode()
        print(data)

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
        conn.send(STATE["WAIT"].encode())
        socket_list.append((conn, addr))
        x = threading.Thread(target=player_thread, args=(conn, addr))
        thread_list.append(x)

    for t in thread_list:
        t.start()
        
    s.close()           

# except KeyboardInterrupt:
#     for conn in socket_list:
#         conn[0].close()

#     for t in thread_list:
#         if t.is_alive():
#             t.join()

#     s.close()
#     print("Keyboard interrupt!")
#     exit(1)

except socket.error:
    print("Error occured")
    print(str(socket.error))
    s.close() 


