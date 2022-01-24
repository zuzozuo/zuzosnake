import socket
import sys
import json
import threading
import time
import curses
from snake import Snake
from infobox import InfoBox
from consts import PORT, BUFF_SIZE


class Client:
    def __init__(self, ip, p, nick, scr, scr_x, scr_y):
        self.server_ip = ip
        self.nick = nick
        # self.port = p
        self.s = socket.socket()       
        self.data =""

        self.screen = scr
        self.screen_w = scr_x 
        self.screen_h = scr_y

        # VALUES FOR SNAKE WINDOW 
        self.snake_w = int(scr_x - 3)/2
        self.snake_h = scr_y - 5
        self.snake_x = 2
        self.snake_y = 2

        # VALUES FOR INFOBOX WINDOW
        self.info_w = int(((scr_x - 3)/2 - 2))
        self.info_h = self.snake_h
        self.info_x = self.snake_w + 2
        self.info_y = self.snake_y

        try:
            self.s.connect((ip, p))
            self.s.send(nick.encode())

            t =  threading.Thread(target=self.connection_test, args=())
            t.start()
            

        except socket.error:
            print("socket error!")

    def connection_test(self):     
        #info = InfoBox(self.info_w, self.info_h, self.info_x, self.info_y)
        info = curses.newwin(self.info_h, self.info_w, self.info_y, self.info_x)
        info.clear()
        info.box()
        info.border(1)

        while True:
            data = self.s.recv(BUFF_SIZE)
            if(data):
                data = json.loads(data.decode())
                info.addstr(self.info_y + 2 , self.info_x + 3, "T E S T")
                #info.get_data("TEST LOL")
                
            #info.refresh()
            #info.update()
        self.s.close()

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

        self.screen.nodelay(True)

        is_collision = False
        key = 0 
        event = 0

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

            self.screen.addstr(1, self.screen_w - 20, "Score: " + str(snake.get_score()))
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

        test_client.game()

        
    except IndexError:
        print("No ip addr or nick  given!")

    except ValueError:
        print("Your terminal is too small! Current size x: {} y:{}".format(screen_y, screen_x))


if __name__ == "__main__":
    curses.wrapper(main)











