#  Imports
# -------------------------------------------------
import random
import time
from modules.logger import Logger # Debuging
from modules.data.custom import CustomGate
from modules.data.chip import Chip
# -------------------------------------------------

logger = Logger("Engine") # Engine's logger, to provide debug informations.

# Default gates.
# All gates here are the default gates included in the game as 'vanilla' gates.
# Differs from 'custom' gates, which are built by the user, or provided in certain levels.

def gate_and(inputs): # And Gate
    # Takes 2 Inputs, 1 Output
    # On when both inputs are on.

    # Truth Table:
    # In0 In1 Out
    #  0   0   0
    #  1   0   0
    #  0   1   0
    #  1   1   1

    return [inputs[0] and inputs[1]]

def gate_or(inputs):# Or Gate
    # Takes 2 Inputs, 1 Output
    # On when at least one inputs is on.

    # Truth Table:
    # In0 In1 Out
    #  0   0   0
    #  1   0   1
    #  0   1   1
    #  1   1   1
    return [inputs[0] or inputs[1]]

def gate_not(inputs):# Not Gate
    # Takes 1 Input, 1 Output
    # Reverse the Input

    # Truth Table:
    # In0 Out 
    #  0   1   
    #  1   0   

    return [not inputs[0]]

def gate_xor(inputs):# Xor Gate
    # Takes 2 Inputs, 1 Output
    # On when only one inputs is on.

    # Truth Table:
    # In0 In1 Out
    #  0   0   0
    #  1   0   1
    #  0   1   1
    #  1   1   0

    return [inputs[0] ^ inputs[1]]

def gate_nand(inputs):# Nand Gate
    # Takes 2 Inputs, 1 Output
    # Reverse and gate, on when not both inputs are on.
    # Same as chaining an and gate, and a not gate.

    # Truth Table:
    # In0 In1 Out
    #  0   0   1
    #  1   0   1
    #  0   1   1
    #  1   1   0

    return [not (inputs[0] and inputs[1])]

def gate_nor(inputs):# Nor Gate
    # Takes 2 Inputs, 1 Output
    # Reverse or gate, on when none are on.

    # Truth Table:
    # In0 In1 Out
    #  0   0   1
    #  1   0   0
    #  0   1   0
    #  1   1   0

    return [not (inputs[0] or inputs[1])]

def gate_clk(inputs):# Clock
    # Takes 0 Input, 1 Output
    # Special gate that switch is output each second, from on to off.

    return [round(time.time()) % 2 == 0]

def gate_pass(inputs): # Pass
    # Takes x inputs, x outputs.
    # No logic here, just outputs it's inputs.

    return inputs

LOGIC_MAP = { # List of all logic gates functions, linked with the id of the logic gate using it. Used for easy access.
    "AND": gate_and,
    "OR": gate_or,
    "NOT": gate_not,
    "XOR": gate_xor,
    "NAND": gate_nand,
    "NOR": gate_nor,
    "CLK": gate_clk,
    "PASS": gate_pass
}

def calculate_output(gate_type:str, inputs:list) -> list: 
    # Function used to calculate the outputs of a 'vanilla' logic gate, based on it's type and it's inputs.
    # Output a single False, in case of gate type not found.
    if gate_type in LOGIC_MAP:
        return LOGIC_MAP[gate_type](inputs)
    return [False]

def calculate_custom(gate: CustomGate): 
    # Function used to calculate the outputs of a 'custom' gate. 
    # The custom gate, is built on 2 levels. The top inputs and outputs, that are connected to the rest of the logic circuit, and a custom 'chip' class inside, which contains another logic circuit. Thus the name, custom gate.
    gate.prop_io() # The top inputs are replicated inside the custom chip's inputs.
    propagate_values(gate.chip) #The propagate function is called recursivly on the chip inside the gate, to simulate it's own logic circuit.
    gate.update_io() # The outputs inside the chip are replicate to the top outputs.


def sort_gates(chip: Chip) -> tuple: 
    # Function to sort the gates inside a chip based on their types, and output a tuple containing lists of gate ids.
    # Here the gates are sorted in 2 types:
    gates = [] #Logic gates, same for 'vanilla' and 'custom' logic gates.
    inputs = [] #Input gates, that are simulated first.
    outputs = [] #Output gates, the end of the simulation.

    for i in chip.gates: #Iterate through all gates in the chip
        gate = chip.gates[i]
        current = gate.type # Get the type of the gate
        id = gate.id
        if current == "Input":
            inputs.append(id) # If it's an input, add it's id to the corresponding list.
        elif current == "Output": 
            outputs.append(id)# Same if it's an output.
        else:
            gates.append(id) # If it's neither an output, nor an input, then it must be a gate.

    return gates, inputs, outputs # Return the three lists as tuple, containing the sorted ids.

def draw_connections(chip: Chip, inputs: list, outputs: list, gates: list) -> dict:
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
                elif gate.type == "Custom":
                    calculate_custom(gate)
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
            elif gate.type == "Custom":
                    calculate_custom(gate)
            
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