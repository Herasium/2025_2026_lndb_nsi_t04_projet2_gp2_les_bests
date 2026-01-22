import json
from modules.data import data
from modules.data.gate_index import gate_types
from modules.data.nodes.path import Path
import os 
import zlib

class Chip:
    def __init__(self,id):
        self.paths = {}
        self.gates = {}
        self.id = id
        self.name = "Default Chip"
        self.type = "Chip"

    def save(self):
        paths = {}
        gates = {}

        for id in self.paths:
            paths[id] = self.paths[id].save()

        for id in self.gates:
            gates[id] = self.gates[id].save()

        result = {
            "type": self.type,
            "name": self.name,
            "id": self.id,
            "gates": gates,
            "paths": paths,
            "version": "0.12"
        }

        dump = json.dumps(result)
        path = data.current_path

        with open(os.path.join(os.path.join(path,"saves"),f"{self.id}.chip"),"wb") as file:
            file.write(zlib.compress(dump.encode()))

        print(f'Saved {self.name}, #{self.id}')

    def load(self,data):
        self.type = data["type"]
        self.name = data["name"]
        self.id = data["id"]

        for key in data["gates"]:
            gate = data["gates"][key]
            if gate["type"] == "Gate":
                new = gate_types[gate["gate"]]("default_id")
            else:
                new = gate_types[gate["type"]]("default_id")

            new.load(gate)
            self.gates[key] = new

        for key in data["paths"]:
            new = Path("default_id")
            new.load(data["paths"][key])
            self.paths[key] = new

        print(f"Loaded Chip {self}")

    def __str__(self):

        result = f"Chip (#{self.id}) \n Gates:"

        for i in self.gates:
            result += f"\t {self.gates[i]} \n"

        result += " Paths: \n"

        for i in self.paths:
            result += f"\t {self.paths[i]} \n"

        return result