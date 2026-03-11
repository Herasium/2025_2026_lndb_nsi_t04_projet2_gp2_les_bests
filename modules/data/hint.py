
from modules.data.chip import Chip

class Hint:
    def __init__(self,id):
        self.chip = Chip(f"hint_chip_{id}")
        self.text = "Default Hint"

        self.type = 0 #0: Textual, 1: Chip, 2: Both
        self.id = id

