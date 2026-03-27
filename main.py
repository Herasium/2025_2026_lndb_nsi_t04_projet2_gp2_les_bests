"""
Point d'entrée de l'application Logic Box.

Ce module initialise les systèmes centraux du jeu, notamment la journalisation, 
le chargement des données et la gestion de la fenêtre principale, avant de 
lancer la vue initiale de l'interface utilisateur.
"""

from modules.ui.window import Window
from modules.ui.main_menu.in_progress_view import MainMenuView
from modules.data import data
from modules.data.loader import Loader
from modules.logger import Logger
import arcade

# Active la mesure des performances
arcade.enable_timings()

logger: Logger = Logger("Main")
loader: Loader = Loader()

logger.print(f"Logic Box, v.{data.VERSION}.")
logger.print(f"Chemin actuel : {data.current_path}")

try:
    data.load()
    logger.print("Préférences chargées.")
except Exception as e:
    logger.warning(f"Échec du chargement des préférences, retour aux valeurs par défaut. {e}")

windows: Window = Window()
data.window = windows
logger.print("Fenêtre créée.")

loader.load()

Main: MainMenuView = MainMenuView()
Pause: MainMenuView = MainMenuView(pause=True)

data.main = Main
data.pause = Pause

windows.display(Main)

# Lance la boucle principale de l'application
windows.run()