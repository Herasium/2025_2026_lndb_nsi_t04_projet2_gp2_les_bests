from os import listdir
from os.path import isfile, join
import zlib
import json
from modules.data import data
from modules.data.chip import Chip
import arcade
import traceback


def load_saves():

    saves = join(data.current_path,"saves")
    files = [f for f in listdir(saves) if isfile(join(saves, f))]
    read = []

    for file_path in files:
        complete = join(saves,file_path)
        try: 
            with open(complete,"rb") as file:
                raw= file.read()
                file.close()

            dump = zlib.decompress(raw).decode()
            loaded = json.loads(dump)
            read.append(loaded)
        except Exception as e:
            print(f"Failed to read file {complete} ({e})")

    for i in read:
        try:
            new = Chip("default_id")
            new.load(i)
            data.loaded_chips[i["id"]] = new
        except Exception as e: 
             print(f"Failed to load chip \n\n{i}\n\n")
             print(traceback.format_exc())

def load_tiles():
        
        ui_border_sheet = arcade.SpriteSheet("assets/ui_border_grid.png")

        ui_border_tiles = ui_border_sheet.get_texture_grid(
            size = (64, 64),
            columns = 4,
            count = 4*4,
        )

        data.ui_border_tiles = ui_border_tiles

        gate_sheet = arcade.SpriteSheet("assets/gate_grid.png")

        gate_tiles = gate_sheet.get_texture_grid(
            size=(data.UI_EDITOR_GRID_SIZE, data.UI_EDITOR_GRID_SIZE),
            columns=6,
            count=6*6
        )

        data.gate_tiles = gate_tiles

def load_font():
     arcade.load_font("assets/press_start.ttf")
