import random
import time
from line_profiler import profile
from modules.logger import Logger
from modules.data.custom import CustomGate
from modules.data.chip import Chip
from modules.data.gate import Gate

"""Provides simulation logic for circuit chips, including gate operations, 
signal propagation, and circuit traversal."""

logger: Logger = Logger("Engine")


def gate_and(inputs: list[int]) -> list[int]:
    """Calculates AND operation.

    Args:
        inputs: List containing two input bits.

    Returns:
        Result of the AND operation.
    """
    return [(inputs[0] and inputs[1]) * 1]


def gate_adder(inputs: list[int]) -> list[int]:
    """Calculates Full Adder operation.

    Args:
        inputs: List containing three input bits [A, B, Cin].

    Returns:
        [Sum, Carry]
    """
    A, B, Cin = inputs

    sum_bit = A ^ B ^ Cin
    carry = (A & B) | (Cin & (A ^ B))

    return [sum_bit, carry]


def gate_subtractor(inputs: list[int]) -> list[int]:
    """Calculates Full Subtractor operation.

    Args:
        inputs: List containing three input bits [A, B, Bin].

    Returns:
        [Difference, Borrow]
    """
    A, B, Bin = inputs

    diff = A ^ B ^ Bin
    borrow = ((~A & 1) & B) | (Bin & (~(A ^ B) & 1))

    return [diff, borrow]


def gate_or(inputs: list[int]) -> list[int]:
    """Calculates OR operation.

    Args:
        inputs: List containing two input bits.

    Returns:
        Result of the OR operation.
    """
    return [(inputs[0] or inputs[1]) * 1]


def gate_not(inputs: list[int]) -> list[int]:
    """Calculates NOT operation.

    Args:
        inputs: List containing a single input bit.

    Returns:
        Inverted bit.
    """
    return [(not inputs[0]) * 1]


def gate_xor(inputs: list[int]) -> list[int]:
    """Calculates XOR operation.

    Args:
        inputs: List containing two input bits.

    Returns:
        Result of the XOR operation.
    """
    return [(inputs[0] ^ inputs[1]) * 1]


def gate_nand(inputs: list[int]) -> list[int]:
    """Calculates NAND operation.

    Args:
        inputs: List containing two input bits.

    Returns:
        Result of the NAND operation.
    """
    return [(not (inputs[0] and inputs[1])) * 1]


def gate_nor(inputs: list[int]) -> list[int]:
    """Calculates NOR operation.

    Args:
        inputs: List containing two input bits.

    Returns:
        Result of the NOR operation.
    """
    return [(not (inputs[0] or inputs[1])) * 1]


def gate_clk(inputs: list[int] = []) -> list[int]:
    """Provides a clock signal based on system time.

    Args:
        inputs: Ignored input list.

    Returns:
        Alternating bit based on current Unix timestamp.
    """
    return [round(time.time()) % 2]


def gate_pass(inputs: list[int]) -> list[int]:
    """Passes input values through unchanged.

    Args:
        inputs: Input list to pass.

    Returns:
        Input list unchanged.
    """
    return inputs


def gate_8not(inputs: list[int]) -> list[int]:
    """Performs 8-bit inversion via XOR.

    Args:
        inputs: List containing an 8-bit integer value.

    Returns:
        Bitwise inverted 8-bit value.
    """
    return [inputs[0] ^ ((1 << 8) - 1)]


def gate_8and(inputs: list[int]) -> list[int]:
    """Performs 8-bit AND.

    Args:
        inputs: List containing two 8-bit integer values.

    Returns:
        Bitwise AND of inputs.
    """
    return [(inputs[0] & inputs[1]) & ((1 << 8) - 1)]


def gate_8or(inputs: list[int]) -> list[int]:
    """Performs 8-bit OR.

    Args:
        inputs: List containing two 8-bit integer values.

    Returns:
        Bitwise OR of inputs.
    """
    return [(inputs[0] | inputs[1]) & ((1 << 8) - 1)]


def gate_8xor(inputs: list[int]) -> list[int]:
    """Performs 8-bit XOR.

    Args:
        inputs: List containing two 8-bit integer values.

    Returns:
        Bitwise XOR of inputs.
    """
    return [(inputs[0] ^ inputs[1]) & ((1 << 8) - 1)]


def gate_8nand(inputs: list[int]) -> list[int]:
    """Performs 8-bit NAND.

    Args:
        inputs: List containing two 8-bit integer values.

    Returns:
        Bitwise NAND of inputs.
    """
    return [~(inputs[0] & inputs[1]) & ((1 << 8) - 1)]


def gate_8nor(inputs: list[int]) -> list[int]:
    """Performs 8-bit NOR.

    Args:
        inputs: List containing two 8-bit integer values.

    Returns:
        Bitwise NOR of inputs.
    """
    return [~(inputs[0] | inputs[1]) & ((1 << 8) - 1)]


def gate_8maker(inputs: list[int]) -> list[int]:
    """Converts a sequence of bits into an 8-bit integer.

    Args:
        inputs: List of individual bits.

    Returns:
        Single-element list containing the integer representation.
    """
    result = []
    for i in inputs:
        result.append(i*1)
    return [int("".join(map(str, result)), 2)]


def gate_8breaker(inputs: list[int]) -> list[int]:
    """Decomposes an 8-bit integer into a sequence of bits.

    Args:
        inputs: List containing the integer to decompose.

    Returns:
        8-bit binary representation as a list of integers.
    """
    return [int(bit) for bit in format(inputs[0], "08b")]


def gate_delay(inputs: list[int], gate: Gate) -> list[int]:
    """Hold the signal for 1 tick.

    Args:
        inputs: List containing one input bit.

    Returns:
        Bit as it was one tick ago.
    """
    old = gate.old_output
    gate.old_output = inputs[0]
    return [old]


def gate_8adder(inputs: list[int]) -> int:
    """8-bit adder without carry output.

    Args:
        inputs: [A, B] where 0 <= A, B <= 255

    Returns:
        8-bit result (0–255)
    """
    A, B = inputs
    return [(A + B) & 0xFF]


def gate_8subtractor(inputs: list[int]) -> int:
    """8-bit subtractor without borrow output.

    Args:
        inputs: [A, B] where 0 <= A, B <= 255

    Returns:
        8-bit result (0–255)
    """
    A, B = inputs
    return [(A - B) & 0xFF]


LOGIC_MAP: dict[str, callable] = {
    "AND": gate_and,
    "OR": gate_or,
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
}


class Engine:
    """Simulates circuit chip behavior and signal propagation."""

    @profile
    def calculate_output(
        self, gate_type: str, inputs: list[int], gate: Gate
    ) -> list[int]:
        """Calculates output for a standard logic gate.

        Args:
            gate_type: Identifier for the gate logic.
            inputs: Input values for the gate.

        Returns:
            Output values as a list.
        """
        if gate_type in LOGIC_MAP:
            if gate_type == "DLY":
                return LOGIC_MAP[gate_type](inputs, gate)
            return LOGIC_MAP[gate_type](inputs)
        return [False]

    @profile
    def calculate_custom(self, gate: CustomGate) -> None:
        """Simulates internal logic for a custom gate component.

        Args:
            gate: Custom gate object to be simulated.
        """
        gate.prop_io()
        self.propagate_values(gate.chip, visible=False)
        gate.update_io()

    @profile
    def sort_gates(self, chip: Chip) -> tuple[list[str], list[str], list[str]]:
        """Categorizes chip components into logic, input, and output gates.

        Args:
            chip: The chip structure to analyze.

        Returns:
            Tuple containing lists of logic gate IDs, input IDs, and output IDs.
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
        """Builds a connectivity map for the chip.

        Args:
            chip: The chip structure.
            inputs: List of input gate IDs.
            outputs: List of output gate IDs.
            gates: List of logic gate IDs.

        Returns:
            Dictionary mapping gate IDs to connection path structures.
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
        """Resets validation state for all gates and paths.

        Args:
            chip: The chip object to reset.
            gates: Logic gate IDs.
            outputs: Output gate IDs.
        """
        for gate_id in gates + outputs:
            gate = chip.gates[gate_id]
            gate.val_inputs = [False] * len(gate.inputs)
            gate.val_done = False

        for path in chip.paths.values():
            path.val_done = False

    @profile
    def get_wired_inputs_map(self, connections: dict[str, list]) -> dict[str, set[int]]:
        """Maps gate input ports to their wired status.

        Args:
            connections: Connectivity map of the chip.

        Returns:
            Dictionary mapping gate ID to a set of active input port indices.
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
        """Propagates signal from a source gate to connected targets.

        Args:
            chip: The chip structure.
            connections: Connectivity map of the chip.
            source_id: ID of the gate originating the signal.
        """
        if source_id not in connections:
            return

        gate = chip.gates[source_id]

        for out_idx, target_paths in enumerate(connections[source_id][1]):
            if out_idx >= len(gate.outputs):
                continue

            signal_value = gate.outputs[out_idx]

            for path_group in target_paths:
                for conn in path_group:
                    target_gate = chip.gates[conn[1]]
                    target_port = conn[2]
                    path_id = conn[5]

                    should_write = True
                    if target_gate.val_inputs[target_port]:
                        if random.random() < 0.5:
                            should_write = False
                        else:
                            should_write = False

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
        """Iteratively simulates signal propagation through logic gates.

        Args:
            chip: The chip being simulated.
            connections: Connectivity map.
            gates: Logic gate IDs.
            inputs: Input gate IDs.
            outputs: Output gate IDs.
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

            # Force resolution of stalled gates
            if not processed_this_frame and unprocessed:
                random_id = random.choice(list(unprocessed))
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
            logger.warning("Safeguard reached. Infinite loop or too complex.")

    @profile
    def propagate_values(self, chip: Chip, visible=True) -> None:
        """Initializes and runs the signal propagation sequence.

        Args:
            chip: The chip object to simulate.
        """
        gates, inputs, outputs = self.sort_gates(chip)
        connections = self.draw_connections(chip, inputs, outputs, gates)
        self.reset_input_validation(chip, gates, outputs)

        for inp_id in inputs:
            self.propagate_outputs(chip, connections, inp_id, visible=visible)

        self.run_propagation_loop(
            chip, connections, gates, inputs, outputs, visible=visible
        )
