"""Interface de liste des niveaux, utilisée lors de l'appui sur « niveaux » dans le menu principal."""

import logging

# Configuration du logger pour le suivi de l'interface utilisateur
logger = logging.getLogger(__name__)

class LevelListView:
    """
    Gère l'affichage et la logique de sélection des niveaux pour l'utilisateur.
    """

    def __init__(self, levels_data):
        # Initialisation de la vue avec les données de niveaux fournies
        self.levels_data = levels_data
        logger.info("Initialisation de LevelListView avec les données de niveaux.")

    def render(self):
        """Affiche la liste des niveaux à l'écran."""
        try:
            # Logique pour générer les boutons de niveaux dans la boucle principale
            print("Affichage du menu des niveaux...")
        except Exception as e:
            logger.error(f"Échec du rendu de la liste des niveaux : {e}")
            raise RuntimeError("Une erreur est survenue lors du chargement de l'interface des niveaux.")

    def on_level_select(self, level_id):
        """Gère l'événement de sélection d'un niveau par l'utilisateur."""
        if level_id not in self.levels_data:
            logger.warning(f"Tentative d'accès à un ID de niveau invalide : {level_id}")
            return False
        
        # Charger le niveau sélectionné
        logger.info(f"Niveau {level_id} sélectionné par l'utilisateur.")
        return True