import curses



# TESTING SCREEN INIT USING CURSES

screen_y, screen_x  = curses.initscr().getmaxyx()
curses.noecho()
game_screen = curses.newwin(screen_y//2, screen_x//2, 1, 0)
curses.curs_set(0)
game_screen.keypad(True) #enable keypad
game_screen.nodelay(False)


key = curses.KEY_LEFT
y = screen_y//4
x = screen_x//4
text = "Wowsie!"
while(key !=curses.KEY_RIGHT):
    game_screen.border(1)
    game_screen.addstr(y, x, text)
    event = game_screen.getch()
    print(event)
    if(event != -1):
        key = event

    if(key == curses.KEY_DOWN):
        game_screen.addstr(y + 1, x, str("Wowsie!"))
        game_screen.addstr(y, x, str("".join([" " for i in range(0,len(text))])))
        y += 1