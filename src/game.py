from snake import Snake
from infobox import InfoBox
import curses
import time


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

        snake_w = int(self.width - 3)/2
        snake_h = self.height - 5

        snake = Snake(snake_w, snake_h, 2, 2)

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
            info.update()

            self.screen.addstr(1, self.width - 20, "Score: " + str(snake.get_score()))
            self.screen.refresh()
            time.sleep(0.1)
