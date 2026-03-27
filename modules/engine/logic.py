import random
import time
from line_profiler import profile
from modules.logger import Logger
from modules.data.custom import CustomGate
from modules.data.chip import Chip
from modules.data.gate import Gate

"""Fournit la logique de simulation pour les puces de circuit, incluant les opérations 
des portes, la propagation du signal et le parcours du circuit."""

logger: Logger = Logger("Engine")


def gate_and(inputs: list[int]) -> list[int]:
    """Calcule l'opération ET (AND).

    Args:
        inputs: Liste contenant deux bits d'entrée.

    Returns:
        Résultat de l'opération ET.
    """
    return [(inputs[0] and inputs[1]) * 1]

def gate_tand(inputs: list[int]) -> list[int]:
    """Calcule l'opération ET (AND).

    Args:
        inputs: Liste contenant trois bits d'entrée.

    Returns:
        Résultat de l'opération ET.
    """
    return [(inputs[0] and inputs[1] and inputs[2]) * 1]


def gate_adder(inputs: list[int]) -> list[int]:
    """Calcule l'opération d'un additionneur complet (Full Adder).

    Args:
        inputs: Liste contenant trois bits d'entrée [A, B, Cin].

    Returns:
        [Somme, Retenue]
    """
    A, B, Cin = inputs

    sum_bit = A ^ B ^ Cin
    carry = (A & B) | (Cin & (A ^ B))

    return [sum_bit, carry]


def gate_subtractor(inputs: list[int]) -> list[int]:
    """Calcule l'opération d'un soustracteur complet (Full Subtractor).

    Args:
        inputs: Liste contenant trois bits d'entrée [A, B, Bin].

    Returns:
        [Différence, Retenue]
    """
    A, B, Bin = inputs

    diff = A ^ B ^ Bin
    borrow = ((~A & 1) & B) | (Bin & (~(A ^ B) & 1))

    return [diff, borrow]


def gate_or(inputs: list[int]) -> list[int]:
    """Calcule l'opération OU (OR).

    Args:
        inputs: Liste contenant deux bits d'entrée.

    Returns:
        Résultat de l'opération OU.
    """
    return [(inputs[0] or inputs[1]) * 1]

def gate_tor(inputs: list[int]) -> list[int]:
    """Calcule l'opération OU (OR).

    Args:
        inputs: Liste contenant trois bits d'entrée.

    Returns:
        Résultat de l'opération OU.
    """
    return [(inputs[0] or inputs[1] or inputs[2]) * 1]


def gate_not(inputs: list[int]) -> list[int]:
    """Calcule l'opération NON (NOT).

    Args:
        inputs: Liste contenant un seul bit d'entrée.

    Returns:
        Bit inversé.
    """
    return [(not inputs[0]) * 1]


def gate_xor(inputs: list[int]) -> list[int]:
    """Calcule l'opération OU exclusif (XOR).

    Args:
        inputs: Liste contenant deux bits d'entrée.

    Returns:
        Résultat de l'opération XOR.
    """
    return [(inputs[0] ^ inputs[1]) * 1]


def gate_nand(inputs: list[int]) -> list[int]:
    """Calcule l'opération NON-ET (NAND).

    Args:
        inputs: Liste contenant deux bits d'entrée.

    Returns:
        Résultat de l'opération NAND.
    """
    return [(not (inputs[0] and inputs[1])) * 1]


def gate_nor(inputs: list[int]) -> list[int]:
    """Calcule l'opération NON-OU (NOR).

    Args:
        inputs: Liste contenant deux bits d'entrée.

    Returns:
        Résultat de l'opération NOR.
    """
    return [(not (inputs[0] or inputs[1])) * 1]


def gate_clk(inputs: list[int] = []) -> list[int]:
    """Fournit un signal d'horloge basé sur le temps système.

    Args:
        inputs: Liste d'entrées ignorée.

    Returns:
        Bit alternant basé sur l'horodatage Unix actuel.
    """
    return [round(time.time()) % 2]


def gate_pass(inputs: list[int]) -> list[int]:
    """Transmet les valeurs d'entrée sans modification.

    Args:
        inputs: Liste d'entrée à transmettre.

    Returns:
        Liste d'entrée inchangée.
    """
    return inputs


def gate_8not(inputs: list[int]) -> list[int]:
    """Effectue une inversion sur 8 bits via XOR.

    Args:
        inputs: Liste contenant une valeur entière de 8 bits.

    Returns:
        Valeur 8 bits avec inversion bit à bit.
    """
    return [inputs[0] ^ ((1 << 8) - 1)]


def gate_8and(inputs: list[int]) -> list[int]:
    """Effectue un ET (AND) sur 8 bits.

    Args:
        inputs: Liste contenant deux valeurs entières de 8 bits.

    Returns:
        Résultat du ET bit à bit des entrées.
    """
    return [(inputs[0] & inputs[1]) & ((1 << 8) - 1)]


def gate_8or(inputs: list[int]) -> list[int]:
    """Effectue un OU (OR) sur 8 bits.

    Args:
        inputs: Liste contenant deux valeurs entières de 8 bits.

    Returns:
        Résultat du OU bit à bit des entrées.
    """
    return [(inputs[0] | inputs[1]) & ((1 << 8) - 1)]


def gate_8xor(inputs: list[int]) -> list[int]:
    """Effectue un OU exclusif (XOR) sur 8 bits.

    Args:
        inputs: Liste contenant deux valeurs entières de 8 bits.

    Returns:
        Résultat du XOR bit à bit des entrées.
    """
    return [(inputs[0] ^ inputs[1]) & ((1 << 8) - 1)]


def gate_8nand(inputs: list[int]) -> list[int]:
    """Effectue un NON-ET (NAND) sur 8 bits.

    Args:
        inputs: Liste contenant deux valeurs entières de 8 bits.

    Returns:
        Résultat du NAND bit à bit des entrées.
    """
    return [~(inputs[0] & inputs[1]) & ((1 << 8) - 1)]


def gate_8nor(inputs: list[int]) -> list[int]:
    """Effectue un NON-OU (NOR) sur 8 bits.

    Args:
        inputs: Liste contenant deux valeurs entières de 8 bits.

    Returns:
        Résultat du NOR bit à bit des entrées.
    """
    return [~(inputs[0] | inputs[1]) & ((1 << 8) - 1)]


def gate_8maker(inputs: list[int]) -> list[int]:
    """Convertit une séquence de bits en un entier de 8 bits.

    Args:
        inputs: Liste de bits individuels.

    Returns:
        Liste à élément unique contenant la représentation entière.
    """

    return [int("".join(map(str, inputs)), 2)]


def gate_8breaker(inputs: list[int]) -> list[int]:
    """Décompose un entier de 8 bits en une séquence de bits.

    Args:
        inputs: Liste contenant l'entier à décomposer.

    Returns:
        Représentation binaire sur 8 bits sous forme de liste d'entiers.
    """
    return [int(bit) for bit in format(inputs[0], "08b")]


def gate_delay(inputs: list[int], gate: Gate) -> list[int]:
    """Maintient le signal pendant 1 tick.

    Args:
        inputs: Liste contenant un bit d'entrée.

    Returns:
        Le bit tel qu'il était il y a un tick.
    """
    old = gate.old_output
    gate.old_output = inputs[0]
    return [old]


def gate_8adder(inputs: list[int]) -> int:
    """Additionneur 8 bits sans sortie de retenue.

    Args:
        inputs: [A, B] où 0 <= A, B <= 255

    Returns:
        Résultat 8 bits (0–255)
    """
    A, B = inputs
    return [(A + B) & 0xFF]


def gate_8subtractor(inputs: list[int]) -> int:
    """Soustracteur 8 bits sans sortie de retenue.

    Args:
        inputs: [A, B] où 0 <= A, B <= 255

    Returns:
        Résultat 8 bits (0–255)
    """
    A, B = inputs
    return [(A - B) & 0xFF]

def gate_8mux(inputs: list[int]) -> list[int]:
    """
    Utilise la première entrée comme sélecteur pour choisir l'une des 8 entrées suivantes.
    
    Args:
        inputs: Une liste où l'indice 0 est le sélecteur (0-7) 
                et les indices 1-8 sont les entrées de données.

    Returns:
        La valeur d'entrée choisie.
    """

    selector = inputs[0] % 8
    data_bits = inputs[1:9]
    
    return [data_bits[selector]]

def gate_register(inputs: list[int], gate: Gate) -> list[int]:
    """
    Stocke une valeur unique de 8 bits.

    Args:
        inputs: Valeur d'entrée (8), Save (Sauvegarder), Load (Charger)

    Returns:
        0 ou la valeur stockée.
    """

    if inputs[1] == True:
        gate.current_value = inputs[0]

    if inputs[2] == True:
        return [gate.current_value]
    return [0]

LOGIC_MAP: dict[str, callable] = {
    "AND": gate_and,
    "OR": gate_or,
    "TAND": gate_tand,
    "TOR": gate_tor,
    "NOT": gate_not,
    "XOR": gate_xor,
    "NAND": gate_nand,
    "NOR": gate_nor,
    "CLK": gate_clk,
    "PASS": gate_pass,
    "8NOT": gate_8not,
    "8BREAK": gate_8breaker,
    "8MAKER": gate_8maker,
    "DLY": gate_delay,
    "8AND": gate_8and,
    "8OR": gate_8or,
    "8NAND": gate_8nand,
    "8NOR": gate_8nor,
    "ADDER": gate_adder,
    "SUB": gate_subtractor,
    "8ADDER": gate_8adder,
    "8SUB": gate_8subtractor,
    "8XOR": gate_8xor,
    "8MUX": gate_8mux,
    "8REGISTER": gate_register,
}


class Engine:
    """Simule le comportement des puces de circuit et la propagation des signaux."""

    @profile
    def calculate_output(
        self, gate_type: str, inputs: list[int], gate: Gate
    ) -> list[int]:
        """Calcule la sortie pour une porte logique standard.

        Args:
            gate_type: Identifiant pour la logique de la porte.
            inputs: Valeurs d'entrée pour la porte.

        Returns:
            Valeurs de sortie sous forme de liste.
        """
        if gate_type in LOGIC_MAP:
            if gate_type in ["DLY", "8REGISTER"]:
                return LOGIC_MAP[gate_type](inputs, gate)
            return LOGIC_MAP[gate_type](inputs)
        return [False]

    @profile
    def calculate_custom(self, gate: CustomGate) -> None:
        """Simule la logique interne pour un composant de porte personnalisé.

        Args:
            gate: Objet de porte personnalisée à simuler.
        """
        gate.prop_io()
        self.propagate_values(gate.chip, visible=False)
        gate.update_io()

    @profile
    def sort_gates(self, chip: Chip) -> tuple[list[str], list[str], list[str]]:
        """Catégorise les composants de la puce en portes logiques, d'entrée et de sortie.

        Args:
            chip: La structure de la puce à analyser.

        Returns:
            Tuple contenant les listes d'IDs des portes logiques, d'entrée et de sortie.
        """
        gates: list[str] = []
        inputs: list[str] = []
        outputs: list[str] = []
        for gate_id, gate in chip.gates.items():
            if gate.type == "Input":
                inputs.append(gate.id)
            elif gate.type == "Output":
                outputs.append(gate.id)
            else:
                gates.append(gate.id)
        return gates, inputs, outputs

    @profile
    def draw_connections(
        self, chip: Chip, inputs: list[str], outputs: list[str], gates: list[str]
    ) -> dict[str, list]:
        """Construit une carte de connectivité pour la puce.

        Args:
            chip: La structure de la puce.
            inputs: Liste des IDs des portes d'entrée.
            outputs: Liste des IDs des portes de sortie.
            gates: Liste des IDs des portes logiques.

        Returns:
            Dictionnaire associant les IDs de portes aux structures de chemin de connexion.
        """
        paths = chip.paths
        result: dict[str, list] = {}

        for i in inputs:
            gate = chip.gates[i]
            result[gate.id] = [[], [[] for _ in range(len(gate.outputs))]]

        for o in outputs:
            gate = chip.gates[o]
            result[gate.id] = [[[] for _ in range(len(gate.inputs))], []]

        for g in gates:
            gate = chip.gates[g]
            result[gate.id] = [
                [[] for _ in range(len(gate.inputs))],
                [[] for _ in range(len(gate.outputs))],
            ]

        for path_id, path in paths.items():
            path_outputs = [out.copy() + [path.id] for out in path.outputs]
            for input_info in path.inputs:
                if input_info[1] in result:
                    result[input_info[1]][1][input_info[2]].append(path_outputs)

        return result

    @profile
    def reset_input_validation(
        self, chip: Chip, gates: list[str], outputs: list[str]
    ) -> None:
        """Réinitialise l'état de validation pour toutes les portes et chemins.

        Args:
            chip: L'objet puce à réinitialiser.
            gates: IDs des portes logiques.
            outputs: IDs des portes de sortie.
        """
        for gate_id in gates + outputs:
            gate = chip.gates[gate_id]
            gate.val_inputs = [False] * len(gate.inputs)
            gate.val_done = False

        for path in chip.paths.values():
            path.val_done = False

    @profile
    def get_wired_inputs_map(self, connections: dict[str, list]) -> dict[str, set[int]]:
        """Associe les ports d'entrée des portes à leur statut de câblage.

        Args:
            connections: Carte de connectivité de la puce.

        Returns:
            Dictionnaire associant l'ID de la porte à un ensemble d'indices de ports d'entrée actifs.
        """
        wired_map: dict[str, set[int]] = {}
        for source_id, data in connections.items():
            for port_conns in data[1]:
                for path_group in port_conns:
                    for conn in path_group:
                        target_id, target_port = conn[1], conn[2]
                        wired_map.setdefault(target_id, set()).add(target_port)
        return wired_map

    @profile
    def propagate_outputs(
        self, chip: Chip, connections: dict[str, list], source_id: str, visible=False
    ) -> None:
        """Propage le signal d'une porte source vers les cibles connectées.

        Args:
            chip: La structure de la puce.
            connections: Carte de connectivité de la puce.
            source_id: ID de la porte à l'origine du signal.
        """
        if source_id not in connections:
            return

        gate = chip.gates[source_id]

        for out_idx, target_paths in enumerate(connections[source_id][1]):
            if out_idx >= len(gate.outputs):
                continue

            signal_value = gate.outputs[out_idx]*1

            for path_group in target_paths:
                for conn in path_group:
                    target_gate = chip.gates[conn[1]]
                    target_port = conn[2]
                    path_id = conn[5]

                    should_write = True

                    if should_write:
                        target_gate.inputs[target_port] = signal_value
                        target_gate.val_inputs[target_port] = True

                    if path_id in chip.paths:
                        chip.paths[path_id].current_value = signal_value
                        chip.paths[path_id].val_done = True
                    if visible:
                        if target_gate.type in ["Output", "Gate"]:
                            target_gate.gen_tile_pattern()
                        if (
                            target_gate.type == "Complex"
                            or target_gate.gate_type == "8Output"
                        ):
                            target_gate.update_text_readings()

    @profile
    def run_propagation_loop(
        self,
        chip: Chip,
        connections: dict[str, list],
        gates: list[str],
        inputs: list[str],
        outputs: list[str],
        visible: bool = False,
    ) -> None:
        """Simule de manière itérative la propagation du signal à travers les portes logiques.

        Args:
            chip: La puce en cours de simulation.
            connections: Carte de connectivité.
            gates: IDs des portes logiques.
            inputs: IDs des portes d'entrée.
            outputs: IDs des portes de sortie.
        """
        unprocessed = set(gates + outputs)
        wired_inputs_map = self.get_wired_inputs_map(connections)
        safeguard_max: int = 2000
        iterations: int = 0

        while unprocessed and iterations < safeguard_max:
            iterations += 1
            processed_this_frame: list[str] = []

            for gate_id in list(unprocessed):
                gate = chip.gates[gate_id]
                is_ready = all(
                    gate.val_inputs[port] for port in wired_inputs_map.get(gate_id, [])
                )

                if is_ready:
                    if gate.type in ["Gate", "Complex"]:
                        gate.outputs = self.calculate_output(
                            gate.gate_type, gate.inputs, gate
                        )
                    elif gate.type == "Custom":
                        self.calculate_custom(gate)

                    self.propagate_outputs(chip, connections, gate_id, visible=visible)
                    gate.val_done = True
                    processed_this_frame.append(gate_id)

            for pid in processed_this_frame:
                unprocessed.remove(pid)

            # Forcer la résolution des portes bloquées
            if not processed_this_frame and unprocessed:
                random_id = list(unprocessed)[0]
                gate = chip.gates[random_id]

                if gate.type in ["Gate", "Complex"]:
                    gate.outputs = self.calculate_output(
                        gate.gate_type, gate.inputs, gate
                    )
                elif gate.type == "Custom":
                    self.calculate_custom(gate)

                self.propagate_outputs(chip, connections, random_id, visible=visible)
                gate.val_done = True
                unprocessed.remove(random_id)

        if iterations >= safeguard_max:
            logger.warning("Limite de sécurité atteinte. Boucle infinie ou circuit trop complexe.")

    @profile
    def propagate_values(self, chip: Chip, visible=True) -> None:
        """Initialise et lance la séquence de propagation du signal.

        Args:
            chip: L'objet puce à simuler.
        """
        gates, inputs, outputs = self.sort_gates(chip)
        connections = self.draw_connections(chip, inputs, outputs, gates)
        self.reset_input_validation(chip, gates, outputs)

        for inp_id in inputs:
            self.propagate_outputs(chip, connections, inp_id, visible=visible)

        self.run_propagation_loop(
            chip, connections, gates, inputs, outputs, visible=visible
        )