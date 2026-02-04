import json
import os

from modules.data.chip import Chip
from modules.ui.toolbox.id_generator import random_id
from modules.data import data
from modules.logger import Logger
from modules.engine.logic import propagate_values

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
        self.truth = []
        self.start = 1
        self.play = False
        self.answer = None

    def play_mode(self):
        self.play = True
        self.answer = self.chip
        self.chip = Chip(f"play_{self.id}")
        

    def start_chip(self):
        if self.start == 1:
            for i in self.chip.gates:
                self.chip.gates[i].inputs = [False for _ in self.chip.gates[i].inputs]
                self.chip.gates[i].outputs = [False for _ in self.chip.gates[i].outputs]
        if self.start == 2:
            for i in self.chip.gates:
                self.chip.gates[i].inputs = [True for _ in self.chip.gates[i].inputs]
                self.chip.gates[i].outputs = [True for _ in self.chip.gates[i].outputs]

    def get_inputs(self):
        result = []
        for i in self.chip.gates:
            if self.chip.gates[i].type == "Input":
                result.append(i)
        return result
    
    def get_outputs(self):
        result = []
        for i in self.chip.gates:
            if self.chip.gates[i].type == "Output":
                result.append(i)
        return result

    def get_single_truth_table(self):

        self.start_chip()
        propagate_values(self.chip)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        size = len(inputs)
        power = 2 ** size
        for current in range(power):
            values = [bool(current & (1 << i)) for i in range(size)]
            for index in range(len(inputs)):
                self.chip.gates[inputs[index]].outputs[0] = values[index]
            propagate_values(self.chip)
            result = [self.chip.gates[i].inputs[0] for i in outputs]
            int_value = sum(b << i for i, b in enumerate(reversed(values)))
            self.truth[self.start][int_value] = result

    def get_truth_table(self):
        self.truth = []
        initial = self.start
        for i in range(3):
            self.start = i
            self.truth.append({})
            self.get_single_truth_table()
        self.start = initial
        print(self.truth)

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
                "version": data.VERSION,
                "start": self.start,
                "truth": self.truth
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
        self.start = data["level"]["start"]
        self.truth = data["level"]["truth"]

        logger.debug(f"Loaded Level {self}")

    def __str__(self):
        result = f"Level (#{self.id}) {self.name} {self.number}"
        return result

