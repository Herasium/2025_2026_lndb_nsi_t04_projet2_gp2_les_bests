class COLORS:
    VALUE_ON = "DC2626"
    VALUE_OFF = "D9D9D9"
        
class ImageBuffer():
    def __init__(self):

        self.buffer = {}

    def add_gate_type(self,id):
        self.buffer[id] = {
            "complete": False,
            "textures": {}
        }

    def add_texture(self,id,texture_id,texture):
        self.buffer[id]["textures"][texture_id] = texture

    def get_texture(self,id,texture_id):
        if texture_id in self.buffer[id]["textures"]:
            return self.buffer[id]["textures"][texture_id]
        else:
            return False

    def complete_gate(self,id):
        self.buffer[id]["complete"] = True

    def is_complete_gate(self,id):
        return self.buffer[id]["complete"]

class LevelButtonsBuffer():

    def __init__(self):
        self.buffer = {}

    def get(self,id):
        return self.buffer[id]
    
    def set(self,id,image):
        self.buffer[id] = image
        

class Data:
    def __init__(self):
        self.WINDOW_WIDTH = 1920
        self.WINDOW_HEIGHT = 1080
        self.WINDOW_FULLSCREEN = True
        self.UI_EDITOR_GRID_SIZE = 27
        self.VERSION = "a.160"
        self.COLORS = COLORS
        self.IMAGE = ImageBuffer()
        self.LEVEL_BUTTONS = LevelButtonsBuffer()
        self.loaded_chips = {}
        self.loaded_levels = {}
        self.window = None
        self.level_colors = ["green","yellow","orange","red"]
        self.categories = ["Fondamentals of logic","Some basic gates","Some NANDic gates"]

data = Data()