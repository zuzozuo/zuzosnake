import curses
import logging
import time
from snake import Snake
from consts import PORT, BUFF_SIZE , REQ_EOL
import socket
import json
import threading
import sys
import errno

# --- GLOBAL VARIABLES  :(
player_data = {
                "alive": False,
                "score": 0,
                "nick" : ""
            }

all_player_data = ""
exit_game = False
is_connected = False
# --- CLASSES 

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height       

        # VALUES FOR SNAKE WINDOW 
        self.snake_w = int(width - 3)/2
        self.snake_h = height - 5
        self.snake_x = 2
        self.snake_y = 2

        # VALUES FOR INFOBOX WINDOW
        self.info_w = int((width/2) - 7) 
        self.info_h = self.snake_h
        self.info_x = self.snake_w + 1
        self.info_y = self.snake_y

    def print_screen(self):
        print(self.screen)

    def run_single(self):

        self.print_screen()

        directions = {
            "LEFT": [-1, 0],  # x y 
            "RIGHT": [1, 0],
            "UP" : [0, -1],
            "DOWN" : [0, 1]
        }

        curses.curs_set(0)

        self.screen.box()
        self.screen.addstr(0, self.width - 5, str(self.width) + "x" + str(self.height)) # prints main window size
        self.screen.addstr(1, self.width - 5, "CURSED SNAKEE")
        self.screen.refresh()

        snake = Snake(self.snake_w * 2, self.snake_h, self.snake_x, self.snake_y)

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

        return 0 


    def run_multi(self):
        global player_data, all_player_data, exit_game, is_connected

        player_data["alive"] = True
        player_data["score"] = 0

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

            player_data["score"] = snake.get_score()

            posy = 0
            to_print = all_player_data

            for line in to_print:
                info_text = "nick: " + line["nick"] + " score: " + str(line["score"]) + " alive: " + str(line["alive"])
                infobox.addstr(3 + posy ,3 ,info_text)
                posy +=1

            infobox.refresh()          
            self.screen.addstr(1, self.width - 20, "Score: " + str(snake.get_score()))
            self.screen.refresh()
            time.sleep(0.1)

        
        player_data["alive"] = False

        # --- AFTER DEATH - there is no life : ( 

        # infobox.endwin()
        self.screen.clear()

        self.screen.box()
        self.screen.addstr(0,int(self.width/2)-5, str(self.width) + "x" + str(self.height)) # prints main window size
        self.screen.addstr(1, int(self.width/2)-5, "CURSED SNAKEE")
        self.screen.addstr(4, int(self.width/2)-5, "WAITING FOR OTHER PLAYERS TO FINISH THE GAME....") # TODO MAKE IT PRETTIER
        self.screen.refresh()

        #  NOTE - TO FINISH!    

        while True:
            alive_states = [] 
            players_num = all_player_data[0]["players_num"]
            to_print = all_player_data
            posy = 0
            for line in to_print:
                info_text = "nick: " + line["nick"] + " score: " + str(line["score"]) + " alive: " + str(line["alive"])
                self.screen.addstr(6 + posy , int(self.width/2)- 20 , info_text)
                posy +=1
                alive_states.append(line["alive"])

            exit_game = True if(players_num == alive_states.count(False)) else False
            
            if (exit_game):
                break

            self.screen.refresh()
            time.sleep(0.1)
        

        curses.endwin()

        return 0 


class Client:
    def __init__(self, server_ip, nick):
        self.server_ip = server_ip
        self.nick = nick
        self.socket = None
        self.data = None
        self.received = None

    def conn(self):
        global player_data, all_player_data, is_connected, exit_game

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) 
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setblocking(False)

        player_data["alive"] = True
        player_data["score"] = 0
        player_data["nick"] = self.nick

        try:
            self.socket.settimeout(10)
            self.socket.connect((self.server_ip, PORT))
            is_connected  = True

            while True:

                self.socket.send(json.dumps(player_data)+ REQ_EOL)

                buff = self.socket.recv(BUFF_SIZE)

                if len(buff) <= 0:
                    logging.warning("Empty buff")
                    return
                
                all_player_data = json.loads(buff.decode())

                if(exit_game):
                    break

        except socket.error as e:
            is_connected = False

            if(e[0] == errno.EPIPE):
                logging.error("Server unexpectedly closed connection!")
            elif (e[0] == errno.EINPROGRESS):
                logging.error("Cannot connect!")

        finally:
            is_connected = False
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

        client = Client(server_ip, nick)
        game = Game(screen, screen_x, screen_y)
        t =  threading.Thread(target=client.conn, args=())
        t.start()

        start = time.time()

        while True:
            if is_connected:
                game.run_multi()
                break
            elif (time.time() - start) > 3 and not is_connected:
                screen.addstr(10, int(screen_x/2)-20, "Could not connect to the server...")
                screen.refresh()
                #TODO IF COULD NOT CONNECT WE CAN ASK PLAYER IF HE WANTS TO PLAY SINGLE MODE
                screen.addstr(15, int(screen_x/2)-20, "Do you wish to play single-mode version?  (y/n")
                screen.refresh()
                key = screen.getch()

                if(key == ord('n')):
                    break
                
                if(key == ord('y')):
                    game.run_single()
                    break
                time.sleep(0.1)

    except IndexError:
        print("No ip addr or nick  given!")
        exit(1)

    except ValueError:
        print("Your terminal is too small! Current size x: {} y:{}".format(screen_y, screen_x))
        exit(1)
    
    except KeyboardInterrupt:
        print("RIP\n")
    
    #finally:
        #t.join()
        #client.socket.close()

#------------------------------------------------------------------
if __name__ == '__main__':
    curses.wrapper(main)

#TODO AFTER MULTI SHOW SCORES AND WAIT FOR EXIT KEY
    if(len(all_player_data) > 0):
        sorted_data = sorted(all_player_data, key=lambda d: d['score']) 

        print("HIGH SCORES TIME: ")
        print("THE WINNER IS...." + str(sorted_data[0]['nick'])) # TODO SOME FANCY LETTERS!
        
        for line in sorted_data:
            print(str(line))