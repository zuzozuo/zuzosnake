#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-

import curses
import random
from consts import FOOD_S, HEAD_S, TAIL_S, MAX_FOOD_NUMBER

# ---- CLASSES 

class Snake:
    def __init__(self, w, h, win_x, win_y): 
        self.width = w
        self.height = h
        self.win_x = win_x 
        self.win_y = win_y 
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

    
    def spawn_food(self):

        if len(self.food) > MAX_FOOD_NUMBER:
            return

        x = random.randint(self.win_x + 2, self.width - 2)
        y = random.randint(self.win_y, self.height - 2)

        for _ in range(0, random.randint(1, 3)):
            while (([x, y] in self.tail) or ([x, y] in self.food)): 
                x = random.randint(self.win_x + 2, self.width - 2)
                y = random.randint(self.win_y, self.height - 2)

            self.food.append([x, y])

        for food in self.food:
            self.window.addstr(food[1], food[0], FOOD_S) 

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
            self.spawn_food()

            self.window.refresh()


        self.tail.insert(0, [self.x, self.y])

        if(len(self.tail) > 1):
            to_del = self.tail.pop()

        self.window.addstr(to_del[1], to_del[0], " ")        
        
        # drawing head
        self.window.addstr(self.tail[0][1], self.tail[0][0], HEAD_S) 

        # drawing the rest of the body
        for i in range(1, len(self.tail)):
            self.window.addstr(self.tail[i][1], self.tail[i][0], TAIL_S)
        
        self.window.refresh()