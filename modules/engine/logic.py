import random
import time

def gate_and(inputs):
    return [inputs[0] and inputs[1]]

def gate_or(inputs):
    return [inputs[0] or inputs[1]]

def gate_not(inputs):
    return [not inputs[0]]

def gate_xor(inputs):
    return [inputs[0] ^ inputs[1]]

def gate_nand(inputs):
    return [not (inputs[0] and inputs[1])]

def gate_nor(inputs):
    return [not (inputs[0] or inputs[1])]

def gate_clk(inputs):
    return [round(time.time()) % 2 == 0]

def gate_pass(inputs):
    return inputs

LOGIC_MAP = {
    "AND": gate_and,
    "OR": gate_or,
    "NOT": gate_not,
    "XOR": gate_xor,
    "NAND": gate_nand,
    "NOR": gate_nor,
    "CLK": gate_clk,
    "PASS": gate_pass
}

def calculate_output(gate_name, inputs):
    if gate_name in LOGIC_MAP:
        return LOGIC_MAP[gate_name](inputs)
    return False

def sort_gates(chip):
    gates = []
    inputs = []
    outputs = []

    for i in chip.gates:
        gate = chip.gates[i]
        current = gate.type
        id = gate.id
        if current == "Input":
            inputs.append(id)
        elif current == "Output":
            outputs.append(id)
        else:
            gates.append(id)

    return gates, inputs, outputs

def draw_connections(chip, inputs, outputs, gates):
    paths = chip.paths
    result = {}

    for a in inputs:
        i = chip.gates[a]
        result[i.id] = [[], [[] for _ in range(len(i.outputs))]]
        
    for b in outputs:
        output = chip.gates[b]
        result[output.id] = [[[] for _ in range(len(output.inputs))], []]

    for c in gates:
        gate = chip.gates[c]
        result[gate.id] = [[[] for _ in range(len(gate.inputs))], [[] for _ in range(len(gate.outputs))]]

    for d in paths:
        path = paths[d]
        path_outputs = []

        for out in path.outputs:
            new = out.copy()
            new.append(path.id)
            path_outputs.append(new)

        for i in path.inputs:
            if i[1] in result:
                result[i[1]][1][i[2]].append(path_outputs)

    return result

def reset_input_validation(chip, gates, outputs):
    for i in gates + outputs:
        gate = chip.gates[i]
        gate.val_inputs = [False for _ in range(len(gate.inputs))]    
        gate.val_done = False

    for i in chip.paths:
        chip.paths[i].val_done = False

def get_wired_inputs_map(connections):

    wired_map = {}
    
    for source_id, data in connections.items():
        outputs_config = data[1] 
        for port_conns in outputs_config:
            for path_group in port_conns:
                for conn in path_group:
                    # conn format: [Type, target_id, target_port, ...]
                    target_id = conn[1]
                    target_port = conn[2]
                    
                    if target_id not in wired_map:
                        wired_map[target_id] = set()
                    wired_map[target_id].add(target_port)
    return wired_map

def propagate_outputs(chip, connections, source_id):
    if source_id not in connections:
        return

    for output_port_index, target_paths in enumerate(connections[source_id][1]):

        if len(chip.gates[source_id].outputs) <= output_port_index:
            continue
            
        signal_value = chip.gates[source_id].outputs[output_port_index]

        for path_group in target_paths:
            for conn in path_group:
                target_id = conn[1]
                target_port = conn[2]
                path_id = conn[5]

                target_gate = chip.gates[target_id]

                should_write = True
                if target_gate.val_inputs[target_port]:
                    if random.random() < 0.5:
                        should_write = False 
                    else:
                        should_write = True 
                
                if should_write:
                    target_gate.inputs[target_port] = signal_value
                    target_gate.val_inputs[target_port] = True

                if path_id in chip.paths:
                    chip.paths[path_id].current_value = signal_value
                    chip.paths[path_id].val_done = True

                if target_gate.type in ["Output","Gate"]:
                    target_gate.gen_tile_pattern()

def run_propagation_loop(chip, connections, gates, inputs, outputs):
    unprocessed = set(gates + outputs)
    
    wired_inputs_map = get_wired_inputs_map(connections)

    safeguard_max = 2000
    iterations = 0

    while unprocessed and iterations < safeguard_max:
        iterations += 1
        processed_this_frame = []

        for gate_id in list(unprocessed):
            gate = chip.gates[gate_id]
            
            is_ready = True
            
            if gate_id in wired_inputs_map:
                required_ports = wired_inputs_map[gate_id]
                for port_idx in required_ports:
                    if not gate.val_inputs[port_idx]:
                        is_ready = False
                        break

            if is_ready:
                if gate.type == "Gate":
                    gate.outputs = calculate_output(gate.gate_type, gate.inputs)

                propagate_outputs(chip, connections, gate_id)
                
                gate.val_done = True
                processed_this_frame.append(gate_id)

        for pid in processed_this_frame:
            unprocessed.remove(pid)

        if not processed_this_frame and unprocessed:
            random_id = random.choice(list(unprocessed))
            gate = chip.gates[random_id]
            
            if gate.type == "Gate":
                gate.outputs = calculate_output(gate.gate_type, gate.inputs)
            
            propagate_outputs(chip, connections, random_id)
            
            gate.val_done = True
            unprocessed.remove(random_id)

    if iterations >= safeguard_max:
        print("Safeguard reached. Infinite loop or too complex.")

def propagate_values(chip):

    gates, inputs, outputs = sort_gates(chip)
    connections = draw_connections(chip, inputs, outputs, gates)
    reset_input_validation(chip, gates, outputs)

    for inp_id in inputs:
        propagate_outputs(chip, connections, inp_id)

    run_propagation_loop(chip, connections, gates, inputs, outputs)