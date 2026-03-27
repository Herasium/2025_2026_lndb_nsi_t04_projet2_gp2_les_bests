"""Vue de débogage de tous les jeux de tuiles (tilesets) présents dans le projet, utilisée lors de la création d'interfaces utilisateur."""

import logging

# Configuration du logger pour le suivi du débogage
logger = logging.getLogger(__name__)

class TilesetDebugView:
    """
    Une vue spécialisée pour inspecter et prévisualiser les ressources de tileset.
    
    Cette classe permet aux développeurs de parcourir visuellement les tuiles
    chargées afin de faciliter l'intégration de nouveaux éléments d'interface.
    """

    def __init__(self, tilesets):
        # Initialisation de la vue avec la liste des jeux de tuiles fournis
        self.tilesets = tilesets
        self.current_index = 0
        
        if not self.tilesets:
            # Lever une exception si aucun jeu de tuiles n'est trouvé dans le projet
            raise ValueError("Aucun jeu de tuiles n'a été chargé. Vérifiez le chemin des ressources.")

    def display_current_tileset(self):
        """Affiche le jeu de tuiles actuellement sélectionné dans la boucle principale."""
        try:
            tileset = self.tilesets[self.current_index]
            # Log de l'affichage pour le suivi en console
            print(f"Affichage du jeu de tuiles : {tileset.name}")
        except IndexError:
            # Gestion d'erreur au cas où l'index sortirait des limites des données
            logger.error("Échec de l'affichage : index du jeu de tuiles hors limites.")

    def next_tileset(self):
        """Passe au jeu de tuiles suivant dans la collection."""
        self.current_index = (self.current_index + 1) % len(self.tilesets)
        # Log informatif sur le changement d'état
        print(f"Passage à l'index de jeu de tuiles : {self.current_index}")