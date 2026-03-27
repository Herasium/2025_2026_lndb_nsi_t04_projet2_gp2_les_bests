"""Module de registre pour les composants de portes logiques.

Fournit une cartographie centralisée des identifiants de chaînes de caractères vers 
leurs implémentations de classes de portes logiques respectives pour les systèmes 
1-bit, 8-bits et à largeurs mixtes.
"""

from typing import Dict, Type, Any

# Importations des nœuds 1-bit
from modules.data.nodes.one.gand import And
from modules.data.nodes.one.gnot import Not
from modules.data.nodes.one.gor import Or
from modules.data.nodes.one.nand import Nand
from modules.data.nodes.one.nor import Nor
from modules.data.nodes.one.xor import Xor
from modules.data.nodes.one.clock import Clock
from modules.data.nodes.one.gpass import Pass
from modules.data.nodes.one.input import Input
from modules.data.nodes.one.output import Output
from modules.data.nodes.one.delay import Delay
from modules.data.nodes.one.addr import Adder
from modules.data.nodes.one.sub import Sub
from modules.data.nodes.one.on import On
from modules.data.nodes.one.off import Off
from modules.data.nodes.one.tand import TAnd
from modules.data.nodes.one.tor import TOr

# Importations des nœuds 8-bits
from modules.data.nodes.eight.gnot import Not as Not_8
from modules.data.nodes.eight.input import Input as Input_8
from modules.data.nodes.eight.output import Output as Output_8
from modules.data.nodes.eight.gand import And as And_8
from modules.data.nodes.eight.gor import Or as Or_8
from modules.data.nodes.eight.nand import Nand as Nand_8
from modules.data.nodes.eight.nor import Nor as Nor_8
from modules.data.nodes.eight.addr import Adder as Adder_8
from modules.data.nodes.eight.sub import Sub as Sub_8
from modules.data.nodes.eight.xor import Xor as Xor_8
from modules.data.nodes.eight.one import ONE as One_8
from modules.data.nodes.eight.mux import Mux as Mux_8

# Importations des nœuds mixtes (conversion et stockage)
from modules.data.nodes.mix.eight_breaker import Breaker as Breaker_8
from modules.data.nodes.mix.eight_maker import Maker as Maker_8
from modules.data.nodes.mix.register import Register

# Registre global de tous les types de portes
gate_types: Dict[str, Type[Any]] = {
    "AND": And,
    "NOT": Not,
    "OR": Or,
    "NAND": Nand,
    "NOR": Nor,
    "XOR": Xor,
    "CLK": Clock,
    "PASS": Pass,
    "Input": Input,
    "Output": Output,
    "ADDER": Adder,
    "SUB": Sub,
    "8NOT": Not_8,
    "8Input": Input_8,
    "8Output": Output_8,
    "8BREAK": Breaker_8,
    "8MAKER": Maker_8,
    "DLY": Delay,
    "8AND": And_8,
    "8OR": Or_8,
    "8NAND": Nand_8,
    "8NOR": Nor_8,
    "8ADDER": Adder_8,
    "8SUB": Sub_8,
    "8ONE": One_8,
    "8XOR": Xor_8,
    "ON": On,
    "OFF": Off,
    "TOR": TOr,
    "TAND": TAnd,
    "8MUX": Mux_8,
    "8REGISTER": Register,
}

# Registre spécifique aux composants 1-bit
gate_types_1: Dict[str, Type[Any]] = {
    "AND": And,
    "NOT": Not,
    "OR": Or,
    "NAND": Nand,
    "NOR": Nor,
    "XOR": Xor,
    "CLK": Clock,
    "PASS": Pass,
    "Input": Input,
    "Output": Output,
    "DLY": Delay,
    "ADDER": Adder,
    "SUB": Sub,
    "ON": On,
    "OFF": Off,
    "TOR": TOr,
    "TAND": TAnd,
}

# Registre spécifique aux composants 8-bits
gate_types_8: Dict[str, Type[Any]] = {
    "8NOT": Not_8,
    "8Input": Input_8,
    "8Output": Output_8,
    "8AND": And_8,
    "8OR": Or_8,
    "8NAND": Nand_8,
    "8NOR": Nor_8,
    "8ADDER": Adder_8,
    "8SUB": Sub_8,
    "8ONE": One_8,
    "8XOR": Xor_8,
    "8MUX": Mux_8,
}

# Registre pour les composants de conversion et les registres mixtes
gate_types_mix: Dict[str, Type[Any]] = {
    "8BREAK": Breaker_8, 
    "8MAKER": Maker_8,
    "8REGISTER": Register
}