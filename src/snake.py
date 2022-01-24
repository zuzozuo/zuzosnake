import curses
import random
import time

# ---- CLASSES 

class Snake:
    def __init__(self, w, h, win_x, win_y):
        self.width = w
        self.height = h
        self.win_x = win_x
        self.win_y = win_y
        self.current_dir = [0, random.choice([-1,1])]
        self.score = 0


        # SNAKE WINDOW INIT
        self.window = curses.newwin(h, w, win_y, win_x)
        self.window.clear()
        self.window.box()
        self.window.border(1)

        # SNAKE START RANDOM POSITIONS

        self.x = random.randint(2, int(w/2)) # current x pos
        self.y = random.randint(2, int(h/2)) # current y pos

        # SNAKE LIST
        self.tail = [[self.x, self.y]]

        # FOOD LIST
        self.food = []

    def move(self, direction):
        # NEW HEAD COORDS
        self.x += direction[0] 
        self.y += direction[1]

        self.current_dir = direction
    
    def spawn_food(self):

        x = random.randint(self.win_x + 2, self.width - 2)
        y = random.randint(self.win_y, self.height - 2)
        
        while (([x, y] in self.tail) or ([x, y] in self.food)): 
            x = random.randint(self.win_x + 2, self.width - 2)
            y = random.randint(self.win_y, self.height - 2)

        self.food.append([x, y])

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

    # ----- 
    def add_score(self):
        self.score +=1
    
    def get_score(self):
        return self.score

    # ----- 
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
        
        # drawing head
        self.window.addstr(self.tail[0][1], self.tail[0][0], "#") 

        # drawing the rest of the body
        for i in range(1, len(self.tail)):
            self.window.addstr(self.tail[i][1], self.tail[i][0], "o")
        
        self.window.refresh()