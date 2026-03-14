
#1 bit
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

#8 Bit
from modules.data.nodes.eight.gnot import Not as Not_8
from modules.data.nodes.eight.input import Input as Input_8
from modules.data.nodes.eight.output import Output as Output_8

#Mix
from modules.data.nodes.mix.eight_breaker import Breaker as Breaker_8
from modules.data.nodes.mix.eight_maker import Maker as Maker_8

gate_types = {
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
    "8NOT": Not_8,
    "8Input": Input_8,
    "8Output": Output_8,
    "8BREAK": Breaker_8,
    "8MAKER": Maker_8,
}

gate_types_1 = {
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
}
gate_types_8 = {
    "8NOT": Not_8,
    "8Input": Input_8,
    "8Output": Output_8,
}
gate_types_mix = {
    "8BREAK": Breaker_8,
    "8MAKER": Maker_8
}
