import socket
import threading
import time
import json
import pickle
from consts import PORT, BUFF_SIZE,  PLAYER_COUNT, TIME


socket_list = []
thread_list = []
start = 0
end = 0


class Server:
    def __init__(self):
        self.connections = []
        self.players = []
        self.states = []
        self.scores = []
        self.whole_data = []

        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', PORT))
        self.s.setblocking(0)
        self.s.listen(3)

    def init_vars(self, n):
        for _ in range (0, n):
            states = {
                "PLAYER_DEAD" : False,
                "PLAYER_DISCONNECTED" : False,
                "START_GAME" : True
            }

            self.scores.append(0)
            self.states.append(states)         

    def client_thread(self, c, id):

        print("Connection from: " + str(self.players[id]["ip"]))
        nick = c.recv(BUFF_SIZE).decode()
        self.players[id]["nick"] = nick
        
        data_to_send = {
            "players" : self.players,
            "states" : self.states,
            "scores"  : self.scores,
            "connected" : True,
            "info" : "Initial data",
            "id": id
        } 

        data_to_send = (json.dumps(data_to_send)).encode("utf-8")
        c.send(data_to_send)

        while True:       

            to_send = json.dumps({
            "players" : self.players,
            "states" : self.states,
            "scores"  : self.scores,
            "connected" : True,
            "info" : "Initial data",
            "id": id
            } )

            c.send(to_send)

            
            time.sleep(1.0)

            client_data = c.recv(BUFF_SIZE).decode()
            print(client_data +"\n")
            
            if(len(client_data) > 0):
                client_data = json.loads(client_data)
                # UPDATE OF DATA TO SEND
                for player in self.players:
                    if player[client_data["id"]] == id:
                        self.scores[client_data["id"]] = client_data["score"]
                        self.states[client_data["id"]]["PLAYER_DEAD"] = client_data["is_dead"]
            

    def wait_for_players(self):
        try:    
            start = time.time()
            end = start 

            while (len(socket_list) < PLAYER_COUNT) and ((end - start) < TIME):

                end = time.time()
                try:                    
                    self.connections.append(self.s.accept())

                except socket.error:
                    continue
                
            self.init_vars(len(self.connections))

            for i in range(0, len(self.connections)):
                player_info = {
                    "id" : i,
                    "ip" : self.connections[i][1][0],
                    "port": self.connections[i][1][1]
                }
                self.players.append(player_info)

                t = threading.Thread(target=self.client_thread, args=(self.connections[i][0], i))
                t.start()
        
        except socket.error:
            print("Error occured")
            print(str(socket.error))
            self.s.close() 



if __name__ == "__main__":
    test_server = Server()
    test_server.wait_for_players()

