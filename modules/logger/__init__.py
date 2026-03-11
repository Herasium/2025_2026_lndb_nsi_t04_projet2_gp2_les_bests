
#  Imports
# -------------------------------------------------
from modules.data import data # Global Shared Data
import datetime
# -------------------------------------------------

# Logger: Basic logger to help debug and display critical informations.
# Display messages with a color code for easy debuging.
# Takes as input the name of the process (Loader, Main...)

class Logger():

    def __init__(self,name: str):
        self.name = name

        self.levels = [ # 5 severities of messages, each with a header (0: Debug - 4: Error)
            "DEBUG", #Low level info, often temporary
            "INFO", #Basic infomations, startup notice, version etc..
            "SUCCESS", #Launch of a new part of the code (MainMenu etc..)
            "WARNING", #Non critical errors, todos...
            "ERROR" # Fatal errors, that will result in a game crash / freeze.
        ]

        self.colors = [ # Each severity is displayed as a color coded message in the ANSI Escape Code format.
            "\033[0m", #Default Debug
            "\033[36m", #Cyan Info
            "\033[92m", #Bright Green Success
            "\033[33m", #Yellow Warning
            "\033[31m", #Red Error
        ]

        self.history = [] #Saved message history, to save in file if needed.

    def _header(self,level:int) -> str: #First part of the message, containing the severity and the color, as well as the process that sent the message and a timestamp for good measure.
        timstamp = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")
        header = f"{self.colors[level]}LogicBox v.{data.VERSION} | {self.name} | {timstamp} | {self.levels[level]} | "
        # Result Example: LogicBox v.136 | Loader | 17:12:55.200927 | SUCCESS | (all in bright green)
        return header

    # A function per severity, for quick access an readability when using the class.
    # Each add the message to the header, with the according severity, and saves + prints the resulting message.
    # A default ANSI Escape code is added at the end of each message, to reset the console color, in case of prints by other methods (imports, of forgotten print())

    def debug(self,message:str) -> None: 
        data = f"{self._header(0)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data) 
        

    def print(self,message:str) -> None: #INFO
        data = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def info(self,message:str) -> None: #INFO
        data = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def success(self,message:str) -> None:
        data = f"{self._header(2)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def warning(self,message:str) -> None:
        data = f"{self._header(3)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)
    
    def error(self,message:str) -> None:
        data = f"{self._header(4)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)