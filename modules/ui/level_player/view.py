import arcade
import time
from typing import Optional, List, Tuple, Any, Dict

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.id_generator import random_id
from modules.ui.toolbox.easing import BackEaseOut, ElasticEaseOut
from modules.ui.toolbox.text import Text
from modules.ui.editor.view import EditorView
from modules.ui.editor.input import InputFrame

from modules.data.nodes.path import Path

from modules.data.custom import CustomGate

from modules.data import data
from modules.data.gate_index import gate_types

from modules.logger import Logger

from modules.engine import Engine

logger: Logger = Logger("LevelPlayer")


class LevelPlayer(arcade.View):
    """Gère la vue interactive du niveau de jeu, incluant le rendu de l'interface utilisateur,
    l'édition pilotée par l'utilisateur et la simulation des portes logiques.
    """

    def __init__(self, id: Optional[str] = None) -> None:
        """Initialise la vue LevelPlayer et charge la configuration du niveau.

        Args:
            id: Identifiant du niveau.
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

        if id is None:
            logger.error("Aucun identifiant de niveau fourni, retour en arrière.")
            data.window.back()
            arcade.quit()
        else:
            if id in data.loaded_levels:
                self.level = data.loaded_levels[id]
                self.level.play_mode()
            else:
                logger.error("Identifiant de niveau invalide, retour en arrière.")
                data.window.back()
                arcade.quit()

        self.moving_gate_offset: Tuple[int, int] = (0, 0)
        self._real_camera_position: Tuple[int, int] = (0, 0)
        self.camera_position: Tuple[int, int] = (0, 0)
        self.bottom_camera_position: List[int] = [0, 0]

        self.bottom_gates: List[Any] = []
        self.bottom_gate_bar()

        self.background_color = arcade.types.Color.from_hex_string("121212")

        self.camera_hold: bool = False
        self.fps: float = 0
        self.delta_time: float = 1
        self.frame_count: int = 0
        self.last_time: float = 1

        self.engine: Engine = Engine()
        self.stress_test: bool = False

        self.display_hint_frame: bool = True
        self.current_hint_frame: int = 0

        if self.stress_test:
            self.perf_graph_list = arcade.SpriteList()
            graph = arcade.PerfGraph(400, 400, graph_data="FPS")
            graph.position = 200, 200
            self.perf_graph_list.append(graph)

        self.prepare_right_frame()
        self.prepare_won_frame()
        self.prepare_hint_frame()

    def reload_hint(self):
        self.hint_frame_text.text = self.level.hints[self.current_hint_frame]

    def prepare_hint_frame(self) -> None:
        """Initialise les éléments de l'interface pour l'écran d'indices. (Instructions du niveau.)"""

        self.hint_frame = Entity(
            x=384, y=220, width=576 * 2, height=320 * 2, sprite=data.level_player_empty
        )
        self.hint_frame_text = Text(
            x=data.WINDOW_WIDTH / 2,
            y=data.WINDOW_HEIGHT / 2,
            width=1000,
            height=300,
            text="",
            multiline=True,
        )
        self.hint_frame_ok = Entity(
            x=384 + 576 * 2 - 137 * 1.2 - 90,
            y=310,
            width=137 * 1.2,
            height=120,
            sprite=data.button_ok,
        )
        self.hint_frame_next = Entity(
            x=384 + 576 * 2 - 169 * 1.2 - 90,
            y=310,
            width=169 * 1.2,
            height=120,
            sprite=data.button_next_on,
        )
        self.hint_frame_back = Entity(
            x=384 + 90, y=310, width=160 * 1.2, height=120, sprite=data.button_back
        )

        if (len(self.level.hints) - 1) < 1:
            self.display_hint_frame = False
            return

        self.hint_frame_text.text = self.level.hints[0]

    def prepare_won_frame(self) -> None:
        """Initialise les éléments de l'interface pour l'écran de victoire."""
        self.win_frame_ease = BackEaseOut(-500, 220, 90)
        self.win_frame = Entity(
            x=384, y=-500, width=576 * 2, height=320 * 2, sprite=data.level_player_win
        )

        self.win_text_level_num = arcade.Text(
            f"Niveau {self.level.number}",
            512,
            580,
            arcade.color.WHITE,
            20,
            font_name="Press Start 2P",
        )
        self.win_text_level_name = arcade.Text(
            f"{self.level.name}",
            512,
            540,
            arcade.color.WHITE,
            20,
            font_name="Press Start 2P",
        )

        self.win_button_next = Entity(
            x=990, y=348, width=432, height=256, sprite=data.button_next_on
        )

        self.win_stars: List[Entity] = []
        self.win_stars_ease: List[ElasticEaseOut] = []

        for i in range(3):
            sprite = data.star
            if i > self.level.get_stars_count() - 1:
                sprite = data.star_empty
            self.win_stars.append(
                Entity(
                    x=535 + i * 135 + 54,
                    y=410 + 54,
                    width=108,
                    height=108,
                    sprite=sprite,
                    anchor=arcade.Vec2(0.5, 0.5),
                )
            )
            self.win_stars_ease.append(
                ElasticEaseOut(-20 + i * -20, end=108, duration=128 + i * 20)
            )

    def prepare_right_frame_basic(self) -> None:
        """Construit l'interface de la barre latérale droite, incluant le rendu de la table de vérité."""
        self.check_button = Entity(
            x=1402, y=57, width=216, height=128, sprite=data.button_check
        )
        self.truth_table = Entity(
            x=1402,
            y=data.WINDOW_HEIGHT - 383,
            width=448,
            height=64,
            sprite=data.truth_table,
        )
        self.button_answer = Entity(
            x=1634, y=57, width=216, height=128, sprite=data.button_answer
        )
        self.level_info = Entity(
            x=1402,
            y=data.WINDOW_HEIGHT - 127,
            width=448,
            height=64,
            sprite=data.level_info,
        )

        self.level_name_text = arcade.Text(
            f"Niveau {self.level.number} : {self.level.name}",
            1408,
            900,
            arcade.color.WHITE,
            12,
            font_name="Press Start 2P",
        )

        self.level_desc_text: List[arcade.Text] = []
        texts: List[str] = self.level.description.split(" ")
        c: int = 0

        # Effectue un retour à la ligne automatique (word wrap) glouton basique
        for _ in range(len(texts)):
            if c > len(texts) - 2:
                break
            if len(texts[c] + texts[c + 1]) + 1 <= 24:
                b = texts.pop(c + 1)
                texts[c] += " " + b
            else:
                c += 1

        for i in range(len(texts)):
            self.level_desc_text.append(
                arcade.Text(
                    texts[i],
                    1408,
                    850 - 25 * i,
                    arcade.color.WHITE,
                    10,
                    font_name="Press Start 2P",
                )
            )

    def prepare_right_frame(self) -> None:
        self.prepare_right_frame_basic()
        if self.level.is_complex:
            self.prepare_right_frame_complex()
        else:
            self.prepare_right_frame_simple()

    def prepare_right_frame_complex(self) -> None:
        self.truth_inputs = arcade.Text(
            "Entrée(s)",
            1626,
            data.WINDOW_HEIGHT - (447),
            arcade.color.WHITE,
            18,
            font_name="Press Start 2P",
            anchor_x="center",
        )
        result = ""

        for i in self.level.compare_fail["in"]:
            result += f"{i} "

        self.truth_inputs_values = arcade.Text(
            result,
            1626,
            data.WINDOW_HEIGHT - (497),
            arcade.color.WHITE,
            16,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        self.truth_targets = arcade.Text(
            "Cible(s)",
            1626,
            data.WINDOW_HEIGHT - (547),
            arcade.color.WHITE,
            18,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        result = ""

        for i in self.level.compare_fail["target"]:
            result += f"{i} "

        self.truth_targets_values = arcade.Text(
            result,
            1626,
            data.WINDOW_HEIGHT - (597),
            arcade.color.WHITE,
            16,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        self.truth_outputs = arcade.Text(
            "Sortie(s)",
            1626,
            data.WINDOW_HEIGHT - (647),
            arcade.color.WHITE,
            18,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        result = ""

        for i in self.level.compare_fail["out"]:
            result += f"{i} "

        self.truth_outputs_values = arcade.Text(
            result,
            1626,
            data.WINDOW_HEIGHT - (697),
            arcade.color.WHITE,
            16,
            font_name="Press Start 2P",
            anchor_x="center",
        )

    def prepare_right_frame_simple(self) -> None:

        table = self.level.truth[self.level.answer.id]
        chip_truth: Optional[Dict] = None

        if self.level.chip.id in self.level.truth:
            chip_truth = self.level.truth[self.level.chip.id]

        self.truth_table_inputs: List[List[arcade.Text]] = [
            [] for _ in range(len(table["meta"]["inputs"]))
        ]
        self.truth_table_outputs: List[List[arcade.Text]] = [
            [] for _ in range(len(table["meta"]["outputs"]))
        ]
        self.line_set: List[List[Tuple[Tuple[float, float], Tuple[float, float]]]] = []
        self.truth_table_titles: List[arcade.Text] = []

        add_y = 28
        add_x = 27
        total_len = (len(table["data"][0]) * 2 + table["meta"]["size"] + 4) * add_x
        start_x = (
            1402
            + (7 * 32)
            - ((len(table["data"][0]) * 2 + table["meta"]["size"] + 4) / 2 * add_x)
        )
        start_y = data.WINDOW_HEIGHT - (447)

        offset_x = 0
        offset_y = 0

        self.line_set.append(
            [
                (start_x - 10, start_y - offset_y + add_y - 4),
                (start_x + total_len + 10, start_y + add_y - offset_y - 4),
            ]
        )
        self.truth_table_titles.append(
            arcade.Text(
                "Entrées",
                start_x + (table["meta"]["size"] / 2) * add_x,
                start_y + add_y + 5,
                arcade.color.WHITE,
                10,
                font_name="Press Start 2P",
                anchor_x="center",
            )
        )
        self.truth_table_titles.append(
            arcade.Text(
                "Cible",
                start_x
                + (table["meta"]["size"] + 2 + len(table["data"][0]) / 2) * add_x
                - 5,
                start_y + add_y + 5,
                arcade.color.WHITE,
                9,
                font_name="Press Start 2P",
                anchor_x="center",
            )
        )
        self.truth_table_titles.append(
            arcade.Text(
                "Actuel",
                start_x
                + (table["meta"]["size"] + 4 + len(table["data"][0]) * 1.5) * add_x,
                start_y + add_y + 5,
                arcade.color.WHITE,
                9,
                font_name="Press Start 2P",
                anchor_x="center",
            )
        )

        if not table["meta"]["complex"]:
            for current in range(table["meta"]["power"]):
                values = [
                    bool(current & (1 << i)) for i in range(table["meta"]["size"])
                ]
                for i in range(len(values)):
                    self.truth_table_inputs[i].append(
                        arcade.Text(
                            str(values[i] * 1),
                            start_x + offset_x,
                            start_y - offset_y,
                            arcade.color.WHITE,
                            14,
                            font_name="Press Start 2P",
                            anchor_x="center",
                        )
                    )
                    offset_x += add_x
                offset_x += add_x * 2
                for i in range(len(table["data"][current])):
                    self.truth_table_outputs[i].append(
                        arcade.Text(
                            str(table["data"][current][i] * 1),
                            start_x + offset_x,
                            start_y - offset_y,
                            arcade.color.WHITE,
                            14,
                            font_name="Press Start 2P",
                            anchor_x="center",
                        )
                    )
                    offset_x += add_x
                offset_x += add_x * 2
                if chip_truth:
                    for i in range(len(chip_truth["data"][current])):
                        color = arcade.color.RED_PURPLE
                        if table["data"][current][i] == chip_truth["data"][current][i]:
                            color = arcade.color.GREEN_YELLOW
                        self.truth_table_outputs[i].append(
                            arcade.Text(
                                str(chip_truth["data"][current][i] * 1),
                                start_x + offset_x,
                                start_y - offset_y,
                                color,
                                14,
                                font_name="Press Start 2P",
                                anchor_x="center",
                            )
                        )
                        offset_x += add_x
                else:
                    for i in range(len(table["data"][current])):
                        self.truth_table_outputs[i].append(
                            arcade.Text(
                                "?",
                                start_x + offset_x,
                                start_y - offset_y,
                                arcade.color.WHITE,
                                14,
                                font_name="Press Start 2P",
                                anchor_x="center",
                            )
                        )
                        offset_x += add_x
                self.line_set.append(
                    [
                        (start_x - 10, start_y - offset_y - 4),
                        (start_x + offset_x + 10, start_y - offset_y - 4),
                    ]
                )
                offset_x = 0
                offset_y += add_y

    def bottom_bar_width_sum(self) -> int:
        """Retourne la largeur cumulée de toutes les icônes de portes dans la barre d'outils inférieure."""
        result: int = 0
        for i in self.bottom_gates:
            result += i.tile_width
        return result

    def bottom_gate_bar(self) -> None:
        """Remplit la barre d'outils inférieure avec les portes disponibles selon les contraintes du niveau."""
        self.bottom_gates = []
        for i in self.level.max_usage:
            if i != "Input" and i != "Output":
                if i in gate_types:
                    position = (
                        self.bottom_bar_width_sum() + len(self.bottom_gates)
                    ) * data.UI_EDITOR_GRID_SIZE + 64
                    self.bottom_gates.append(
                        gate_types[i](f"bottom_gate_{random_id()}")
                    )
                    self.bottom_gates[-1].camera = self.bottom_camera_position
                    self.bottom_gates[-1].y = 3 * data.UI_EDITOR_GRID_SIZE
                    self.bottom_gates[-1].x = position
                elif i in data.loaded_chips:
                    chip = data.loaded_chips[i]
                    position = (
                        self.bottom_bar_width_sum() + len(self.bottom_gates)
                    ) * data.UI_EDITOR_GRID_SIZE + 64
                    self.bottom_gates.append(
                        CustomGate(f"bottom_gate_{random_id()}", chip)
                    )
                    self.bottom_gates[-1].camera = self.bottom_camera_position
                    self.bottom_gates[-1].y = 3 * data.UI_EDITOR_GRID_SIZE
                    self.bottom_gates[-1].x = position

    def get_hovered_bottom_gate(self) -> Optional[str]:
        """Identifie quelle icône de porte dans la barre d'outils est actuellement survolée."""
        for i in self.bottom_gates:
            if i.entity.touched:
                if i.type == "Custom":
                    return i.base_chip_id
                return i.gate_type
        return None

    def draw_bottom_gates(self) -> None:
        """Affiche les icônes de portes dans la barre d'outils inférieure."""
        for i in self.bottom_gates:
            i.draw()

    def reset(self) -> None:
        """Réinitialise l'état actuel du niveau."""
        pass

    def draw_frame_border(self) -> None:
        """Affiche la bordure extérieure de la fenêtre de l'interface."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=data.WINDOW_HEIGHT,
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_sprite_rect(data.level_player_border, rect)

    def draw_frame_border_top(self) -> None:
        """Affiche le haut de la bordure (deuxième couche pour éviter les superpositions)."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=data.WINDOW_HEIGHT,
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_sprite_rect(data.level_player_border_no_bg, rect)

    def draw_frame_background(self) -> None:
        """Affiche la texture d'arrière-plan de la grille du niveau."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=(((data.WINDOW_HEIGHT + 32) // 64) * 64),
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_texture_rect(data.background_grid_texture, rect)

    def draw_debug_text(self) -> None:
        """Affiche les métriques de performance du moteur et le décompte des objets."""
        debug_list = [
            f"Caméra: {self.camera_position}",
            f"FPS: {self.fps} / {round(self.delta_time * 100000) / 100} ms / {self.frame_count}",
            f"Objets: {len(self.level.chip.gates.keys())}g/{len(self.level.chip.paths.keys())}p",
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

    def draw_level_time(self) -> None:
        """Affiche le temps écoulé par rapport aux limites et les indicateurs de progression."""
        debug_list = [
            f"Temps Limite: {round(time.time() - self.level.start_time)}s / {self.level.time}s",
            f"Étoiles: {self.level.get_stars_count()}",
        ]
        start_y = data.WINDOW_HEIGHT - 80
        for index, item in enumerate(debug_list):
            arcade.draw_text(
                item,
                64,
                start_y - (index * 25),
                arcade.color.WHITE,
                14,
                font_name="Press Start 2P",
            )
        arcade.draw_sprite_rect(
            data.star, arcade.rect.XYWH(64 + 8 * 20 + 7, 986, 25, 25)
        )

    def draw_won(self) -> None:
        """Affiche la fenêtre modale de victoire et les icônes d'étoiles animées."""
        if not self.win_frame_ease.done:
            value = self.win_frame_ease.tick()
            self.win_frame.y = value
        self.win_frame.draw()
        if self.win_frame_ease.done:
            self.win_text_level_num.draw()
            self.win_text_level_name.draw()
            for i in range(len(self.win_stars)):
                value = self.win_stars_ease[i].tick()
                star = self.win_stars[i]
                star._width = value
                star.height = value
                star.draw()
            self.win_button_next.draw()

    def draw_right(self) -> None:
        """Affiche les composants de la barre latérale et la table de vérité calculée."""
        self.check_button.draw()
        self.truth_table.draw()
        self.button_answer.draw()
        self.level_info.draw()
        self.level_name_text.draw()
        for i in self.level_desc_text:
            i.draw()

        if not self.level.is_complex:
            for i in self.truth_table_inputs:
                for a in i:
                    a.draw()
            for i in self.truth_table_outputs:
                for a in i:
                    a.draw()
            for coords in self.line_set:
                arcade.draw_line(
                    coords[0][0],
                    coords[0][1],
                    coords[1][0],
                    coords[1][1],
                    arcade.color.WHITE,
                    1,
                )
            for i in self.truth_table_titles:
                i.draw()
        else:
            self.truth_inputs.draw()
            self.truth_outputs.draw()
            self.truth_targets.draw()
            self.truth_inputs_values.draw()
            self.truth_targets_values.draw()
            self.truth_outputs_values.draw()

    def draw_hint(self) -> None:
        """Affiche le cadre d'indices pour fournir les instructions de base du niveau."""

        if self.display_hint_frame:
            self.hint_frame.draw()
            self.hint_frame_text.draw()

            if self.current_hint_frame == (len(self.level.hints) - 1):
                self.hint_frame_ok.draw()
            if self.current_hint_frame < (len(self.level.hints) - 1):
                self.hint_frame_next.draw()
            if self.current_hint_frame > 0:
                self.hint_frame_back.draw()

    def on_draw(self) -> None:
        """Boucle de rendu principale : met à jour les états visuels et dessine les couches."""
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

        self.draw_frame_border()
        self.draw_bottom_gates()
        self.draw_frame_border_top()
        self.draw_right()
        self.draw_level_time()
        self.draw_hint()

        if self.level.won:
            self.draw_won()
        if self.stress_test:
            self.perf_graph_list.draw()

        self.frame_count += 1
        self.delta_time = time.time() - self.last_time
        self.last_time = time.time()

    def on_update(self, delta_time: float) -> None:
        """Boucle de mise à jour par image pour la simulation et le suivi d'état."""
        self.fps = 1 / self.delta_time * 10000 // 10000
        self.simulate()

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les raccourcis clavier pour l'interaction, la suppression et la navigation."""
        if key == data.keys.input_toggle and not self.level.won:
            for g in self.level.chip.gates.values():
                if g.entity.touched and g.type == "Input":
                    if g.outputs_sizes[0] == 1:
                        g.switch()
                    elif g.gate_type in ["8Input"]:
                        data.window.display(InputFrame(self.level.chip,g.id))
        if key == 65473:  # Sortie d'urgence : F4
            arcade.exit()

        if key == data.keys.back:
            if self.current_path or self.selected_follower:
                if self.current_path:
                    self.current_path.abort()
                self.current_path = None
                self.selected_follower = None
            else:
                data.window.display(data.pause)

        if (
            key == data.keys.gate_delete
            and not self.level.won
            and self.current_path is None
        ):
            self.delete()

    def delete_gate(self, id: str) -> None:
        """Supprime la porte spécifiée et réconcilie les chemins de circuit affectés."""
        to_delete: List[str] = []
        if self.level.chip.gates[id].type in ["Gate", "Custom", "Complex"]:
            for index in self.level.chip.paths.keys():
                p = self.level.chip.paths[index]
                for input in p.inputs:
                    if input[1] == id:
                        to_delete.append(index)
   
                for output in p.outputs:
                    if output[1] == id:
                        to_delete.append(index)

            del self.level.chip.gates[id]
            for i in to_delete:
                self.delete_path(i)
            self.level.chip.changed = True

    def delete_path(self,path_id):

        p = self.level.chip.paths[path_id]
        for i in self.level.chip.paths[path_id].outputs:
                    gate_id = i[1]
                    gate_output_id = i[2]    
                    if gate_id in self.level.chip.gates:
                        self.level.chip.gates[gate_id].inputs[gate_output_id] = 0
        del self.level.chip.paths[path_id]

    def delete(self) -> None:
        """Initie le processus de suppression pour l'objet actuellement sélectionné."""
        for g in self.level.chip.gates.values():
            if g.entity.touched:
                self.delete_gate(g.id)
                break

        to_delete = []
        for p in self.level.chip.paths.values():
            if p.touched:
                to_delete.append(p.id)

        for p in to_delete:
            self.delete_path(p)

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de relâchement de touche."""
        pass

    @property
    def camera(self) -> Tuple[int, int]:
        """Fournit la position actuelle de la caméra quantifiée."""
        return self.camera_position

    @camera.setter
    def camera(self, value: Tuple[int, int]) -> None:
        """Met à jour la position de la caméra et recalibre les décalages d'objets."""
        self._real_camera_position = value
        self.camera_position = (
            (self._real_camera_position[0] // data.UI_EDITOR_GRID_SIZE)
            * data.UI_EDITOR_GRID_SIZE,
            (self._real_camera_position[1] // data.UI_EDITOR_GRID_SIZE)
            * data.UI_EDITOR_GRID_SIZE,
        )
        for g in self.level.chip.gates:
            self.level.chip.gates[g].camera_moving(self.camera_position)
        for p in self.level.chip.paths:
            self.level.chip.paths[p].camera = self.camera_position
        if self.current_path:
            self.current_path.camera = self.camera_position

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int) -> None:
        """Gère le mouvement de la souris pour le glisser-déposer d'objets et la mise à jour du circuit."""
        mouse.position = (x, y)
        if self.level.won:
            return
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
            # Recalcule la géométrie des câbles en fonction du mouvement de la porte
            for path in self.level.chip.paths.values():
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
                    self.level.chip.changed = True
                    path.recalculate_hitbox()

    def simulate(self) -> None:
        """Propage les états logiques à travers la puce du circuit actuel."""
        self.engine.propagate_values(self.level.chip)
        if self.level.chip.changed:
            self.level.chip.changed = False
            self.level.calculate_inventory()
            self.bottom_gate_bar()

    def won(self) -> None:
        """Active l'interface utilisateur et les états logiques liés à la victoire."""
        self.prepare_won_frame()

    def launch_next_level(self) -> None:
        """Transitionne l'application vers le niveau suivant dans la séquence."""
        levels: List[str] = list(data.loaded_levels.keys())

        def sort_keys(i: str) -> int:
            return data.loaded_levels[i].number

        levels.sort(key=sort_keys)
        current = levels.index(self.level.id)
        if (current + 1) < len(levels):
            data.window.display(LevelPlayer(levels[current + 1]))

    def next_hint(self):
        if self.current_hint_frame < (len(self.level.hints) - 1):
            self.current_hint_frame += 1
        else:
            self.display_hint_frame = False
        self.reload_hint()

    def previous_hint(self):
        if self.current_hint_frame > 0:
            self.current_hint_frame = 0
        self.reload_hint()