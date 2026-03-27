
import sys

class MainMenuView:
    """
    Gère l'affichage et les interactions de l'interface utilisateur pour le menu principal.
    Cette classe est responsable du rendu des boutons, du texte et de la capture des 
    événements utilisateur au démarrage de l'application.
    """

    def __init__(self, screen, assets):
        # Initialise la vue avec l'écran de rendu et les ressources chargées
        self.screen = screen
        self.assets = assets
        self.font = pygame.font.Font(None, 74)
        self.menu_active = True

    def draw_menu(self):
        # Affiche le titre du menu sur l'écran
        title_text = self.font.render("Menu Principal", True, (255, 255, 255))
        self.screen.blit(title_text, (250, 100))

        # Affiche les instructions pour l'utilisateur
        start_text = self.font.render("Appuyez sur ENTRÉE pour Jouer", True, (200, 200, 200))
        self.screen.blit(start_text, (150, 300))

    def handle_input(self):
        # Gère les entrées clavier et les événements système
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quitte l'application de manière sécurisée
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Désactive le menu pour lancer le jeu
                    self.menu_active = False

    def run(self):
        # Boucle principale de la vue du menu
        while self.menu_active:
            self.handle_input()
            self.screen.fill((0, 0, 0))  # Efface l'écran avec une couleur noire
            self.draw_menu()
            pygame.display.flip()  # Met à jour l'affichage de la fenêtre