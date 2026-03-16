# Imports
# -------------------------------------------------
import random  # For stochastic behavior in propagation conflict resolution
import time    # For clock-based gate
from modules.logger import Logger  # Debugging/logging class
from modules.data.custom import CustomGate  # Custom gate class
from modules.data.chip import Chip  # Chip representation
# -------------------------------------------------

logger = Logger("Engine")  # Logger instance for engine debug outputs

# -------------------------------------------------
# Vanilla logic gates (default gates)
# -------------------------------------------------

def gate_and(inputs: list[int]) -> list[int]:
    """AND gate: returns 1 if both inputs are 1, else 0."""
    return [(inputs[0] and inputs[1]) * 1]


def gate_or(inputs: list[int]) -> list[int]:
    """OR gate: returns 1 if at least one input is 1, else 0."""
    return [(inputs[0] or inputs[1]) * 1]


def gate_not(inputs: list[int]) -> list[int]:
    """NOT gate: inverts a single input."""
    return [(not inputs[0]) * 1]


def gate_xor(inputs: list[int]) -> list[int]:
    """XOR gate: returns 1 if only one input is 1, else 0."""
    return [(inputs[0] ^ inputs[1]) * 1]


def gate_nand(inputs: list[int]) -> list[int]:
    """NAND gate: inverse of AND; returns 0 only if both inputs are 1."""
    return [(not (inputs[0] and inputs[1])) * 1]


def gate_nor(inputs: list[int]) -> list[int]:
    """NOR gate: inverse of OR; returns 1 only if both inputs are 0."""
    return [(not (inputs[0] or inputs[1])) * 1]


def gate_clk(inputs: list[int] = []) -> list[int]:
    """Clock gate: toggles every second; ignores inputs."""
    return [round(time.time()) % 2]


def gate_pass(inputs: list[int]) -> list[int]:
    """Pass-through gate: returns inputs unchanged."""
    return inputs


def gate_8nor(inputs: list[int]) -> list[int]:
    """8-bit NOR gate: XOR input with 0xFF (bitwise inversion for 8 bits)."""
    return [inputs[0] ^ ((1 << 8) - 1)]


def gate_8maker(inputs: list[int]) -> list[int]:
    """Convert list of 0/1 bits into an 8-bit integer."""
    return [int("".join(map(str, inputs)), 2)]


def gate_8breaker(inputs: list[int]) -> list[int]:
    """Convert an 8-bit integer into a list of 0/1 bits."""
    return [int(bit) for bit in format(inputs[0], '08b')]


# Mapping gate names to functions for vanilla logic
LOGIC_MAP = {
    "AND": gate_and,
    "OR": gate_or,
    "NOT": gate_not,
    "XOR": gate_xor,
    "NAND": gate_nand,
    "NOR": gate_nor,
    "CLK": gate_clk,
    "PASS": gate_pass,
    "8NOT": gate_8nor,
    "8BREAK": gate_8breaker,
    "8MAKER": gate_8maker,
}


# -------------------------------------------------
# Engine class: simulates a circuit chip
# -------------------------------------------------

class Engine:

    def calculate_output(self, gate_type: str, inputs: list[int]) -> list[int]:
        """
        Calculate the output of a vanilla gate.

        Parameters:
        - gate_type: str - The type of gate ("AND", "OR", etc.)
        - inputs: list[int] - Input values for the gate

        Returns:
        - list[int] - Output values (single-element list for vanilla gates)
        """
        if gate_type in LOGIC_MAP:
            return LOGIC_MAP[gate_type](inputs)
        return [False]

    def calculate_custom(self, gate: CustomGate) -> None:
        """
        Calculate outputs for a custom gate.
        Replicates top-level inputs into the internal chip,
        propagates internal logic, then updates outputs.
        """
        gate.prop_io()  # replicate top-level inputs to internal chip
        self.propagate_values(gate.chip)  # simulate internal logic
        gate.update_io()  # replicate internal outputs to top-level outputs

    def sort_gates(self, chip: Chip) -> tuple[list[str], list[str], list[str]]:
        """
        Sort gates into vanilla logic gates, inputs, and outputs.

        Returns:
        - tuple: (logic_gates, input_gates, output_gates) as lists of gate IDs (str)
        """
        gates, inputs, outputs = [], [], []
        for gate_id, gate in chip.gates.items():
            if gate.type == "Input":
                inputs.append(gate.id)
            elif gate.type == "Output":
                outputs.append(gate.id)
            else:
                gates.append(gate.id)
        return gates, inputs, outputs

    def draw_connections(self, chip: Chip, inputs: list[str], outputs: list[str], gates: list[str]) -> dict[str, list]:
        """
        Build a connection map for the chip.

        Returns:
        - dict: maps gate IDs (str) to input/output path lists
        """
        paths = chip.paths
        result = {}

        # Initialize input gate entries
        for i in inputs:
            gate = chip.gates[i]
            result[gate.id] = [[], [[] for _ in range(len(gate.outputs))]]

        # Initialize output gate entries
        for o in outputs:
            gate = chip.gates[o]
            result[gate.id] = [[[] for _ in range(len(gate.inputs))], []]

        # Initialize logic gate entries
        for g in gates:
            gate = chip.gates[g]
            result[gate.id] = [[[] for _ in range(len(gate.inputs))], [[] for _ in range(len(gate.outputs))]]

        # Fill connections based on paths
        for path_id, path in paths.items():
            path_outputs = [out.copy() + [path.id] for out in path.outputs]
            for input_info in path.inputs:
                if input_info[1] in result:
                    result[input_info[1]][1][input_info[2]].append(path_outputs)

        return result

    def reset_input_validation(self, chip: Chip, gates: list[str], outputs: list[str]) -> None:
        """
        Reset validation flags for gates and paths before simulation.
        """
        for gate_id in gates + outputs:
            gate = chip.gates[gate_id]
            gate.val_inputs = [False] * len(gate.inputs)
            gate.val_done = False

        for path in chip.paths.values():
            path.val_done = False

    def get_wired_inputs_map(self, connections: dict[str, list]) -> dict[str, set[int]]:
        """
        Build a map of which input ports are wired for each gate.

        Returns:
        - dict: {gate_id: set(port_indices)}
        """
        wired_map: dict[str, set[int]] = {}
        for source_id, data in connections.items():
            for port_conns in data[1]:
                for path_group in port_conns:
                    for conn in path_group:
                        target_id, target_port = conn[1], conn[2]
                        wired_map.setdefault(target_id, set()).add(target_port)
        return wired_map

    def propagate_outputs(self, chip: Chip, connections: dict[str, list], source_id: str) -> None:
        """
        Propagate output values from a gate to connected paths and gates.
        """
        if source_id not in connections:
            return

        gate = chip.gates[source_id]

        for out_idx, target_paths in enumerate(connections[source_id][1]):
            if out_idx >= len(gate.outputs):
                continue  # Skip missing output ports

            signal_value = gate.outputs[out_idx]

            for path_group in target_paths:
                for conn in path_group:
                    target_gate = chip.gates[conn[1]]
                    target_port = conn[2]
                    path_id = conn[5]

                    # Randomized conflict resolution
                    if target_gate.val_inputs[target_port] and random.random() < 0.5:
                        continue

                    target_gate.inputs[target_port] = signal_value
                    target_gate.val_inputs[target_port] = True

                    if path_id in chip.paths:
                        chip.paths[path_id].current_value = signal_value
                        chip.paths[path_id].val_done = True

                    if target_gate.type in ["Output", "Gate"]:
                        target_gate.gen_tile_pattern()
                    if target_gate.type == "Complex" or target_gate.gate_type == "8Output":
                        target_gate.update_text_readings()

    def run_propagation_loop(self, chip: Chip, connections: dict[str, list], gates: list[str], inputs: list[str], outputs: list[str]) -> None:
        """
        Execute simulation loop until all gates have propagated their outputs.
        Includes safeguard to prevent infinite loops.
        """
        unprocessed = set(gates + outputs)
        wired_inputs_map = self.get_wired_inputs_map(connections)
        safeguard_max = 2000
        iterations = 0

        while unprocessed and iterations < safeguard_max:
            iterations += 1
            processed_this_frame = []

            # Process ready gates
            for gate_id in list(unprocessed):
                gate = chip.gates[gate_id]
                is_ready = all(gate.val_inputs[port] for port in wired_inputs_map.get(gate_id, []))
                
                if is_ready:
                    if gate.type in ["Gate", "Complex"]:
                        gate.outputs = self.calculate_output(gate.gate_type, gate.inputs)
                    elif gate.type == "Custom":
                        self.calculate_custom(gate)

                    self.propagate_outputs(chip, connections, gate_id)
                    gate.val_done = True
                    processed_this_frame.append(gate_id)

            # Remove processed gates
            for pid in processed_this_frame:
                unprocessed.remove(pid)

            # Force process one random gate if stuck
            if not processed_this_frame and unprocessed:
                random_id = random.choice(list(unprocessed))
                gate = chip.gates[random_id]

                if gate.type in ["Gate", "Complex"]:
                    gate.outputs = self.calculate_output(gate.gate_type, gate.inputs)
                elif gate.type == "Custom":
                    self.calculate_custom(gate)

                self.propagate_outputs(chip, connections, random_id)
                gate.val_done = True
                unprocessed.remove(random_id)

        if iterations >= safeguard_max:
            print("Safeguard reached. Infinite loop or too complex.")

    def propagate_values(self, chip: Chip) -> None:
        """
        Top-level function to propagate all input values through a chip.
        """
        gates, inputs, outputs = self.sort_gates(chip)
        connections = self.draw_connections(chip, inputs, outputs, gates)
        self.reset_input_validation(chip, gates, outputs)

        for inp_id in inputs:
            self.propagate_outputs(chip, connections, inp_id)

        self.run_propagation_loop(chip, connections, gates, inputs, outputs)