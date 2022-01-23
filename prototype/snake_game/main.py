import curses
from snake import Game

# ---- MAIN

def main(screen):
    try:
        # --- SCREEN INITIALIZATION
        screen_x = int(curses.COLS) # main screen width
        screen_y = int(curses.LINES) # main screen height
        
        if(screen_y < 30 or screen_x < 30):
            raise ValueError(screen_x , screen_y)
        

        test = Game(screen, screen_x , screen_y)
        test.print_screen()
        test.run()

    except ValueError:
        print("Your terminal is too small! Current size x: {} y:{}".format(screen_y, screen_x))
        
    print("Success!")

if __name__ == "__main__":
    curses.wrapper(main) # creates screen object
    