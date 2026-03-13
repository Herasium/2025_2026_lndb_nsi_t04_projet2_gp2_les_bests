
class English:

    def __init__(self):
        
        self.tutorial = {
            "button_1" : "-> How to play ?"
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
            "button_1" : "-> Comment jouer ?"
        }

    
    def get(self, menu, key):
        if menu in self.__dict__:
            if key in self.__dict__[menu]:
                return self.__dict__[menu][key]
            else:
                return f"Key '{key}' not found in menu '{menu}'"
        else:
            return f"Menu '{menu}' not found"