from modules.data.nodes.gand import And
from modules.data.nodes.gnot import Not
from modules.data.nodes.gor import Or
from modules.data.nodes.nand import Nand
from modules.data.nodes.nor import Nor
from modules.data.nodes.xor import Xor
from modules.data.nodes.clock import Clock
from modules.data.nodes.gpass import Pass
from modules.data.nodes.input import Input
from modules.data.nodes.output import Output

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
    "Output": Output
}