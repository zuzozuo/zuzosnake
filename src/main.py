import curses
import random
import time
# ---- FUNCTIONS

# ---- CLASSES 

class Snake:
    def __init__(self, width, height, win_x, win_y):
        self.width = width
        self.height = height
        self.win_x = win_x
        self.win_y = win_y


        # SNAKE WINDOW INIT
        self.window = curses.newwin(height, width, win_y, win_x)
        self.window.clear()
        self.window.box()
        self.window.border(1)
        self.window.addstr(1, int(self.width/2), "CURSED SNAKEE")

        # SNAKE START RANDOM POSITIONS

        self.x = random.randint(2, int(width/2))
        self.y = random.randint(2, int(height/2))

        # SNAKE LIST
        self.tail = [[self.x, self.y]]

    
    def move(self, direction):
        self.tail[0][0] += direction[0] 
        self.tail[0][1] += direction[1]
    
    def check_collision(self):

        if(self.tail[0][0] <= 0 or self.tail[0][0] >= self.width-1):
            return True
        
        if(self.tail[0][1] <= 0 or self.tail[0][1] >= self.height-1):
            return True
            
        return False

    def update(self):
        self.window.addstr(self.tail[0][1], self.tail[0][0], "o")
        self.window.refresh()



class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height        

    def print_screen(self):
        print(self.screen)

    def run(self):

        directions = {
            "LEFT": [-1, 0],  # x y 
            "RIGHT": [1, 0],
            "UP" : [0, -1],
            "DOWN" : [0, 1]
        }

        curses.curs_set(0)

        self.screen.box()
        self.screen.addstr(0,int(self.width/2), str(self.width) + "x" + str(self.height)) # prints main window size
        self.screen.refresh()

        snake_w = self.width - 5
        snake_h = self.height - 5

        snake = Snake(snake_w, snake_h, 2, 2)

        self.screen.nodelay(True)

        is_collision = False
        key = 0

        while key != 27 and not is_collision:
            event = self.screen.getch()

            key = key if event ==-1 else event # remembering the last pressed key TO CHANGE

            if (key == curses.KEY_LEFT):
                snake.move(directions["LEFT"])
            
            if (key == curses.KEY_RIGHT):
                snake.move(directions["RIGHT"])
            
            if (key == curses.KEY_DOWN):
                snake.move(directions["DOWN"])
            
            if (key == curses.KEY_UP):
                snake.move(directions["UP"])

            is_collision = snake.check_collision()
            print(is_collision)
            snake.update()

            self.screen.refresh()
            time.sleep(0.1)


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
    