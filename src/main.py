import curses
import random
import time

WINDOW_OFFSET = 2
# ---- FUNCTIONS

# ---- CLASSES 

class Snake:
    def __init__(self, width, height, win_x, win_y):
        self.width = width
        self.height = height
        self.win_x = win_x
        self.win_y = win_y
        self.current_dir = [0, 0]


        # SNAKE WINDOW INIT
        self.window = curses.newwin(height, width, win_y, win_x)
        self.window.clear()
        self.window.box()
        self.window.border(1)

        # SNAKE START RANDOM POSITIONS

        self.x = random.randint(2, int(width/2))
        self.y = random.randint(2, int(height/2))

        # SNAKE LIST
        self.tail = [[self.x, self.y]]

    
    def move(self, direction):
        # NEW HEAD COORDS
        self.tail[0][0] += direction[0] 
        self.tail[0][1] += direction[1]

        self.current_dir = direction
    
    def border_collision(self):

        if(self.tail[0][0] <= 0 or self.tail[0][0] >= self.width-1):
            return True
        
        if(self.tail[0][1] <= 0 or self.tail[0][1] >= self.height-1):
            return True
        return False

    def food_collision(self, food):
        food = [food[0] - WINDOW_OFFSET, food[1] - WINDOW_OFFSET]
        if(self.tail[0]  == food):
            return True
        else:
            return False

    def update(self):

        self.window.addstr(self.tail[0][1] - self.current_dir[1], self.tail[0][0] - self.current_dir[0], " ")
        self.window.addstr(self.tail[0][1], self.tail[0][0], "o")
        self.window.refresh()



class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height        
        self.score = 0

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
        self.screen.addstr(1, int(self.width/2), "CURSED SNAKEE")
        self.screen.refresh()

        snake_w = self.width - 5
        snake_h = self.height - 5

        snake = Snake(snake_w, snake_h, WINDOW_OFFSET, WINDOW_OFFSET)

        self.screen.nodelay(True)

        is_collision = False
        key = 0
        event = 0

        food = [5, 5] # random start


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

            is_collision = snake.border_collision()
            food_collision = snake.food_collision(food)

            if (food_collision):
                self.screen.addstr(food[1], food[0], " ")
                self.score += 1
                # snake.tail.insert(0, [food[0] - WINDOW_OFFSET, food[1] - WINDOW_OFFSET])
                food = [random.randint(3, snake_w-1), random.randint(3, snake_h-1)]
                
                print("Food spawn!: " + str(food))

            snake.update()
            self.screen.addstr(1, self.width -20, "Score: " + str(self.score))
            self.screen.addstr(food[1], food[0], "x")
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
    