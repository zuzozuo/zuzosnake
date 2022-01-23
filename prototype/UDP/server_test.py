import socket
import time
import json

# ------- CONSTS 
# ------- CONSTS
PORT = 20001
BUFF_SIZE = 1024
STR_MESS = "SERVER TEST MESSAGE "

# -----
clients = set()

try:
    # --- OPENING SOCKET
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server_socket.bind(('', PORT))
except socket.error:
    print(socket.error)

start = time.time() # START OF TIME MEASURE


# --- PLAYERS GATHERING
while (True):
    (message,  sender) = server_socket.recvfrom(BUFF_SIZE)

    if(sender):
        try:
            end = time.time()
            
            if(len(clients)  < 3) and ((end - start) < 31):
                clients.add(sender)
                
                bytes_to_send = str.encode(STR_MESS)
                server_socket.sendto(bytes_to_send, sender)
                print(end-start)
            else:
                #for client in clients:
                    #bytes_to_send = json.dump({'game_state': True, 'mess': 'connected to server'})
                    #pass
                break

        except Exception as e:
            print(e)

# ---- WAITING FOR CLIENTS

while (True):
    (message,  sender) = server_socket.recvfrom(BUFF_SIZE)

    if (sender in clients):
        server_socket.sendto(str.encode("You are the chosen one! "), sender)
        pass
    else:
        server_socket.sendto(str.encode("You shall not pass!"), sender)





print(clients)


