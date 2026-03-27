import json
import os
import time
from typing import List, Dict, Any, Optional, Union
import random

from modules.data.chip import Chip
from modules.ui.toolbox.id_generator import random_id
from modules.data import data
from modules.logger import Logger
from modules.engine import Engine

logger: Logger = Logger("Level")


class Level:
    """Gère la logique des niveaux du jeu, incluant l'état de la puce, les objectifs et la progression.

    Attributs :
        chip (Chip) : La puce logique associée à ce niveau.
        engine (Engine) : Le moteur de simulation utilisé pour évaluer la logique du circuit.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """Initialise l'instance de Level.

        Args :
            id : L'identifiant utilisé pour configurer la puce de base.
        """
        self.chip: Chip = Chip(id)
        self.number: int = 0
        self.time: int = 300
        self.id: str = f"level_{id}"
        self.name: str = "Niveau par défaut"
        self.description: str = "Niveau de base pour apprendre les fondements des portes logiques."

        self.start_text: List[str] = []
        self.hints: List[str] = []
        self.truth: Dict[str, Any] = {}
        self.start: int = 1
        self.play: bool = False
        self.answer: Optional[Chip] = None

        self.max_usage: Dict[str, int] = {}
        self.inventory: Dict[str, int] = {}
        self.won: bool = False
        self.start_time: float = 0.0
        self.stars: int = 0
        self.shown_hints: bool = False
        self.shown_solution: bool = False
        self.color: int = 0
        self.category: int = 0
        self.is_custom: bool = False
        self.is_complex: bool = False
        self.truth_test_values: List[List[int]] = []
        self.compare_fail = {}
        self.prepared_tt = []
        self.is_prepared_tt = False
        self.engine: Engine = Engine()

    def play_mode(self) -> None:
        """Prépare le niveau pour le jeu en réinitialisant l'état et en définissant la logique cible."""
        if self.play:
            self.play = True
            self.chip = self.answer.copy()
            self.chip.id = random_id()
        else:
            self.play = True
            self.answer = self.chip
            self.chip = self.answer.copy()
            self.chip.id = random_id()

        self.won = False
        self.start_time = time.time()
        self.stars = 3
        self.shown_hints = False
        self.shown_solution = False
        self.chip.paths = {}
        self.is_complex = False

        left: List[str] = self.get_gates(self.chip)

        keys_to_delete: List[str] = [i for i in self.chip.gates.keys() if i in left]
        for key in keys_to_delete:
            del self.chip.gates[key]

        self.calculate_inventory()
        self.setup_random_test_values()
        self.get_truth_table(answer=True)

    def setup_random_test_values(self):
        """Configure des valeurs de test aléatoires pour la validation."""
        inputs: List[str] = self.get_inputs(self.answer)
        self.truth_test_values = []

        self.compare_fail = {"in": [], "out": [], "target": []}

        for _ in range(255):
            values = []
            for i in inputs:
                if self.answer.gates[i].gate_type in ["ON", "8ONE"]:
                    values.append(1)
                elif self.answer.gates[i].gate_type in ["OFF"]:
                    values.append(0)
                else:
                    values.append(
                        random.randint(
                            0, 2 ** self.answer.gates[i].outputs_sizes[0] - 1
                        )
                    )
            self.truth_test_values.append(values)

    def get_stars_count(self) -> int:
        """Calcule le nombre d'étoiles actuel basé sur le temps et l'utilisation d'indices.

        Retourne :
            Le nombre d'étoiles obtenues, allant de 0 à 3.
        """
        self.stars = 3

        if round(time.time() - self.start_time) > self.time:
            self.stars -= 1

        if self.shown_hints or self.shown_solution:
            self.stars -= 1

        return self.stars

    def calculate_inventory(self) -> None:
        """Calcule les besoins d'utilisation des portes et l'utilisation actuelle du joueur."""
        self.max_usage = {}
        for i in self.answer.gates:
            if self.answer.gates[i].type == "Custom":
                key = self.answer.gates[i].base_chip_id
                self.max_usage[key] = self.max_usage.get(key, 0) + 1
            else:
                key = self.answer.gates[i].gate_type
                self.max_usage[key] = self.max_usage.get(key, 0) + 1

            if self.answer.gates[i].type == "Complex":
                self.is_complex = True

        self.inventory = {}
        for i in self.chip.gates:
            if self.chip.gates[i].type == "Custom":
                key = self.chip.gates[i].base_chip_id
                self.inventory[key] = self.inventory.get(key, 0) + 1
            else:
                key = self.chip.gates[i].gate_type
                self.inventory[key] = self.inventory.get(key, 0) + 1

    def start_chip(self, chip: Optional[Chip] = None) -> None:
        """Réinitialise les états d'E/S des portes au sein de la puce spécifiée.

        Args :
            chip : La puce à initialiser ; utilise la puce actuelle par défaut si None.
        """
        if chip is None:
            chip = self.chip

        if self.start == 1:
            for i in chip.gates:
                chip.gates[i].inputs = [0 for _ in chip.gates[i].inputs]
                chip.gates[i].outputs = [0 for _ in chip.gates[i].outputs]
        elif self.start == 2:
            for i in chip.gates:
                chip.gates[i].inputs = [1 for _ in chip.gates[i].inputs]
                chip.gates[i].outputs = [1 for _ in chip.gates[i].outputs]

    def get_inputs(self, chip: Optional[Chip] = None) -> List[str]:
        """Identifie tous les identifiants des portes d'entrée.

        Args :
            chip : La puce à inspecter.

        Retourne :
            Une liste d'identifiants de portes agissant comme entrées.
        """
        if chip is None:
            chip = self.chip
        return [i for i in self.chip.gates if self.chip.gates[i].type == "Input"]

    def get_outputs(self, chip: Optional[Chip] = None) -> List[str]:
        """Identifie tous les identifiants des portes de sortie.

        Args :
            chip : La puce à inspecter.

        Retourne :
            Une liste d'identifiants de portes agissant comme sorties.
        """
        if chip is None:
            chip = self.chip
        return [i for i in self.chip.gates if self.chip.gates[i].type == "Output"]

    def get_gates(self, chip: Optional[Chip] = None) -> List[str]:
        """Identifie tous les identifiants des portes logiques fonctionnelles.

        Args :
            chip : La puce à inspecter.

        Retourne :
            Une liste d'identifiants de portes pour les portes standards ou personnalisées.
        """
        if chip is None:
            chip = self.chip
        return [
            i
            for i in self.chip.gates
            if self.chip.gates[i].type in ["Gate", "Custom", "Complex"]
        ]

    def compare_truth_tables(self) -> bool:
        """Valide la puce actuelle par rapport à la table de vérité de la solution attendue.

        Retourne :
            True si les tables de vérité correspondent, False sinon.
        """
        if self.answer is None:
            return False
        if self.answer.id not in self.truth or self.chip.id not in self.truth:
            return False

        for i in self.truth[self.answer.id]["data"]:
            if (
                self.truth[self.answer.id]["data"][i]
                != self.truth[self.chip.id]["data"][i]
            ):
                if self.is_complex:
                    self.compare_fail = {
                        "in": self.truth[self.answer.id]["meta"]["values"][i],
                        "out": self.truth[self.chip.id]["data"][i],
                        "target": self.truth[self.answer.id]["data"][i],
                    }
                return False
        return True

    def check_victory(self) -> bool:
        """Détermine si les objectifs du niveau ont été atteints.

        Retourne :
            L'état de victoire actuel.
        """
        self.won = self.compare_truth_tables()
        return self.won

    def get_single_truth_table_complex(self, chip: Chip) -> None:
        """Génère une table de vérité pour la puce complexe fournie.

        Args :
            chip : L'instance à évaluer.
        """
        copy: Chip = chip.copy()
        self.start_chip(copy)
        self.engine.propagate_values(copy)

        inputs: List[str] = self.get_inputs(copy)
        outputs: List[str] = self.get_outputs(copy)
        size: int = len(inputs)

        self.truth[chip.id]["meta"].update(
            {
                "size": size,
                "inputs": inputs,
                "outputs": outputs,
                "values": self.truth_test_values,
                "complex": True,
            }
        )
        count = 0
        for current in self.truth_test_values:
            for index in range(len(inputs)):
                copy.gates[inputs[index]].outputs[0] = current[index]

            self.engine.propagate_values(copy)

            result = [copy.gates[i].inputs[0] for i in outputs]
            self.truth[chip.id]["data"][count] = result
            count += 1

    def get_single_truth_table_simple(self, chip: Chip) -> None:
        """Génère une table de vérité pour la puce simple fournie.

        Args :
            chip : L'instance à évaluer.
        """
        copy: Chip = chip.copy()
        self.start_chip(copy)
        self.engine.propagate_values(copy)

        inputs: List[str] = self.get_inputs(copy)
        outputs: List[str] = self.get_outputs(copy)
        size: int = len(inputs)

        self.truth[chip.id]["meta"].update(
            {
                "size": size,
                "inputs": inputs,
                "outputs": outputs,
                "power": 2**size,
                "complex": False,
            }
        )

        power: int = 2**size
        for current in range(power):
            # Génère les combinaisons d'états binaires pour les lignes de la table de vérité
            values = [bool(current & (1 << i)) for i in range(size)]
            for index in range(len(inputs)):
                copy.gates[inputs[index]].outputs[0] = values[index]

            self.engine.propagate_values(copy)

            result = [copy.gates[i].inputs[0] for i in outputs]
            # Mappe le tableau de bits vers un index entier pour le dictionnaire de résultats
            int_value = sum(b << i for i, b in enumerate(reversed(values)))
            self.truth[chip.id]["data"][int_value] = result

    def get_truth_table(self, answer: bool = False) -> None:
        """Initialise le stockage de la table de vérité et déclenche la génération.

        Args :
            answer : Si True, évalue la puce solution ; sinon, la puce du joueur.
        """
        used: Chip = self.answer if answer else self.chip
        self.truth[used.id] = {"meta": {}, "data": {}}
        if self.is_complex:
            self.get_single_truth_table_complex(used)
        else:
            self.get_single_truth_table_simple(used)

    def save(self) -> None:
        """Sérialise le niveau actuel et la configuration de la puce dans un fichier."""
        chip_save = self.chip.save(no_file=True)
        requirements: List[Dict[str, Any]] = []
        for i in chip_save["requirements"]:
            requirements.append(data.loaded_chips[i].save(no_file=True))

        result: Dict[str, Any] = {
            "chip": chip_save,
            "requirements": requirements,
            "level": {
                "time": self.time,
                "id": self.id,
                "number": self.number,
                "name": self.name,
                "description": self.description,
                "hints": self.hints,
                "version": data.VERSION,
                "start": self.start,
                "truth": self.truth,
                "color": self.color,
                "category": self.category,
                "is_custom": self.is_custom,
            },
        }

        dump: str = json.dumps(result, indent=1)
        path: str = data.current_path
        save_dir: str = os.path.join(path, "levels")
        os.makedirs(save_dir, exist_ok=True)

        file_path: str = os.path.join(save_dir, f"{self.id}.level")
        with open(file_path, "wb") as file:
            file.write(dump.encode())

        logger.success(f"Niveau sauvegardé : {self.id}")

    def load(self, data: Dict[str, Any]) -> None:
        """Hydrate l'état du niveau à partir d'un dictionnaire de configuration.

        Args :
            data : Le dictionnaire source contenant les paramètres du niveau.
        """
        self.time = data["level"]["time"]
        self.id = data["level"]["id"]
        self.number = data["level"]["number"]
        self.description = data["level"]["description"]
        self.hints = data["level"]["hints"]
        self.name = data["level"]["name"]
        self.start = data["level"]["start"]
        self.color = data["level"]["color"]
        self.category = data["level"]["category"]

        self.chip.partial_load(data["chip"])
        self.chip.load()
        self.chip.name = f"L{self.number}"
        self.chip.private = True

        if data["level"]["version"] > 250:
            self.prepared_tt = data["level"]["prepared_tt"]
            self.is_prepared_tt = data["level"]["is_prepared_tt"]

        if data["level"]["version"] > 200:
            self.is_custom = data["level"]["is_custom"]

        logger.debug(f"Niveau chargé : {self}")

    def __str__(self) -> str:
        """Fournit une représentation sous forme de chaîne de caractères du niveau.

        Retourne :
            L'ID du niveau, son nom et son index.
        """
        return f"Niveau (#{self.id}) {self.name} {self.number}"