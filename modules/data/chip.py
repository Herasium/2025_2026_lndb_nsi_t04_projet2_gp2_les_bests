import json
from modules.data import data
from modules.data.gate_index import gate_types
from modules.data.nodes.path import Path
from modules.logger import Logger
from modules.ui.toolbox.id_generator import random_id
from modules.data.custom import CustomGate
import os 

logger = Logger("Chip")

class Chip:
    def __init__(self,id):
        self.paths = {}
        self.gates = {}
        self.id = id
        self.name = "Default Chip"
        self.type = "Chip"
        self.changed = False
        self.requirements = []
        self.temp_data = None

    def copy(self):
        new = Chip("no_id")
        new.partial_load(json.loads(self.save(no_file=True,dojson=True)))
        new.load()
        new.id = random_id()
        return new

    def save(self,no_file=False, dojson= False):
        paths = {}
        gates = {}

        self.requirements = []

        for id in self.paths:
            paths[id] = self.paths[id].save()

        for id in self.gates:
            gates[id] = self.gates[id].save()
            if self.gates[id].type == "Custom":
                self.requirements.append(self.gates[id].base_chip_id)
                self.requirements += data.loaded_chips[self.gates[id].base_chip_id].requirements
        self.requirements = list(set(self.requirements)) #Removes duplicates
        print(self.requirements)
        result = {
            "type": self.type,
            "name": self.name,
            "id": self.id,
            "gates": gates,
            "paths": paths,
            "version": data.VERSION,
            "requirements": self.requirements
        }

        if no_file and not dojson:
            return result

        dump = json.dumps(result,indent=1)
        if dojson: return dump
        path = data.current_path
        os.makedirs(os.path.join(path,"saves"), exist_ok=True) 
        with open(os.path.join(os.path.join(path,"saves"),f"{self.id}.chip"),"wb") as file:
            file.write(dump.encode())
        
        logger.print(f'Saved {self.name}, #{self.id}')

    def partial_load(self,data):
        self.type = data["type"]
        self.name = data["name"]
        self.id = data["id"]
        if data["version"] != "a.136":
            self.requirements = data["requirements"]
        self.temp_data = data

    def load(self):
        if self.temp_data == None:
            logger.error("You must partial load a chip, before finishing load.")
            return
        data = self.temp_data
        for key in data["gates"]:
            gate = data["gates"][key]
            if gate["type"] == "Gate":
                new = gate_types[gate["gate"]]("default_id")
            elif gate["type"] == "Custom":
                new = CustomGate("default_id",self)
            else:
                new = gate_types[gate["type"]]("default_id")

            new.load(gate)
            self.gates[key] = new

        for key in data["paths"]:
            new = Path("default_id")
            new.load(data["paths"][key])
            self.paths[key] = new
        self.temp_data = None
        logger.debug(f"Loaded Chip {self}")

    def __str__(self):
        result = f"Chip (#{self.id}) {len(self.gates)} Gates / {len(self.paths)} Paths"
        return result
    
    def get_inputs(self):
        result = []
        for i in self.gates:
            if self.gates[i].type == "Input":
                result.append(i)
        return result
    
    def get_outputs(self):
        result = []
        for i in self.gates:
            if self.gates[i].type == "Output":
                result.append(i)
        return result
    
    def get_gates(self):
        result = []
        for i in self.gates:
            if self.gates[i].type == "Gate":
                result.append(i)
        return result