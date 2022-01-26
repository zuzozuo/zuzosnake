import socket
import sys
import json
import threading
import time
import curses
import pickle
import errno
from snake import Snake
from consts import PORT, BUFF_SIZE


class Client:
    def __init__(self, ip, p, nick, scr, scr_x, scr_y):
        self.server_ip = ip
        self.nick = nick
        self.port = p
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) 

        self.connected = False
        self.data_to_display = {}
        self.is_alive = True
        self.id = -1
        self.wait = False

        self.score = 0

        self.result = []

        self.screen = scr
        self.screen_w = scr_x 
        self.screen_h = scr_y

        # VALUES FOR SNAKE WINDOW 
        self.snake_w = int(scr_x - 3)/2
        self.snake_h = scr_y - 5
        self.snake_x = 2
        self.snake_y = 2

        # VALUES FOR INFOBOX WINDOW
        self.info_w = int((scr_x/2) - 7) 
        self.info_h = self.snake_h
        self.info_x = self.snake_w + 1
        self.info_y = self.snake_y

        

        try:
            self.s.connect((ip, p))
            self.s.send(nick.encode())

            while not self.connected:
                data =  self.s.recv(BUFF_SIZE)
                data = json.loads(data)
                self.connected = data["connected"]
                self.id = data["id"]

            if(self.connected):               
                t =  threading.Thread(target=self.connection, args=())
                t.start()
                self.game()

                if(self.is_alive == False):
                    t.join()
                    self.s.close()
            

        except socket.error:
            print("socket error!")

    def connection(self):     
        results = []
        while True:
            try:
                is_dead = not self.is_alive

                while not server_data:
                    deadline = time.time() + 5.0
                    if time.time() >= deadline:
                        raise socket.timeout
                    self.s.settimeout(deadline - time.time())
                    server_data = self.s.recv(BUFF_SIZE).decode()

                server_data = json.loads(server_data)
                self.data_to_display = server_data["data"]               
                server_data = ""
                results = server_data["result"]
                
                self.s.send(json.dumps({"id": self.id, "score": self.score, "is_dead": is_dead}))
                time.sleep(1)

                if(len(results) > 0):
                    self.result = results
                    break

            except socket.error as e:
                if e.errno == errno.EPIPE:
                    print ("Unexpected conn close")
                    break
                else:
                    print("Diffrent error")
        
        self.s.close()

        # wait for others

    def print_screen(self):
        print(self.screen)
    

    def game(self):

        self.print_screen()
        
        directions = {
            "LEFT": [-1, 0],  # x y 
            "RIGHT": [1, 0],
            "UP" : [0, -1],
            "DOWN" : [0, 1]
        }

        curses.curs_set(0)

        self.screen.box()
        self.screen.addstr(0,int(self.screen_w/2)-5, str(self.screen_w) + "x" + str(self.screen_h)) # prints main window size
        self.screen.addstr(1, int(self.screen_w/2)-5, "CURSED SNAKEE")
        self.screen.refresh()

        snake = Snake(self.snake_w, self.snake_h, self.snake_x, self.snake_y)
        infobox = curses.newwin(self.info_h, self.info_w, self.info_y, self.info_x)
        infobox.clear()
        infobox.box()
        infobox.border(1)
        infobox.refresh()

        self.screen.nodelay(True)

        is_collision = False
        key = 0 
        event = 0

        info_text = ""
        posy = 0

        snake.spawn_food()

    # --- MAIN LOOP
        while key != 27 and not is_collision:
            key = self.screen.getch()

            if (key != -1):
                event = key

            if (event == curses.KEY_LEFT):
                snake.move(directions["LEFT"])
            
            if (event == curses.KEY_RIGHT):
                snake.move(directions["RIGHT"])
            
            if (event == curses.KEY_DOWN):
                snake.move(directions["DOWN"])
            
            if (event == curses.KEY_UP):
                snake.move(directions["UP"])
            
            is_collision = snake.border_collision() or snake.tail_collision()

            snake.update()  
            self.score = snake.get_score()

            posy = 0
            curr_info = self.data_to_display
            for player in curr_info:
                info_text = "nick: " + player["nick"] + " score: " + str(player["score"]) + " is_dead: " + str(player["is_dead"])
                infobox.addstr(5 + posy  , 5, info_text)
                posy +=1

            infobox.refresh()
            self.screen.addstr(1, self.screen_w - 20, "Score: " + str(snake.get_score()))
            self.screen.refresh()
            time.sleep(0.1)
        

        self.is_alive = False
        self.wait = True

        while (self.wait):
            self.screen.clear()
            self.screen.addstr((int(self.screen_h/2)-5), int(self.screen_w/2)-5, "YOU ARE DEAD BUDDY! ")
            self.screen.refresh()
            time.sleep(0.1)
        

def main(screen):
    try:
        if(len(sys.argv) < 3):
            raise IndexError

        server_ip = sys.argv[1]
        player_nick = sys.argv[2]

        # --- SCREEN INITIALIZATION
        screen_x = int(curses.COLS) # main screen width
        screen_y = int(curses.LINES) # main screen height
        
        if(screen_y < 30 or screen_x < 30):
            raise ValueError(screen_x , screen_y)
        
        test_client = Client(server_ip, PORT, player_nick,
                            screen, screen_x, screen_y)

        
    except IndexError:
        print("No ip addr or nick  given!")
        exit(1)

    except ValueError:
        print("Your terminal is too small! Current size x: {} y:{}".format(screen_y, screen_x))
        exit(1)


if __name__ == "__main__":
    curses.wrapper(main)

