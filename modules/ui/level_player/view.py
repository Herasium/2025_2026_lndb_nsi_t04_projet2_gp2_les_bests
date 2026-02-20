import arcade
from line_profiler import profile
from PIL import Image
from pyglet.graphics import Batch
import time

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.grid import Grid
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.id_generator import random_id
from modules.ui.toolbox.easing import BackEaseOut, ElasticEaseOut

from modules.data.nodes.path import Path

from modules.data.nodes.nand import Nand
from modules.data.nodes.gand import And
from modules.data.nodes.gor import Or
from modules.data.nodes.gnot import Not
from modules.data.nodes.xor import Xor
from modules.data.nodes.nor import Nor

from modules.data.nodes.input import Input
from modules.data.nodes.output import Output
from modules.data.chip import Chip

from modules.data import data
from modules.data.gate_index import gate_types

from modules.logger import Logger

from modules.engine.logic import propagate_values

logger = Logger("LevelPlayer")

class LevelPlayer(arcade.View):

    def __init__(self,id=None):
        super().__init__()

        self.follower = Entity()
        self.follower.height = data.UI_EDITOR_GRID_SIZE
        self.follower.width = data.UI_EDITOR_GRID_SIZE

        self.bottom_zone_collider = Entity()
        self.bottom_zone_collider.x = 0
        self.bottom_zone_collider.y = 0
        self.bottom_zone_collider.width = 1920
        self.bottom_zone_collider.height = 3*64

        self.selected_follower = None
        self.moving_gate = None
        self.current_path = None

        if id == None:
            logger.error("No level id provided, going back.")
            data.window.back()
            arcade.quit()
        else:
            if id in data.loaded_levels:
                self.level = data.loaded_levels[id]
                self.level.play_mode()
            else:
                logger.error("Invalid level id provided, going back.")
                data.window.back()
                arcade.quit()

        self.moving_gate_offset = (0, 0)

        self._real_camera_position = (0,0)
        self.camera_position = (0,0)

        self.bottom_gates = []
        self.bottom_gate_bar()

        self.background_color = arcade.types.Color.from_hex_string("121212")

        self.camera_hold = False
        self.fps = 0
        self.delta_time = 1
        self.frame_count = 0
        self.last_time = 1

        self.stress_test = False

        if self.stress_test:
            self.perf_graph_list = arcade.SpriteList()

            graph = arcade.PerfGraph(400, 400, graph_data="FPS")
            graph.position = 200, 200
            self.perf_graph_list.append(graph)

        self.prepare_right_frame()
        self.prepare_won_frame()

    def prepare_won_frame(self):
        self.win_frame_ease = BackEaseOut(-500,1080/2-(320),90)
        self.win_frame = Entity(x=1920/2-(576),y=-500,width=576*2,height=320*2,sprite=data.level_player_win)
        

    def prepare_right_frame(self):

        self.check_button = Entity(x=1402,y=57,width=216,height=128,sprite=data.button_check)
        self.truth_table = Entity(x=1402,y=1080-383,width=448,height=64,sprite=data.truth_table)
        self.button_next_off = Entity(x=1634,y=57,width=216,height=128,sprite=data.button_next_off)
        self.level_info = Entity(x=1402,y=1080-127,width=448,height=64,sprite=data.level_info)

        self.level_name_text = arcade.Text(f"Level {self.level.number} : {self.level.name}",
            1408, 
            900, 
            arcade.color.WHITE,  
            12,
            font_name="Press Start 2P",
        )

        self.level_desc_text = []
        texts = self.level.description.split(" ")
        c = 0

        for _ in range(len(texts)):

            if c > len(texts) - 2:
                break

            if len(texts[c] + texts[c+1]) + 1 <= 24:
                b = texts.pop(c+1)
                texts[c] += " "+b
            else:
                c += 1

        for i in range(len(texts)):

            self.level_desc_text.append(arcade.Text(texts[i], 
                1408, 
                850 - 25*i, 
                arcade.color.WHITE,  
                10,
                font_name="Press Start 2P",
            ))

        table = self.level.truth[self.level.answer.id]
        chip_truth = None

        if self.level.chip.id in self.level.truth:
            chip_truth = self.level.truth[self.level.chip.id]
   
        self.truth_table_inputs = [[] for _ in range(len(table["meta"]["inputs"]))]
        self.truth_table_outputs = [[] for _ in range(len(table["meta"]["outputs"]))]
        self.line_set = []
        self.truth_table_titles = []

        add_y = 28
        add_x = 27

        total_len = (len(table["data"][0])*2+table["meta"]["size"]+4) * add_x

        start_x = 1402 + (7*32) - ((len(table["data"][0])*2+table["meta"]["size"]+4)/2*add_x)
        start_y = 1080-(447)

        offset_x = 0
        offset_y = 0

        self.line_set.append([(start_x - 10,start_y-offset_y+add_y-4),(start_x+total_len+10,start_y+add_y-offset_y-4)])
        self.truth_table_titles.append(arcade.Text("Inputs", 
                    start_x + (table["meta"]["size"]/2)*add_x, 
                    start_y + add_y + 5, 
                    arcade.color.WHITE,  
                    10,
                    font_name="Press Start 2P",
                    anchor_x="center"
        ))
        self.truth_table_titles.append(arcade.Text("Target", 
                    start_x + (table["meta"]["size"] + 2 + len(table["data"][0])/2)*add_x-5, 
                    start_y + add_y + 5, 
                    arcade.color.WHITE,  
                    9,
                    font_name="Press Start 2P",
                    anchor_x="center"
        ))

        self.truth_table_titles.append(arcade.Text("Current", 
                    start_x + (table["meta"]["size"] + 4 + len(table["data"][0])*1.5)*add_x, 
                    start_y + add_y + 5, 
                    arcade.color.WHITE,  
                    9,
                    font_name="Press Start 2P",
                    anchor_x="center"
        ))



        for current in range(table["meta"]["power"]):
            values = [bool(current & (1 << i)) for i in range(table["meta"]["size"])]
            for i in range(len(values)):
                self.truth_table_inputs[i].append(arcade.Text(str(values[i] * 1), 
                    start_x + offset_x, 
                    start_y - offset_y, 
                    arcade.color.WHITE,  
                    14,
                    font_name="Press Start 2P",
                ))

                offset_x += add_x
            offset_x += add_x*2
            for i in range(len(table["data"][current])):
                self.truth_table_outputs[i].append(arcade.Text(str(table["data"][current][i] * 1), 
                    start_x + offset_x, 
                    start_y - offset_y, 
                    arcade.color.WHITE,  
                    14,
                    font_name="Press Start 2P",
                ))

                offset_x += add_x
            offset_x += add_x*2
            if chip_truth:
                for i in range(len(chip_truth["data"][current])):

                    color = arcade.color.RED_PURPLE
                    if table["data"][current][i] == chip_truth["data"][current][i]:
                        color = arcade.color.GREEN_YELLOW

                    self.truth_table_outputs[i].append(arcade.Text(str(chip_truth["data"][current][i] * 1), 
                        start_x + offset_x, 
                        start_y - offset_y, 
                        color,  
                        14,
                        font_name="Press Start 2P",
                    ))

                    offset_x += add_x
            else:
                for i in range(len(table["data"][current])):
                    self.truth_table_outputs[i].append(arcade.Text("?", 
                        start_x + offset_x, 
                        start_y - offset_y, 
                        arcade.color.WHITE,  
                        14,
                        font_name="Press Start 2P",
                    ))

                    offset_x += add_x
      
            self.line_set.append([(start_x - 10,start_y-offset_y-4),(start_x+offset_x+10,start_y-offset_y-4)])
            offset_x = 0
            offset_y += add_y
            

    def bottom_bar_width_sum(self):
        result = 0
        for i in self.bottom_gates:
            result += i.tile_width
        return result

    def bottom_gate_bar(self):
        self.bottom_gates = []
        for i in self.level.max_usage:
            if i != "Input" and i != "Output":
                position = (self.bottom_bar_width_sum()+len(self.bottom_gates))*data.UI_EDITOR_GRID_SIZE + 64 
                self.bottom_gates.append(gate_types[i](f"bottom_gate_{random_id()}"))
                self.bottom_gates[-1].camera = (0,0)
                self.bottom_gates[-1].y = (3*data.UI_EDITOR_GRID_SIZE)
                self.bottom_gates[-1].x = position
                

    def get_hovered_bottom_gate(self):
        for i in self.bottom_gates:
            if i.entity.touched :
                return i.gate_type

    def draw_bottom_gates(self):
        for i in self.bottom_gates:
            i.draw()


    def reset(self):
        pass

    def draw_frame_border(self):

        rect = arcade.XYWH(
                x=0,
                y=0,
                width=1920,
                height=1080,
                anchor=arcade.Vec2(0,0)
            )

        arcade.draw_sprite_rect(data.level_player_border,rect)

    def draw_frame_background(self):

        rect = arcade.XYWH(
                x=0,
                y=0,
                width=1920,
                height=1088,
                anchor=arcade.Vec2(0,0)
            )

        arcade.draw_texture_rect(data.background_grid_texture,rect)



    def draw_debug_text(self):

        debug_list = [
            f"Camera: {self.camera_position}",
            f"FPS: {self.fps} / {round(self.delta_time*100000)/100} ms / {self.frame_count}",
            f"Objects: {len(self.level.chip.gates.keys())}g/{len(self.level.chip.paths.keys())}p"
        ]

        start_y = 1080-70
        
        for index, item in enumerate(debug_list):
            arcade.draw_text(
                item, 
                64,  
                start_y - (index * 25), 
                arcade.color.WHITE,  
                14,
                font_name="Press Start 2P",
            )

    def draw_won(self):
        value = self.win_frame_ease.tick()
        self.win_frame.y = value
        self.win_frame.draw()

    def draw_right(self):

        self.check_button.draw()
        self.truth_table.draw()
        self.button_next_off.draw()
        self.level_info.draw()

            
        self.level_name_text.draw()

        for i in self.level_desc_text: i.draw()

        for i in self.truth_table_inputs: 
            for a in i: 
                a.draw()

        for i in self.truth_table_outputs: 
            for a in i: 
                a.draw()

        for coords in self.line_set:
            arcade.draw_line(coords[0][0],coords[0][1],coords[1][0],coords[1][1],arcade.color.WHITE,1)

        for i in self.truth_table_titles:
            i.draw()

    @profile
    def on_draw(self):
        self.clear()


        self.draw_frame_background()
        for p in self.level.chip.paths.values():
            p.draw()

        for g in self.level.chip.gates.values():
            g.draw()

        if self.current_path:
            self.current_path.draw()

        if self.selected_follower:
            self.selected_follower.draw()

        self.draw_debug_text()
        self.draw_frame_border()
        self.draw_bottom_gates()
        self.draw_right()
        if self.level.won:
            self.draw_won()

        if self.stress_test:
            self.perf_graph_list.draw()

        self.frame_count += 1
        self.delta_time = time.time() - self.last_time
        self.last_time = time.time()
        
    def on_update(self, delta_time):
        self.fps = 1/self.delta_time*10000//10000
        self.simulate()


    def on_key_press(self, key, key_modifiers):

        if key == 101: #e
            for g in self.level.chip.gates.values():
                if g.entity.touched and g.type == "Input":
                    g.switch()

        if key == 97:  # "a"
            data.window.back()
        if key == 65307:  # ESC
            if self.current_path:
                self.current_path.abort()
            self.current_path = None
            self.selected_follower = None

        if key == 115: # s
            self.level.chip.save()

        if key == 65288:
            self.delete()

    def delete_gate(self,id):
        to_delete = []

        if self.level.chip.gates[id].type == "Gate":
            for index in self.level.chip.paths.keys():
                p = self.level.chip.paths[index]

                for input in p.inputs:
                    if input[1] == id:
                        p.remove_branch(input[4])
                        if p.empty:
                            to_delete.append(index)
                            continue
                        p.clean_out_single_branch()

                for output in p.outputs:
                    if output[1] == id:
                        p.remove_branch(output[4])
                        if p.empty:
                            to_delete.append(index)
                            continue
                        p.clean_out_single_branch()

            del self.level.chip.gates[id]
            for i in to_delete:
                del self.level.chip.paths[i]

            self.level.chip.changed = True

    def delete(self):

        for g in self.level.chip.gates.values():
            if g.entity.touched:
                self.delete_gate(g.id)
                break

        for p in self.level.chip.paths.values():
            if p.touched:
                p.remove_branch(p.get_touched_branch)
                if p.empty:
                    del self.level.chip.paths[p.id]
                    break
                p.clean_out_single_branch()
                break

        self.level.chip.changed = True


    def on_key_release(self, key, key_modifiers):
        pass


    @property
    def camera(self):
        return self.camera_position

    @camera.setter
    
    def camera(self,value):
        self._real_camera_position = value
        self.camera_position = ((self._real_camera_position[0] // data.UI_EDITOR_GRID_SIZE) * data.UI_EDITOR_GRID_SIZE,(self._real_camera_position[1] // data.UI_EDITOR_GRID_SIZE) * data.UI_EDITOR_GRID_SIZE)
        for g in self.level.chip.gates:
            self.level.chip.gates[g].camera_moving(self.camera_position)
        for p in self.level.chip.paths:
            self.level.chip.paths[p].camera = self.camera_position
        if self.current_path:
            self.current_path.camera = self.camera_position

    
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x, y)
        
        self.follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2
        self.follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2

        if self.camera_hold:
            self.camera = (self._real_camera_position[0] + delta_x, self._real_camera_position[1] + delta_y)
            #self.camera = (self.camera_position[0] + delta_x, self.camera_position[1] + delta_y)


        if self.selected_follower:
            self.selected_follower._camera = (0,0)
            self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2 
            self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2 

        if self.moving_gate:
            self.moving_gate.x = mouse.cursor[0] - self.moving_gate_offset[0] 
            self.moving_gate.y = mouse.cursor[1] - self.moving_gate_offset[1] 

            # update connected paths
            for path in self.level.chip.paths.values():
                connected_inputs, connected_outputs = path.get_connected_points(self.moving_gate.id)
                modified = False

                for i in connected_inputs:
                    modified = True
                    position = self.moving_gate.outputs_position[i[2]]
                    position = (position[0]- self.camera_position[0] ,position[1] - self.camera_position[1] )
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = position
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = position

                for i in connected_outputs:
                    modified = True
                    position = self.moving_gate.inputs_position[i[2]]
                    position = (position[0] - self.camera_position[0] ,position[1] - self.camera_position[1] )
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = position
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = position

                if modified:
                    self.level.chip.changed = True
                    path.recalculate_hitbox()

    def simulate(self):
        propagate_values(self.level.chip)

        if self.level.chip.changed:
            self.level.chip.changed = False
            self.level.calculate_inventory()
            self.bottom_gate_bar()

    def won(sefl):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):

        if button == 2:
            self.camera_hold = True
            return
        if self.camera_hold:
            return

        if self.check_button.touched:
            self.level.get_truth_table()
            self.prepare_right_frame()
            if self.level.check_victory():
                self.won()
            return

        # Clicked a gate?
        for g in self.level.chip.gates.values():
            touched = g.touched
            if touched:
                if self.current_path is None:
                    # start new path
                    pid = random_id()
                    self.current_path = Path(pid)
                    self.current_path.camera = self.camera
                    self.current_path.add_path()

                    if touched[0] == 1: #Input touched
                        self.current_path.outputs.append([1, g.id, touched[1], 1, self.current_path.current_branch_count])
                    else: #Output touched
                        self.current_path.inputs.append([2, g.id, touched[1], 1, self.current_path.current_branch_count])
                    self.level.chip.changed = True
                    return
                

                else:
                    # finish existing path
                    if touched[0] == 1:#Input touched
                        self.current_path.outputs.append([1, g.id, touched[1], 2, self.current_path.current_branch_count])
                    else:#Output touched
                        self.current_path.inputs.append([2, g.id, touched[1], 2, self.current_path.current_branch_count])
                    self.current_path.camera = self.camera
                    self.current_path.finish()
                    if self.current_path.id not in self.level.chip.paths:
                        self.level.chip.paths[self.current_path.id] = self.current_path

                    self.current_path = None
                    self.level.chip.changed = True
                    return

        # Clicking on a path
        if not self.current_path:
            for p in self.level.chip.paths.values():
                if p.touched:
                    p.add_path()
                    self.current_path = p
                    self.level.chip.changed = True
                    return
        else:
            for p in self.level.chip.paths.values():
                if p.touched and p != self.current_path:
                    self.current_path.add_path()
                    p.merge(self.current_path)

                    if self.current_path.id in self.level.chip.paths:
                        del self.level.chip.paths[self.current_path.id]

                    self.current_path = None
                    self.level.chip.changed = True
                    return

            self.current_path.add_path()
            self.level.chip.changed = True
            return

        # Move a gate
        if self.moving_gate is None:
            for g in self.level.chip.gates.values():
                if g.entity.touched:
                    self.moving_gate_offset = (
                        mouse.cursor[0] - g.x,
                        mouse.cursor[1] - g.y
                    )
                    self.moving_gate = g
                    return

        # Place new gate
        if self.selected_follower is None:
            hovered = self.get_hovered_bottom_gate()
            if hovered in gate_types:
                self.selected_follower =  gate_types[hovered](random_id())
                self.selected_follower.camera = self.camera
                self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[0]
                self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[1]


    def on_mouse_release(self, x, y, button, key_modifiers):
        
        if button == 2:
            self.camera_hold = False

            for g in self.level.chip.gates:
                self.level.chip.gates[g].camera = self.camera_position

        else:
            if not self.selected_follower is None:

                if self.bottom_zone_collider.touched:
                    self.selected_follower = None
                else:
                    self.level.chip.gates[self.selected_follower.id] = self.selected_follower
                    self.selected_follower.camera = self.camera
                    self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[0]
                    self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[1]
                    self.selected_follower = None
                    self.level.chip.changed = True
                    

        self.moving_gate = None
        self.moving_gate_offset = (0, 0)
