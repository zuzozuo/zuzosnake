import socket
import time
import sys
import json
# ------- CONSTS
PORT = 20001
BUFF_SIZE = 1024
STR_MESS = "Greetings and welcome!  "
# --------- GLOBAL VARS
in_game = False
# -------
try:
    if(len(sys.argv) < 2):
        raise IndexError

    server_ip = sys.argv[1]


except IndexError:
    print("No ip addr given!")

# -----------
bytes_to_send = str.encode(STR_MESS)

# ---- CONNECTION
try:
    # --- CREATING SOCKET
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    client_socket.bind(('', PORT))
    client_socket.settimeout(10)

except socket.error:
    print(socket.error)
    exit(1)

# --- TRYING TO CONNECT WITH SERVER
while(True):
    try:
        client_socket.sendto(bytes_to_send, (server_ip, PORT))
        time.sleep(2)            

        received_data = client_socket.recvfrom(BUFF_SIZE)[0]  #only message
        print(received_data)

    except socket.timeout:
        print("Timeout occured....")
        client_socket.close()
        break
    
    except socket.error:
        print ("Socket error occured...")
        client_socket.close()
        break


# ----- IN GAME LOOP

while(in_game):
    print("Congratz! You are in game! Waiting for signal from server...")
    received_data = client_socket.recvfrom(BUFF_SIZE)[0]

    if(received_data):
        print(received_data)




