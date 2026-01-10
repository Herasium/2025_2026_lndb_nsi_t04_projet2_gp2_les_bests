

class Chip:
    def __init__(self):
        self.paths = {}
        self.gates = {}

    def __str__(self):

        result = f"Chip (#NAN) \n Gates:"

        for i in self.gates:
            result += f"\t {self.gates[i]} \n"

        result += " Paths: \n"

        for i in self.paths:
            result += f"\t {self.paths[i]} \n"

        return result