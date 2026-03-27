"""
Ce module gère l'interface utilisateur du menu principal pour l'application.
Il initialise les composants graphiques et gère les interactions de l'utilisateur
pour naviguer vers différentes sections de l'outil.
"""

import logging

# Configuration du logger pour le suivi des erreurs et des informations
logger = logging.getLogger(__name__)

class MainMenuView:
    def __init__(self, controller):
        """
        Initialise la vue du menu principal avec un contrôleur.
        
        :param controller: L'objet contrôleur qui gère la logique métier.
        """
        self.controller = controller
        # Initialisation de l'état de l'affichage
        self.is_visible = False
        logger.info("Initialisation de MainMenuView terminée.")

    def show(self):
        """Affiche le menu principal à l'utilisateur."""
        try:
            self.is_visible = True
            # Logique pour restituer l'interface utilisateur
            print("Affichage du menu principal...")
        except Exception as e:
            logger.error(f"Échec de l'affichage du menu principal : {e}")
            raise RuntimeError("Une erreur est survenue lors du rendu de l'interface utilisateur.")

    def on_button_click(self, button_id):
        """
        Gère les événements de clic sur les boutons du menu.
        
        :param button_id: L'identifiant unique du bouton cliqué.
        """
        # Journalisation de l'interaction pour le débogage
        logger.debug(f"Bouton cliqué : {button_id}")

        if button_id == "start_game":
            # Lancer la boucle principale du jeu
            self.controller.start_session()
        elif button_id == "settings":
            # Ouvrir le panneau de configuration des paramètres
            self.controller.open_settings()
        else:
            # Cas de repli si l'ID du bouton n'est pas reconnu
            logger.warning(f"ID de bouton inconnu reçu : {button_id}")

    def close(self):
        """Ferme le menu principal et nettoie les ressources."""
        self.is_visible = False
        logger.info("Fermeture du menu principal.")