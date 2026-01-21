import json
from modules.data import data
import os 
import zlib

class Chip:
    def __init__(self):
        self.paths = {}
        self.gates = {}
        self.id = "default_chip"
        self.name = "Default Chip"

    def save(self):
        result = {}

        for id in self.paths:
            result[id] = self.paths[id].save()

        for id in self.gates:
            result[id] = self.gates[id].save()

        dump = json.dumps(result)
        path = data.current_path

        with open(os.path.join(os.path.join(path,"saves"),f"{self.id}.chip"),"wb") as file:
            file.write(zlib.compress(dump.encode()))


    def __str__(self):

        result = f"Chip (#NAN) \n Gates:"

        for i in self.gates:
            result += f"\t {self.gates[i]} \n"

        result += " Paths: \n"

        for i in self.paths:
            result += f"\t {self.paths[i]} \n"

        return result