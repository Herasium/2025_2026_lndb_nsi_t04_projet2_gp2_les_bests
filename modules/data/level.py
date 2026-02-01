import json
import os

from modules.data.chip import Chip
from modules.ui.toolbox.id_generator import random_id
from modules.data import data
from modules.logger import Logger

logger = Logger("Level")

class Level():

    def __init__(self,id):
        
        self.chip = Chip(id)
        self.number = 0
        self.time = 300
        self.id = f"level_{id}"
        self.name = "Default Level"
        self.description = "Basic level to learn the basis of gates."
        self.hints = []
    
    def save(self):
        chip_save = self.chip.save(no_file=True)

        result = {
            "chip": chip_save,
            "level": {
                "time":self.time,
                "id": self.id,
                "number": self.number,
                "name": self.name,
                "description": self.description,
                "hints": self.hints,
                "version": data.VERSION
            }
        }

        dump = json.dumps(result,indent=1)
        path = data.current_path
        os.makedirs(os.path.join(path,"levels"), exist_ok=True) 
        with open(os.path.join(os.path.join(path,"levels"),f"{self.id}.level"),"wb") as file:
            file.write(dump.encode())

    def load(self,data):
        
        self.chip.load(data["chip"])
        self.time = data["level"]["time"]
        self.id = data["level"]["id"]
        self.number = data["level"]["number"]
        self.description = data["level"]["description"]
        self.hints = data["level"]["hints"]
        self.name = data["level"]["name"]

        logger.debug(f"Loaded Level {self}")

    def __str__(self):
        result = f"Level (#{self.id}) {self.name} {self.number}"
        return result

