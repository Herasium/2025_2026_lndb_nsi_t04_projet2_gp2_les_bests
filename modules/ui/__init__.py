"""
Ce module gère l'interface utilisateur principale et la boucle d'exécution de l'application.
Il initialise les composants du système, traite les entrées de l'utilisateur et assure
la transition fluide entre les différents états du programme.
"""

import logging

# Configuration du logger pour le suivi des événements du système
logger = logging.getLogger(__name__)

class MainMenuView:
    def __init__(self, settings):
        """
        Initialise la vue du menu principal avec les paramètres fournis.
        
        :param settings: Dictionnaire contenant les configurations de l'interface.
        """
        self.settings = settings
        # Indicateur pour suivre l'état d'affichage du menu
        self.is_visible = False

    def display(self):
        """Affiche le menu principal à l'utilisateur."""
        try:
            self.is_visible = True
            print("Bienvenue dans l'application.")
            logger.info("Le menu principal a été affiché avec succès.")
        except Exception as e:
            # Erreur lors de la tentative de rendu de l'interface
            logger.error(f"Échec de l'affichage du menu : {e}")
            raise RuntimeError("Impossible de charger l'interface utilisateur.")

    def handle_input(self, user_input):
        """
        Traite les commandes saisies par l'utilisateur.
        
        :param user_input: La chaîne de caractères saisie par l'utilisateur.
        """
        if not user_input:
            # Cas où l'utilisateur soumet une entrée vide
            print("L'entrée ne peut pas être vide.")
            return

        logger.info(f"Traitement de l'entrée utilisateur : {user_input}")
        
        # Logique de navigation simple
        if user_input.lower() == "quitter":
            self.close()
        else:
            print(f"Commande '{user_input}' non reconnue.")

    def close(self):
        """Ferme proprement la vue du menu et libère les ressources."""
        self.is_visible = False
        logger.info("Fermeture du menu principal.")

def run_application():
    """Démarre la boucle principale de l'application."""
    config = {"theme": "sombre", "debug": True}
    app = MainMenuView(config)
    
    # Déclenchement de la routine d'affichage initiale
    app.display()

    # Début de la boucle de capture des événements
    while app.is_visible:
        command = input("> ")
        app.handle_input(command)

if __name__ == "__main__":
    run_application()