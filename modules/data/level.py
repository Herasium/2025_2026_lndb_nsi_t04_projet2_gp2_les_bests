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
        self.truth = {}
        self.start = 1
        self.play = False
        self.answer = None
        self.max_usage = {}
        self.inventory = {}

    def play_mode(self):
        self.play = True
        self.answer = self.chip
        self.chip = Chip(f"play_{self.id}")
        self.chip.load(self.answer.save(no_file=True))
        self.chip.id = f"chip_{self.id}"

        self.chip.paths = {}

        left = self.get_gates(self.chip)

        keys_to_delete = [i for i in self.chip.gates.keys() if i in left]
        for key in keys_to_delete:
            del self.chip.gates[key]

        self.calculate_inventory()
        self.get_truth_table(answer=True)

    def calculate_inventory(self):
        self.max_usage = {}
        for i in self.answer.gates:
            if not self.answer.gates[i].gate_type in self.max_usage:
                self.max_usage[self.answer.gates[i].gate_type] = 0
            self.max_usage[self.answer.gates[i].gate_type] += 1

        self.inventory = {}
        for i in self.chip.gates:
            if not self.chip.gates[i].gate_type in self.inventory:
                self.inventory[self.chip.gates[i].gate_type] = 0
            self.inventory[self.chip.gates[i].gate_type] += 1



    def start_chip(self, chip = None):
        if chip == None:
            chip = self.chip

        if self.start == 1:
            for i in chip.gates:
                chip.gates[i].inputs = [False for _ in chip.gates[i].inputs]
                chip.gates[i].outputs = [False for _ in chip.gates[i].outputs]
        if self.start == 2:
            for i in chip.gates:
                chip.gates[i].inputs = [True for _ in chip.gates[i].inputs]
                chip.gates[i].outputs = [True for _ in chip.gates[i].outputs]

    def get_inputs(self, chip = None):
        if chip == None:
            chip = self.chip
        result = []
        for i in self.chip.gates:
            if self.chip.gates[i].type == "Input":
                result.append(i)
        return result
    
    def get_outputs(self, chip = None):
        if chip == None:
            chip = self.chip
        result = []
        for i in self.chip.gates:
            if self.chip.gates[i].type == "Output":
                result.append(i)
        return result
    
    def get_gates(self, chip = None):
        if chip == None:
            chip = self.chip
        result = []
        for i in self.chip.gates:
            if self.chip.gates[i].type == "Gate":
                result.append(i)
        return result

    def get_single_truth_table(self,chip):

        copy = Chip("copy_chip")
        copy.load(chip.save(no_file=True))

        self.start_chip(copy)
        propagate_values(copy)
        inputs = self.get_inputs(copy)
        outputs = self.get_outputs(copy)
        size = len(inputs)
        self.truth[chip.id]["meta"]["size"] = size
        self.truth[chip.id]["meta"]["inputs"] = inputs
        self.truth[chip.id]["meta"]["outputs"] = outputs
        power = 2 ** size
        self.truth[chip.id]["meta"]["power"] = power
        for current in range(power):
            values = [bool(current & (1 << i)) for i in range(size)]
            for index in range(len(inputs)):
                copy.gates[inputs[index]].outputs[0] = values[index]
            propagate_values(copy)
            result = [copy.gates[i].inputs[0] for i in outputs]
            int_value = sum(b << i for i, b in enumerate(reversed(values)))
            self.truth[chip.id]["data"][int_value] = result

    def get_truth_table(self,answer=False):

        used = self.chip
        if answer:
            used = self.answer
        self.truth[used.id] = {"meta": {}, "data": {}}
        self.get_single_truth_table(used)


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

        logger.debug(f"Loaded Level {self}")

    def __str__(self):
        result = f"Level (#{self.id}) {self.name} {self.number}"
        return result

