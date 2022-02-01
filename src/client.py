import curses
import logging
import time
from snake import Snake
from consts import W_WIDTH, W_HEIGHT, PORT, BUFF_SIZE , REQ_EOL
import socket
import json
import threading
import sys
import errno

# --- CLASSES 

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height       

    def print_screen(self):
        print(self.screen)


    def rungame(self):

        self.print_screen()

        directions = {
            "LEFT": [-1, 0],  # x y 
            "RIGHT": [1, 0],
            "UP" : [0, -1],
            "DOWN" : [0, 1]
        }

        curses.curs_set(0)

        self.screen.box()
        self.screen.addstr(0,int(self.width/2)-5, str(self.width) + "x" + str(self.height)) # prints main window size
        self.screen.addstr(1, int(self.width/2)-5, "CURSED SNAKEE")
        self.screen.refresh()

        snake_w = self.width - 5
        snake_h = self.height - 5

        snake = Snake(snake_w, snake_h, 2, 2)

        self.screen.nodelay(True)

        is_collision = False
        key = 0 
        event = 0

        snake.spawn_food()

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

            self.screen.addstr(1, self.width - 20, "Score: " + str(snake.get_score()))
            self.screen.refresh()
            time.sleep(0.1)
        
        curses.endwin()


class Client:
    def __init__(self, server_ip, nick):
        self.server_ip = server_ip
        self.nick = nick
        self.socket = None
        self.data = None
        self.received = None
        self.to_send = None

    def conn(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) 
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setblocking(False)

        try:
            self.socket.settimeout(10)
            self.socket.connect((self.server_ip, PORT))
            self.to_send = {
                    "alive": True,
                    "score": 0,
                    "nick" : self.nick
                }

            while True:

                self.socket.send(json.dumps(self.to_send)+ REQ_EOL)
                buff = self.socket.recv(BUFF_SIZE)

                if len(buff) <= 0:
                    logging.warning("Empty buff")
                    return
                
                #print(buff)

        except socket.error as e:
            if(e[0] == errno.EPIPE):
                logging.error("Server unexpectedly closed connection!")
            elif (e[0] == errno.EINPROGRESS):
                logging.error("Cannot connect!")

        
        finally:
            self.socket.close()
#-----------------------------------------------------------------

def main(screen):
    try:
        if(len(sys.argv) < 3):
            raise IndexError

        server_ip = sys.argv[1]
        nick = sys.argv[2]

        # --- SCREEN INITIALIZATION
        screen_x = int(curses.COLS) # main screen width
        screen_y = int(curses.LINES) # main screen height

        print(screen_x, screen_y)

        client = Client(server_ip, nick)
        game = Game(screen, screen_x, screen_y)
        t =  threading.Thread(target=client.conn, args=())
        t.start()
        game.rungame()

    except IndexError:
        print("No ip addr or nick  given!")
        exit(1)

    except ValueError:
        print("Your terminal is too small! Current size x: {} y:{}".format(screen_y, screen_x))
        exit(1)
    
    except KeyboardInterrupt:
        print("RIP\n")
    
    finally:
        t.join()


#------------------------------------------------------------------
        

if __name__ == '__main__':
    curses.wrapper(main)