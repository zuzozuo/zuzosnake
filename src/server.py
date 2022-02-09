#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-
import logging
from consts import PORT, BUFF_SIZE , PLAYER_COUNT, REQ_EOL
import socket
import json
import select
import json

class Server:

    def __init__(self):
        self.socket = None
        self.epoll = None 
        self.fileno = None
        self.clients = {
            'fileno': [None] * PLAYER_COUNT, 
            'connection': [None] * PLAYER_COUNT,
            'address': [None] * PLAYER_COUNT,
            'request': [None] * PLAYER_COUNT,
            'response': [None] * PLAYER_COUNT
        }
        self.to_send = []
        self.active = 0
# -----------------------------------------------------
    def connect(self):        
        conn, addr = self.socket.accept()
        logging.warning("Incoming connection from ip: {} on port: {}".format(addr[0], addr[1]))
        conn.setblocking(False)

        slot = self.find_slot(None) 

        if not slot in range(PLAYER_COUNT):
            logging.warning("NO EMPTY SLOT LEFT")
            conn.close()
            return False       
        
        clientno = conn.fileno()

        if self.find_slot(clientno) in range(PLAYER_COUNT):
            logging.error("DUPLICATE FOUND: CANNOT CONNECT 2 TIMES")
            conn.close()
            return False
        
        self.epoll.register(clientno, select.EPOLLIN)

        self.clients['fileno'][slot] = clientno
        self.clients['connection'][slot] = conn
        self.clients['address'][slot] = addr
        self.clients['request'][slot] = b''
        self.clients['response'][slot] = b''

        self.active = sum((x is not None for x in self.clients['fileno']))
        logging.warning("Client {} connected with fileno: {} slot num: {}".format(addr[1], clientno, slot))
        return True

# --------------------------------------------------------------------
    def find_slot(self, fileno):
        try:
            return self.clients['fileno'].index(fileno)
        except ValueError:
            return None

# ---------------------------------------------------------------------
    def data_filter(self):

        for line in self.clients["response"]:
            if line is not None and line !=b'':
                tmp = json.loads(line.decode()[:-1])
                tmp["players_num"] = self.active

                if not any(k["nick"] == tmp["nick"] for k in self.to_send):
                    self.to_send.append(tmp)
                else:
                    for k in range(0, len(self.to_send)):
                        self.to_send[k]["players_num"] =  self.active

                        if self.to_send[k]["nick"] == tmp["nick"]:
                            self.to_send[k]["score"] = tmp["score"]
                            self.to_send[k]["alive"] = tmp["alive"]     

# -----------------------------------------------------------------------
    def is_everyone_dead(self):
        if self.active > 0:
            death_counter = 0

            for k in self.to_send:
                if k["alive"] == False:
                    death_counter += 1
            
            if death_counter == self.active:
                logging.warning("Everyone is dead!, Server is going to shut down")
                return True

        return False
                            
# ---------------------------------------------------------------------
    def send(self,slot):
        self.data_filter()
        #print(self.to_send)
        buff = json.dumps(self.to_send).encode()

        written = self.clients['connection'][slot].send(buff) #size
        self.clients['response'][slot] = buff[written:]
        self.epoll.modify(self.clients['fileno'][slot], select.EPOLLIN)

# ---------------------------------------------------------------------
    def receive(self, slot):

        buff = self.clients['connection'][slot].recv(BUFF_SIZE)

        if len(buff) == 0:
            self.conn_close(slot)
            return

        self.clients['request'][slot] += buff

        if REQ_EOL in self.clients['request'][slot]:
            #print("Response from all clients: ")
            self.epoll.modify(self.clients['fileno'][slot], select.EPOLLOUT)

            self.clients['response'][slot] = self.clients['request'][slot]
            self.clients['request'][slot] = b''

# ----------------------------------------------------------------------
    def conn_close(self, slot):
        self.epoll.unregister(self.clients['fileno'][slot])
        self.clients['connection'][slot].close()

        self.clients['fileno'][slot] = None
        self.clients['connection'][slot] = None
        self.clients['address'][slot] = None

# ----------------------------------------------------------------------
    def run(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.bind(("", PORT))
        self.socket.listen(1)
        self.socket.setblocking(False)

        self.fileno = self.socket.fileno()

        self.epoll = select.epoll()
        self.epoll.register(self.fileno, select.EPOLLIN | select.EPOLLET)

        try:

            while True: 
                events = self.epoll.poll(1.0) #timeout

                for fileno, event in events: 
                    if (fileno == self.fileno):
                        self.connect()
                    else:
                        slot = self.find_slot(fileno)
                        if not slot in range(PLAYER_COUNT):
                            logging.error("Slot not found")
                        elif event & select.EPOLLIN:
                            self.receive(slot)
                        elif event & select.EPOLLOUT:
                            self.send(slot)
                        elif event & select.EPOLLHUP:
                            self.conn_close(slot)
                        else:
                            logging.warning("Unknown error")

                if self.is_everyone_dead():
                    break
        
        finally:
            self.epoll.unregister(self.fileno)
            self.epoll.close()
            self.socket.close()

if __name__ == '__main__':
    try:
        server = Server()
        server.run()
    except KeyboardInterrupt:
        print('\nRIP\n')