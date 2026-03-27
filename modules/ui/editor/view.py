import arcade
from line_profiler import profile
import time
from typing import Optional, List, Tuple, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.id_generator import random_id

from modules.data.nodes.path import Path
from modules.data.nodes.one.gand import And
from modules.data.chip import Chip
from modules.data.custom import CustomGate
from modules.data import data
from modules.data.gate_index import (
    gate_types,
    gate_types_1,
    gate_types_8,
    gate_types_mix,
)
from modules.engine import Engine
from modules.logger import Logger
from modules.ui.level_editor.save import SaveFrame
from modules.ui.editor.input import InputFrame
from modules.ui.editor.save import SaveFrame as EditorSaveFrame

"""Fournit l'interface principale pour l'environnement de conception de circuits, 
gérant l'état de l'éditeur, les interactions utilisateur et le rendu visuel."""

logger: Logger = Logger("EditorView")


class EditorView(arcade.View):
    """Orchestre le flux de travail de l'édition de circuits, y compris les composants UI, 
    la manipulation des portes et les cycles de rendu."""

    def __init__(self, id: Optional[str] = None, level: Optional[Any] = None, level_solution: Optional[any] = None,) -> None:
        """Initialise EditorView avec les éléments d'interface utilisateur et l'état nécessaires.

        Args:
            id: Identifiant unique pour une puce existante à charger dans l'éditeur.
            level: Le conteneur de données de niveau si utilisé en mode éditeur de niveau.
        """
        super().__init__()

        self.follower: Entity = Entity()
        self.follower.height = data.UI_EDITOR_GRID_SIZE
        self.follower.width = data.UI_EDITOR_GRID_SIZE

        self.bottom_zone_collider: Entity = Entity()
        self.bottom_zone_collider.x = 0
        self.bottom_zone_collider.y = 0
        self.bottom_zone_collider.width = data.WINDOW_WIDTH
        self.bottom_zone_collider.height = 3 * 64

        self.selected_follower: Optional[Any] = None
        self.moving_gate: Optional[Any] = None
        self.current_path: Optional[Path] = None
        self.level_editor: bool = False
        self.level_solution: bool = True
        self.engine: Engine = Engine()

        if id is None:
            self.chip = Chip(random_id())
        else:
            if id in data.loaded_chips:
                self.chip = data.loaded_chips[id]
            else:
                self.chip = Chip(random_id())

        if level is not None:
            self.level = level
            self.level_editor = True
            self.chip = level.chip

        if level_solution is not None:
            self.chip = level_solution
            self.level_solution = True

        self.moving_gate_offset: Tuple[int, int] = (0, 0)
        self._real_camera_position: Tuple[int, int] = (0, 0)
        self.camera_position: Tuple[int, int] = (0, 0)
        self.bottom_camera_position: List[int] = [0, 0]
        self.current_bottom_categorie: int = 0
        self.bottom_gates: List[Any] = []
        self.bottom_gates_cache = {}

        for i in range(3):
            self.current_bottom_categorie = i
            self.bottom_gate_bar()

        self.current_bottom_categorie = 0
        self.bottom_gate_bar()

        self.editor_categories: List[Entity] = []
        self.setup_editor_categories()

        self.background_color = arcade.types.Color.from_hex_string("121212")
        self.camera_hold: bool = False
        self.fps: int = 0
        self.delta_time: float = 1.0
        self.frame_count: int = 0
        self.last_time: float = 1.0
        self.stress_test: bool = False

        if self.stress_test:
            self.perf_graph_list = arcade.SpriteList()
            graph = arcade.PerfGraph(400, 400, graph_data="FPS")
            graph.position = 200, 200
            self.perf_graph_list.append(graph)

    def setup_editor_categories(self) -> None:
        """Configure les entités UI représentant les catégories de sélection de portes."""
        self.editor_categories = []

        sprite = data.editor_categories["1_bit"]
        self.editor_categories.append(
            Entity(x=48, y=0, width=100, height=30, sprite=sprite)
        )

        sprite = data.editor_categories["custom"]
        self.editor_categories.append(
            Entity(x=175, y=0, width=125, height=30, sprite=sprite)
        )

        sprite = data.editor_categories["8_bit"]
        self.editor_categories.append(
            Entity(x=325, y=0, width=100, height=30, sprite=sprite)
        )

    def bottom_bar_width_sum(self) -> int:
        """Calcule l'espace horizontal total requis pour toutes les portes de la barre inférieure."""
        result = 0
        for i in self.bottom_gates:
            result += i.tile_width
        return result

    @profile
    def bottom_gate_bar(self) -> None:
        """Actualise le contenu de la barre UI inférieure en fonction de la catégorie active."""
        self.bottom_gates = []

        if self.current_bottom_categorie in self.bottom_gates_cache:
            self.bottom_gates = self.bottom_gates_cache[self.current_bottom_categorie]
            self.bottom_bar_update_camera()
            return

        if self.current_bottom_categorie == 1:
            for chip_id in data.loaded_chips:
                if chip_id != self.chip.id:
                    chip = data.loaded_chips[chip_id]
                    if self.chip.id not in chip.requirements:
                        position = (
                            self.bottom_bar_width_sum() + len(self.bottom_gates)
                        ) * data.UI_EDITOR_GRID_SIZE + 64
                        self.bottom_gates.append(
                            CustomGate(f"bottom_gate_{random_id()}", chip)
                        )
                        self.bottom_gates[-1].camera = (0, 0)
                        self.bottom_gates[-1].y = 3 * data.UI_EDITOR_GRID_SIZE
                        self.bottom_gates[-1].x = position
            self.bottom_gates_cache[1] = self.bottom_gates

        elif self.current_bottom_categorie == 0:
            for i in gate_types_1:
                position = (
                    self.bottom_bar_width_sum() + len(self.bottom_gates)
                ) * data.UI_EDITOR_GRID_SIZE + 64
                self.bottom_gates.append(gate_types[i](f"bottom_gate_{random_id()}"))
                self.bottom_gates[-1].camera = (0, 0)
                self.bottom_gates[-1].y = 3 * data.UI_EDITOR_GRID_SIZE
                self.bottom_gates[-1].x = position
            self.bottom_gates_cache[0] = self.bottom_gates
        elif self.current_bottom_categorie == 2:
            for i in {**gate_types_8, **gate_types_mix}:
                position = (
                    self.bottom_bar_width_sum() + len(self.bottom_gates)
                ) * data.UI_EDITOR_GRID_SIZE + 64
                self.bottom_gates.append(gate_types[i](f"bottom_gate_{random_id()}"))
                self.bottom_gates[-1].camera = (0, 0)
                self.bottom_gates[-1].y = 3 * data.UI_EDITOR_GRID_SIZE
                self.bottom_gates[-1].x = position
            self.bottom_gates_cache[2] = self.bottom_gates

    def bottom_bar_update_camera(self) -> None:
        """Synchronise la position de défilement des portes de la barre inférieure."""
        for gate in self.bottom_gates:
            gate.camera = self.bottom_camera_position

    def get_hovered_bottom_gate(self) -> Tuple[int, Any]:
        """Identifie quelle porte de la barre inférieure est actuellement survolée, le cas échéant.

        Returns:
            Un tuple contenant le flag de catégorie et l'identifiant correspondant.
        """
        for i in self.bottom_gates:
            if i.entity.touched:
                if i.gate_type != "Custom":
                    return 0, i.gate_type
                else:
                    return 1, i.base_chip_id
        return 2, None

    def draw_bottom_gates(self) -> None:
        """Rend le menu de sélection des portes."""
        for i in self.bottom_gates:
            i.draw()

    def draw_tile(self, id: Any, x: float, y: float) -> None:
        """Rend un segment de bordure UI individuel.

        Args:
            id: L'identifiant de la texture de tuile spécifique.
            x: Position horizontale.
            y: Position verticale.
        """
        rect = arcade.XYWH(x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0))
        arcade.draw_texture_rect(data.ui_border_tiles[id], rect)

    def reset(self) -> None:
        """Réinitialise l'état de la vue."""
        pass

    def draw_frame_border(self) -> None:
        """Rend la bordure extérieure de la fenêtre UI et son arrière-plan."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=data.WINDOW_HEIGHT,
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_sprite_rect(data.editor_border, rect)

    def draw_frame_border_no_bg(self) -> None:
        """Rend les éléments de premier plan de la bordure de la fenêtre UI."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=data.WINDOW_HEIGHT,
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_sprite_rect(data.editor_border_no_bg, rect)

    def draw_frame_background(self) -> None:
        """Rend l'arrière-plan de l'espace de travail basé sur une grille."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=(((data.WINDOW_HEIGHT + 32) // 64) * 64),
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_texture_rect(data.background_grid_texture, rect)

    def draw_debug_text(self) -> None:
        """Rend les informations de diagnostic pour le suivi des performances."""
        debug_list = [
            f"Level Editor ? {self.level_editor}",
            f"Camera: {self.camera_position}",
            f"FPS: {self.fps} / {round(self.delta_time*100000)/100} ms / {self.frame_count}",
            f"Objects: {len(self.chip.gates.keys())}g/{len(self.chip.paths.keys())}p",
        ]
        start_y = data.WINDOW_HEIGHT - 70
        for index, item in enumerate(debug_list):
            arcade.draw_text(
                item,
                64,
                start_y - (index * 25),
                arcade.color.WHITE,
                14,
                font_name="Press Start 2P",
            )

    def on_draw(self) -> None:
        """Exécute la séquence principale de rendu de la trame."""
        self.clear()
        self.draw_frame_background()

        for p in self.chip.paths.values():
            p.draw()
        for g in self.chip.gates.values():
            g.draw()

        if self.current_path:
            self.current_path.draw()
        if self.selected_follower:
            self.selected_follower.draw()

        self.draw_debug_text()
        self.draw_frame_border()
        self.draw_bottom_gates()
        self.draw_frame_border_no_bg()

        for i in self.editor_categories:
            i.draw()

        if self.stress_test:
            self.perf_graph_list.draw()

        self.frame_count += 1
        self.delta_time = time.time() - self.last_time
        self.last_time = time.time()

    def on_update(self, delta_time: float) -> None:
        """Exécute la logique de simulation et met à jour les métriques de performance."""
        self.fps = 1 / self.delta_time * 10000 // 10000
        self.simulate()
        if self.stress_test:
            for i in range(10000):
                a = random_id()
                self.chip.gates[a] = And(a)

        if (self.frame_count + 1) % (60 * 60 * 1) == 0:
            logger.info("Auto-Save")
            if self.level_editor:
                self.level.save()
            else:
                self.chip.save()

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les actions déclenchées par le clavier pour le basculement d'entrée, la navigation et l'édition."""
        if key == data.keys.input_toggle:
            for g in self.chip.gates.values():
                if g.entity.touched and g.type == "Input":
                    if g.outputs_sizes[0] == 1:
                        g.switch()
                    elif g.gate_type in ["8Input"]:
                        data.window.display(InputFrame(self.chip,g.id))

        if key == 65473:  # Sortie d'urgence : F4
            arcade.exit()
        if key == data.keys.back:
            if self.current_path:
                self.current_path.abort()
            if self.current_path or self.selected_follower:
                self.current_path = None
                self.selected_follower = None
            else:
                if self.level_solution:
                    data.window.back()
                else:
                    data.window.display(data.pause)
        if key == data.keys.chip_save:
            if self.level_editor:
                data.window.display(SaveFrame(self.level))
            else:
                data.window.display(EditorSaveFrame(self.chip))

        if key == data.keys.gate_delete and self.current_path is None:
            self.delete()

    def delete_gate(self, id: str) -> None:
        """Supprime une porte et retire tous les chemins associés à ses ports.

        Args:
            id: L'identifiant de la porte à supprimer.
        """
        to_delete = []
        for index in self.chip.paths.keys():
            p = self.chip.paths[index]
            for input_node in p.inputs:
                if input_node[1] == id:
                    to_delete.append(p.id)

            for output_node in p.outputs:
                if output_node[1] == id:
                    to_delete.append(p.id)

        del self.chip.gates[id]
        for i in to_delete:
            self.delete_path(i)

    def delete_path(self,path_id):
        """Supprime un chemin spécifique par son identifiant."""
        p = self.chip.paths[path_id]
        for i in self.chip.paths[path_id].outputs:
                    gate_id = i[1]
                    gate_output_id = i[2]    
                    if gate_id in self.chip.gates:
                        self.chip.gates[gate_id].inputs[gate_output_id] = 0
        del self.chip.paths[path_id]

    def delete(self) -> None:
            """Initie le processus de suppression pour l'objet actuellement sélectionné."""
            for g in self.chip.gates.values():
                if g.entity.touched:
                    self.delete_gate(g.id)
                    break

            to_delete = []
            for p in self.chip.paths.values():
                if p.touched:
                    to_delete.append(p.id)

            for p in to_delete:
                self.delete_path(p)

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de relâchement de touche."""
        pass

    @property
    def camera(self) -> Tuple[int, int]:
        """Récupère les coordonnées actuelles de la caméra."""
        return self.camera_position

    @camera.setter
    def camera(self, value: Tuple[int, int]) -> None:
        """Définit la position de la caméra et synchronise toutes les entités sur la grille.

        Args:
            value: Les coordonnées cibles de la caméra pour l'alignement.
        """
        self._real_camera_position = value
        self.camera_position = (
            (self._real_camera_position[0] // data.UI_EDITOR_GRID_SIZE)
            * data.UI_EDITOR_GRID_SIZE,
            (self._real_camera_position[1] // data.UI_EDITOR_GRID_SIZE)
            * data.UI_EDITOR_GRID_SIZE,
        )
        for g in self.chip.gates:
            self.chip.gates[g].camera_moving(self.camera_position)
        for p in self.chip.paths:
            self.chip.paths[p].camera = self.camera_position
        if self.current_path:
            self.current_path.camera = self.camera_position

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Met à jour les traceurs de souris UI et effectue les calculs de déplacement."""
        mouse.position = (x, y)

        self.follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2
        self.follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2

        if self.camera_hold:
            self.camera = (
                self._real_camera_position[0] + delta_x,
                self._real_camera_position[1] + delta_y,
            )

        if self.selected_follower:
            self.selected_follower._camera = (0, 0)
            self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2
            self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2

        if self.moving_gate:
            self.moving_gate.x = mouse.cursor[0] - self.moving_gate_offset[0]
            self.moving_gate.y = mouse.cursor[1] - self.moving_gate_offset[1]

            for path in self.chip.paths.values():
                connected_inputs, connected_outputs = path.get_connected_points(
                    self.moving_gate.id
                )
                modified = False

                for i in connected_inputs:
                    modified = True
                    position = self.moving_gate.outputs_position[i[2]]
                    position = (
                        position[0] - self.camera_position[0],
                        position[1] - self.camera_position[1],
                    )
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = position
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = position

                for i in connected_outputs:
                    modified = True
                    position = self.moving_gate.inputs_position[i[2]]
                    position = (
                        position[0] - self.camera_position[0],
                        position[1] - self.camera_position[1],
                    )
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = position
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = position

                if modified:
                    path.recalculate_hitbox()

    def simulate(self) -> None:
        """Invoque le moteur logique pour propager les valeurs des signaux."""
        self.engine.propagate_values(self.chip)

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Gère le défilement à l'intérieur de la barre UI inférieure."""
        if self.bottom_zone_collider.touched:
            self.bottom_camera_position[0] += scroll_y * -data.MOUSE_SENSI
            self.bottom_camera_position[0] = min(self.bottom_camera_position[0], 0)
            self.bottom_bar_update_camera()

    @profile
    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Gère les événements de clic pour la sélection UI et les interactions avec l'espace de travail."""
        if button == 2:
            self.camera_hold = True
            return
        if self.camera_hold:
            return

        for i in range(len(self.editor_categories)):
            if self.editor_categories[i].touched:
                self.current_bottom_categorie = i
                self.bottom_gate_bar()

        for g in self.chip.gates.values():
            touched = g.touched
            if touched:
                if self.current_path is None:
                    pid = random_id()
                    self.current_path = Path(pid)
                    self.current_path.camera = self.camera
                    self.current_path.add_path()
                    if touched[0] == 1:
                        self.current_path.outputs.append(
                            [
                                1,
                                g.id,
                                touched[1],
                                1,
                                self.current_path.current_branch_count,
                            ]
                        )
                    else:
                        self.current_path.inputs.append(
                            [
                                2,
                                g.id,
                                touched[1],
                                1,
                                self.current_path.current_branch_count,
                            ]
                        )
                    self.current_path.current_size = touched[2]
                    return
                else:
                    if touched[2] == self.current_path.current_size:
                        if touched[0] == 1:
                            self.current_path.outputs.append(
                                [
                                    1,
                                    g.id,
                                    touched[1],
                                    2,
                                    self.current_path.current_branch_count,
                                ]
                            )
                        else:
                            self.current_path.inputs.append(
                                [
                                    2,
                                    g.id,
                                    touched[1],
                                    2,
                                    self.current_path.current_branch_count,
                                ]
                            )
                        self.current_path.camera = self.camera
                        self.current_path.finish()
                        if self.current_path.id not in self.chip.paths:
                            self.chip.paths[self.current_path.id] = self.current_path
                        self.current_path = None
                        return

        if not self.current_path:
            for p in self.chip.paths.values():
                if p.touched:
                    p.add_path()
                    self.current_path = p
                    return
        else:
            for p in self.chip.paths.values():
                if p.touched and p != self.current_path:
                    self.current_path.add_path()
                    p.merge(self.current_path)
                    if self.current_path.id in self.chip.paths:
                        del self.chip.paths[self.current_path.id]
                    self.current_path = None
                    return
            self.current_path.add_path()
            return

        if self.moving_gate is None:
            for g in self.chip.gates.values():
                if g.entity.touched:
                    self.moving_gate_offset = (
                        mouse.cursor[0] - g.x,
                        mouse.cursor[1] - g.y,
                    )
                    self.moving_gate = g
                    self.moving_gate.moving = True
                    return

        if self.selected_follower is None:
            type_val, hovered = self.get_hovered_bottom_gate()
            if type_val == 0:
                if hovered in gate_types:
                    self.selected_follower = gate_types[hovered](random_id())
                    self.selected_follower.camera = self.camera
                    self.selected_follower.moving = True
                    self.selected_follower.x = (
                        mouse.cursor[0]
                        - data.UI_EDITOR_GRID_SIZE / 2
                        - self.camera_position[0]
                    )
                    self.selected_follower.y = (
                        mouse.cursor[1]
                        - data.UI_EDITOR_GRID_SIZE / 2
                        - self.camera_position[1]
                    )
            elif type_val == 1:
                if hovered in data.loaded_chips:
                    self.selected_follower = CustomGate(
                        random_id(), data.loaded_chips[hovered]
                    )
                    self.selected_follower.camera = self.camera
                    self.selected_follower.moving = True
                    self.selected_follower.x = (
                        mouse.cursor[0]
                        - data.UI_EDITOR_GRID_SIZE / 2
                        - self.camera_position[0]
                    )
                    self.selected_follower.y = (
                        mouse.cursor[1]
                        - data.UI_EDITOR_GRID_SIZE / 2
                        - self.camera_position[1]
                    )

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Finalise les opérations de glisser-déposer pour les portes et le mouvement de caméra."""
        if button == 2:
            self.camera_hold = False
            for g in self.chip.gates:
                self.chip.gates[g].camera = self.camera_position
        else:
            if self.selected_follower is not None:
                if self.bottom_zone_collider.touched:
                    self.selected_follower = None
                else:
                    self.chip.gates[self.selected_follower.id] = self.selected_follower
                    self.selected_follower.camera = self.camera
                    self.selected_follower.x = (
                        mouse.cursor[0]
                        - data.UI_EDITOR_GRID_SIZE / 2
                        - self.camera_position[0]
                    )
                    self.selected_follower.y = (
                        mouse.cursor[1]
                        - data.UI_EDITOR_GRID_SIZE / 2
                        - self.camera_position[1]
                    )
                    self.selected_follower.moving = False
                    self.selected_follower = None

        if self.moving_gate:
            self.moving_gate.moving = False
        self.moving_gate = None
        self.moving_gate_offset = (0, 0)