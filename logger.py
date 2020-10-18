class Logger:
    def __init__(self, window):
        self.window = window

    def log(self, str):
        self.window.insertln()
        self.window.addstr(0, 0, str)
        self.window.refresh()
