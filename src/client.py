import socket
import sys
import time
import curses
from snake import Game
from consts import BUFF_SIZE, PORT, STATE
import threading

# --- SCREEN INITIALIZATION
def screen_init():
    try:
        screen_x = int(curses.COLS) # main screen width
        screen_y = int(curses.LINES) # main screen height
        
        if(screen_y < 30 or screen_x < 30):
            raise ValueError(screen_x , screen_y)     
        else:
            return screen_x, screen_y  

    except ValueError:
        print("Your terminal is too small! Current size x: {} y:{}".format(screen_y, screen_x))
        exit(1)

# ---- MAIN

def main(screen):
    global server_ip   
    current_state = STATE["WAIT"]

    s = socket.socket()

    try:
        s.connect((server_ip, PORT))

        while True:

            if current_state == STATE["WAIT"]:
                resp = s.recv(BUFF_SIZE).decode()

                if(resp == STATE["START_GAME"]):
                    current_state = STATE["START_GAME"]
                else:
                    print("Waiting for game start...")
        
            if current_state == STATE["START_GAME"]:
                screen_x, screen_y = screen_init()
                test = Game(screen, screen_x , screen_y)
                test.print_screen()
                test.run()
                current_state = s.recv(BUFF_SIZE).decode()
                curses.endwin()
                print(current_state)
            
            if current_state == STATE["PLAYER_DEAD"]:
                print("Oh noes! :(I am dead :( ")
                s.close()

    
    except socket.error:
        print(socket.error)
        s.close()
        exit(1)

        
if __name__ == "__main__":

    global server_ip
    # --- GETTING ARGS
    try:
        if(len(sys.argv) < 2):
            raise IndexError

        server_ip = sys.argv[1]

    except IndexError:
        print("No ip addr given!")
        exit(1)

    curses.wrapper(main) # creates screen object