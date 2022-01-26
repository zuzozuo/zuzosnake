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
        self.death_counter = 0
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

        data_to_send = (json.dumps({"id": id, "connected": True, "wait": False})).encode("utf-8")
        c.send(data_to_send)

        while self.death_counter < (len(self.players)):       
            to_send = json.dumps({"data": self.players})
            c.send(to_send)

            time.sleep(1)

            client_data = c.recv(BUFF_SIZE).decode()

            if(len(client_data) > 0):
                client_data = json.loads(client_data)
                # UPDATE OF DATA TO SEND

                for player in self.players:
                    if player["id"] == client_data["id"]:
                        player["score"] = client_data["score"]
                        player["is_dead"] = client_data["is_dead"]
                    
                    if client_data["id"] == id and client_data["is_dead"] == True:
                        player["wait"] = True

                    
                    if (player["is_dead"]):
                        self.death_counter +=1
        


        rank = self.sort_scores()
        time.sleep(0.5)
        print(rank)
        # TO DO SEND INFO ABOUT DISCONNECTION
        


    def sort_scores(self):
        return sorted(self.players, key=lambda d: d['score']) 

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
                
            #self.init_vars(len(self.connections))

            for i in range(0, len(self.connections)):
                player_info = {
                    "id" : i,
                    "ip" : self.connections[i][1][0],
                    "port": self.connections[i][1][1],
                    "nick": "",
                    "is_dead": False,
                    "score" : 0,
                    "connected" : True,
                    "wait" : False
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

