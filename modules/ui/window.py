
import arcade
from modules.data import data

class Window():

    def __init__(self):
        
        self.width = data.WINDOW_WIDTH
        self.height = data.WINDOW_HEIGHT
        self.title = "LogicBox"

        self.window = arcade.Window(self.width, self.height, self.title,fullscreen=data.WINDOW_FULLSCREEN, update_rate = 0.00001, draw_rate = 0.00001)
        self.view_history = []

    def back(self):
        self.view_history.pop()
        view = self.view_history[-1]
        self.window.show_view(view)

    def first(self):
        view = self.view_history[0]
        self.window.show_view(view)
        self.view_history=[]

    def run(self):
        arcade.run()

    def display(self,view: arcade.View):
        self.view_history.append(view)
        self.window.show_view(view)

    def hide(self):
        self.window.hide_view()