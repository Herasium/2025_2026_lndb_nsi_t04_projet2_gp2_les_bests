
class English:

    def __init__(self):
        
        self.tutorial = {
            "button_1" : "-> How to play ?",
            "button_2" : "-> Keyboard commands",
            "button_3" : "-> INPUT",
            "button_4" : "-> OUTPUT",
            "button_5" : "-> AND",
            "button_6" : "-> NOT",
            "button_7" : "-> OR",
            "button_8" : "-> NAND",
            "button_9" : "-> NOR",
            "button_10" : "-> XOR",
            "button_11" : "-> CLOCK",
            "button_12" : "-> PASS",
            "title_1" : "Rules",
            "title_2" : "Logic gates",
            "button_01" : "Drag gates from the hotbar\n "
                "to the playground. You can click on the output port\n "
                "of a gate to create a wire \n "
                "and then on the input port\n "
                "of another gate to connect them.",
            "button_02" : "def"

        }

    def get(self, menu, key):
        if menu in self.__dict__:
            if key in self.__dict__[menu]:
                return self.__dict__[menu][key]
            else:
                return f"Key '{key}' not found in menu '{menu}'"
        else:
            return f"Menu '{menu}' not found"


class French:
    
    def __init__(self):

        self.tutorial = {
            "button_1" : "-> Comment jouer ?",
            "button_2" : "-> Commandes clavier",
            "button_3" : "-> INPUT",
            "button_4" : "-> OUTPUT",
            "button_5" : "-> AND",
            "button_6" : "-> NOT",
            "button_7" : "-> OR",
            "button_8" : "-> NAND",
            "button_9" : "-> NOR",
            "button_10" : "-> XOR",
            "button_11" : "-> CLOCK",
            "button_12" : "-> PASS",
            "title_1" : "Règles",
            "title_2" : "Portes logiques",
            "button_01" : "zyx",
            "button_02" : "wvu"
        }

    
    def get(self, menu, key):
        if menu in self.__dict__:
            if key in self.__dict__[menu]:
                return self.__dict__[menu][key]
            else:
                return f"Clé '{key}' non trouvée dans menu '{menu}'."
        else:
            return f"Menu '{menu}' non trouvé."
