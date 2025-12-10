def gate_and(inputs):
    return inputs[0] and inputs[1]

def gate_or(inputs):
    return inputs[0] or inputs[1]

def gate_not(inputs):
    return not inputs[0]

def gate_xor(inputs):
    return inputs[0] ^ inputs[1]

def gate_nand(inputs):
    return not (inputs[0] and inputs[1])

def gate_nor(inputs):
    return not (inputs[0] or inputs[1])

LOGIC_MAP = {
    "AND": gate_and,
    "OR": gate_or,
    "NOT": gate_not,
    "XOR": gate_xor,
    "NAND": gate_nand,
    "NOR": gate_nor,
}

def calculate_output(gate_name, inputs):
    """Calculates the output of a gate based on its name and inputs."""
    if gate_name in LOGIC_MAP:
        return LOGIC_MAP[gate_name](inputs)
    return False

def propagate_values(gates, paths):
    """Propagates values from gate outputs to gate inputs through paths."""
    # Reset all path values
    for path in paths.values():
        path.current_value = False

    # Set path values based on their connected gate outputs
    for path in paths.values():
        for output_gate_id, output_pin_index in path.outputs:
            if output_gate_id in gates:
                path.current_value = gates[output_gate_id].outputs[output_pin_index]
                break  # Assume one output source per path for now

    # Update gate inputs based on the new path values
    for gate in gates.values():
        # Reset inputs before propagation
        for i in range(len(gate.inputs)):
            gate.inputs[i] = False

    for path in paths.values():
        for input_gate_id, input_pin_index in path.inputs:
            if input_gate_id in gates:
                gate = gates[input_gate_id]
                if input_pin_index < len(gate.inputs):
                    gate.inputs[input_pin_index] = path.current_value