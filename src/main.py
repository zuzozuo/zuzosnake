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
        self.current_dir = [random.choice([-1,1]), random.choice([-1,1])]
        self.score = 0


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

        # FOOD LIST
        self.food = [[random.randint(self.win_x+2, self.width-2), random.randint(self.win_y, self.height-2)]]

    
    def move(self, direction):
        # NEW HEAD COORDS
        self.x += direction[0] 
        self.y += direction[1]

        self.current_dir = direction
    
    def spawn_food(self):
        new_food = [random.randint(self.win_x+2, self.width-2), random.randint(self.win_y, self.height-2)]
        
        while ((new_food in self.tail) or (new_food in self.food)): 
            new_food = [random.randint(self.win_x+2, self.width-2), random.randint(self.win_y, self.height-2)]
            
        
        self.food.append(new_food)
    
    # ---- COLLISIONS
    def border_collision(self):

        if(self.x <= 0 or self.x >= self.width-1):
            return True
        
        if(self.y <= 0 or self.y >= self.height-1):
            return True
        return False

    def tail_collision(self):
        if ([self.x, self.y] in self.tail[2:]):
            return True

        return False
    
    def snake_tail(self):
        return self.tail
    #------ 
    def add_score(self):
        self.score +=1
    
    def get_score(self):
        return self.score

    def update(self):

        # FOOD COLLISION
        if ([self.x, self.y] in self.food):
            self.tail.insert(0, [self.x, self.y]) #insert new block at food position
            self.food.remove([self.x, self.y])     
            self.add_score()

            if(len(self.food) < 1):
                for i in range (0, random.randint(1,4)):
                    self.spawn_food()
            self.window.refresh()


        self.tail.insert(0, [self.x, self.y])

        if(len(self.tail) > 1):
            to_del = self.tail.pop()

        for food in self.food:
            self.window.addstr(food[1], food[0], "x")

        self.window.addstr(to_del[1], to_del[0], " ")        
        
        self.window.addstr(self.tail[0][1], self.tail[0][0], "O")

        for i in range(1, len(self.tail)):
            self.window.addstr(self.tail[i][1], self.tail[i][0], "o")
        
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
        self.screen.addstr(0,int(self.width/2)-5, str(self.width) + "x" + str(self.height)) # prints main window size
        self.screen.addstr(1, int(self.width/2)-5, "CURSED SNAKEE")
        self.screen.refresh()

        snake_w = self.width - 5
        snake_h = self.height - 5

        snake = Snake(snake_w, snake_h, WINDOW_OFFSET, WINDOW_OFFSET)

        self.screen.nodelay(True)

        is_collision = False
        key = 0 
        event = 0

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

            self.screen.addstr(1, self.width -20, "Score: " + str(snake.get_score()))
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
    