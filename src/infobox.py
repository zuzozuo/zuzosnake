import curses

class InfoBox:
    def __init__(self, w, h, win_x, win_y):
        self.width = w
        self.height = h
        self.win_x = win_x
        self.win_y = win_y

        self.window = curses.newwin(h, w, win_y, win_x)
        self.window.clear()
        self.window.box()
        self.window.border(1)

        self.text = "T E S T"

    def get_data(self, text):
        self.text = text

    
    def update(self):
        self.window.addstr(self.win_y, self.win_x + 1, self.text)
        self.window.refresh()