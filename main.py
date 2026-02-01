import pygame, random
from constantes import liste_fruits, liste_objets_speciaux, images, load_assets
import controller
from objets import Fruit, Glacon, Bombe
from interface import Bouton, dessiner_regles, dessiner_scores

# ============================================================================
# CLASSE : GestionnaireEcran
# ============================================================================
# Cette classe gère tout ce qui concerne l'affichage :
# - Le redimensionnement de la fenêtre
# - Le cache des fonds d'écran
# - L'affichage des fonds selon le mode de jeu
#
# POURQUOI UNE CLASSE ?
# - Regroupe les données (fonds, cache) et les actions (afficher, redimensionner)
# - Évite les variables globales (plus propre, moins de bugs)
# - Plus facile à comprendre : tout ce qui concerne l'écran est AU MÊME ENDROIT
# ============================================================================

class GestionnaireEcran:
    """
    Gère l'affichage des fonds d'écran avec mise en cache.
    
    Attributs:
        fond_1j (Surface): Image de fond pour le mode 1 joueur
        fond_2j_gauche (Surface): Image de fond pour J1 en mode 2 joueurs
        fond_2j_droite (Surface): Image de fond pour J2 en mode 2 joueurs
        cache_1j (Surface): Fond 1 joueur redimensionné (mis en cache)
        cache_2j_gauche (Surface): Fond J1 redimensionné (mis en cache)
        cache_2j_droite (Surface): Fond J2 redimensionné (mis en cache)
        derniere_taille (tuple): Dernière taille d'écran connue (largeur, hauteur)
    """
    
    def __init__(self):
        """
        Initialise le gestionnaire en chargeant les images de fond.
        
        Le constructeur (__init__) est appelé automatiquement quand on crée
        un objet avec : gestionnaire = GestionnaireEcran()
        """
        # ====================================================================
        # CHARGEMENT DES IMAGES DE FOND
        # ====================================================================
        try:
            # Fond pour le joueur 1 en mode 2 joueurs (côté gauche)
            self.fond_2j_gauche = pygame.image.load(
                "Assets/Images/Backgrounds/Background1.png"
            ).convert()
            
            # Fond pour le mode 1 joueur (plein écran)
            self.fond_1j = pygame.image.load(
                "Assets/Images/Backgrounds/Background2.png"
            ).convert()
            
            # Fond pour le joueur 2 en mode 2 joueurs (côté droit)
            self.fond_2j_droite = pygame.image.load(
                "Assets/Images/Backgrounds/Background3.png"
            ).convert()
            
            print("✅ Fonds d'écran chargés avec succès")
            
        except pygame.error as e:
            # Si les images n'existent pas, on crée des fonds colorés de secours
            print(f"⚠️ Erreur chargement fonds : {e}")
            print("📝 Création de fonds de secours...")
            
            self.fond_2j_gauche = pygame.Surface((100, 100))
            self.fond_2j_gauche.fill((100, 50, 50))  # Rouge sombre
            
            self.fond_1j = pygame.Surface((100, 100))
            self.fond_1j.fill((50, 50, 100))  # Bleu sombre
            
            self.fond_2j_droite = pygame.Surface((100, 100))
            self.fond_2j_droite.fill((50, 100, 50))  # Vert sombre
        
        # ====================================================================
        # INITIALISATION DU CACHE
        # ====================================================================
        # Ces variables stockeront les fonds redimensionnés
        # None = pas encore calculé
        self.cache_1j = None
        self.cache_2j_gauche = None
        self.cache_2j_droite = None
        
        # Dernière taille d'écran connue (pour détecter les changements)
        # (0, 0) = jamais calculé, forcera le premier calcul
        self.derniere_taille = (0, 0)
    
    def mettre_a_jour_cache(self, largeur, hauteur):
        """
        Recalcule les fonds redimensionnés si la taille de l'écran a changé.
        
        EXPLICATION POUR LES DÉBUTANTS :
        Cette méthode vérifie si l'écran a changé de taille.
        Si oui, elle redimensionne tous les fonds et les stocke en cache.
        Si non, elle ne fait rien (= optimisation !).
        
        Arguments:
            largeur (int): Largeur actuelle de l'écran en pixels
            hauteur (int): Hauteur actuelle de l'écran en pixels
        
        Retourne:
            bool: True si le cache a été mis à jour, False sinon
        """
        taille_actuelle = (largeur, hauteur)
        
        # Si la taille n'a pas changé, on ne fait rien
        if taille_actuelle == self.derniere_taille:
            return False  # Pas de mise à jour nécessaire
        
        # La taille a changé ! On recalcule tout
        print(f"🖼️ Redimensionnement des fonds pour {largeur}x{hauteur}")
        
        # Calcul du milieu (pour le mode 2 joueurs)
        milieu_x = largeur // 2
        
        # Redimensionnement du fond mode 1 joueur (plein écran)
        self.cache_1j = pygame.transform.scale(
            self.fond_1j, 
            (largeur, hauteur)
        )
        
        # Redimensionnement du fond J1 (moitié gauche)
        self.cache_2j_gauche = pygame.transform.scale(
            self.fond_2j_gauche, 
            (milieu_x, hauteur)
        )
        
        # Redimensionnement du fond J2 (moitié droite)
        # Note : largeur - milieu_x gère le cas où la largeur est impaire
        self.cache_2j_droite = pygame.transform.scale(
            self.fond_2j_droite, 
            (largeur - milieu_x, hauteur)
        )
        
        # Mémorise la taille actuelle pour la prochaine comparaison
        self.derniere_taille = taille_actuelle
        
        return True  # Le cache a été mis à jour
    
    def afficher_fond(self, screen, nombre_de_joueurs, font_info):
        """
        Affiche le fond approprié selon le mode de jeu.
        
        Cette méthode :
        1. Met à jour le cache si nécessaire
        2. Affiche le bon fond selon qu'on est en mode 1 ou 2 joueurs
        3. Affiche les labels des joueurs
        
        Arguments:
            screen (Surface): L'écran Pygame sur lequel dessiner
            nombre_de_joueurs (int): 1 ou 2
            font_info (Font): Police pour les textes d'information
        
        Retourne:
            int: La position X du milieu de l'écran (utile pour le reste du jeu)
        """
        largeur = screen.get_width()
        hauteur = screen.get_height()
        milieu_x = largeur // 2
        
        # Étape 1 : S'assurer que le cache est à jour
        self.mettre_a_jour_cache(largeur, hauteur)
        
        # Étape 2 : Afficher le fond selon le mode
        if nombre_de_joueurs == 1:
            # ----------------------------------------------------------------
            # MODE 1 JOUEUR : Fond plein écran
            # ----------------------------------------------------------------
            screen.blit(self.cache_1j, (0, 0))
            
            # Texte d'instruction centré en haut
            txt_info = font_info.render("Clavier ou Souris", True, (255, 255, 255))
            screen.blit(txt_info, (largeur // 2 - txt_info.get_width() // 2, 20))
        
        else:
            # ----------------------------------------------------------------
            # MODE 2 JOUEURS : Deux fonds côte à côte
            # ----------------------------------------------------------------
            # Fond gauche (Joueur 1)
            screen.blit(self.cache_2j_gauche, (0, 0))
            
            # Fond droit (Joueur 2)
            screen.blit(self.cache_2j_droite, (milieu_x, 0))
            
            # Ligne de séparation blanche
            pygame.draw.line(
                screen, 
                (255, 255, 255),      # Couleur blanche
                (milieu_x, 0),         # Point de départ (haut)
                (milieu_x, hauteur),   # Point d'arrivée (bas)
                3                      # Épaisseur en pixels
            )
            
            # Labels des joueurs
            txt_j1 = font_info.render("J1 (Clavier)", True, (255, 255, 255))
            txt_j2 = font_info.render("J2 (Souris)", True, (255, 255, 255))
            
            # Centrage des labels dans chaque moitié
            screen.blit(txt_j1, (milieu_x // 2 - txt_j1.get_width() // 2, 20))
            screen.blit(txt_j2, (milieu_x + milieu_x // 2 - txt_j2.get_width() // 2, 20))
        
        # Retourne le milieu pour que le reste du code puisse l'utiliser
        return milieu_x

# INITIALISATION
pygame.init()
L_ecran = 1280
H_ecran = 720
screen = pygame.display.set_mode((L_ecran, H_ecran), pygame.RESIZABLE)
pygame.display.set_caption("Fruit Slicer")
clock = pygame.time.Clock()
load_assets()

# Police pour le titre principal "FRUIT SLICER" (très grande)
font_titre = pygame.font.Font(None, 80)

# Police pour les informations générales (moyenne)
font_info = pygame.font.Font(None, 40)

# Police pour afficher les vies et le niveau (moyenne-grande)
font_vies = pygame.font.Font(None, 50)

# Police pour l'écran Game Over (grande)
font_game_over = pygame.font.Font(None, 80)

# Police pour les messages secondaires sur l'écran Game Over
font_raison = pygame.font.Font(None, 40)

# Police pour l'effet FREEZE (très grande pour être bien visible)
font_freeze = pygame.font.Font(None, 120)

# Police pour le timer du freeze
font_timer = pygame.font.Font(None, 80)

# Police pour le texte du décompte "Le jeu démarre dans"
font_phrase = pygame.font.Font(None, 45)

# Police pour les gros chiffres du décompte (3, 2, 1)
font_chrono = pygame.font.Font(None, 150)

# ============================================================================
# CRÉATION DU GESTIONNAIRE D'ÉCRAN
# ============================================================================
# On crée UN SEUL objet qui gère tout l'affichage des fonds
# ============================================================================
gestionnaire_ecran = GestionnaireEcran()

# --- ETAT DU JEU ---
etat_jeu = "menu" 
nombre_de_joueurs = 1
start_ticks = 0 

# NOUVEAU : Vies séparées
vies_j1 = 3
vies_j2 = 3

screen_center_x = L_ecran // 2
bouton_1j = Bouton(screen_center_x - 150, 150, 300, 60, "1 Joueur", (0, 100, 0), (0, 150, 0))
bouton_2j = Bouton(screen_center_x - 150, 230, 300, 60, "2 Joueurs", (0, 0, 100), (0, 0, 150))
bouton_regles = Bouton(screen_center_x - 150, 310, 300, 60, "Comment jouer", (100, 100, 0), (150, 150, 0))
bouton_scores = Bouton(screen_center_x - 150, 390, 300, 60, "Scores", (100, 0, 100), (150, 0, 150))
bouton_quitter = Bouton(screen_center_x - 150, 550, 300, 60, "Quitter", (100, 0, 0), (150, 0, 0))
bouton_retour = Bouton(20, 20, 150, 50, "Retour", (50, 50, 50), (100, 100, 100))
bouton_menu_go = Bouton(0, 0, 300, 60, "Menu Principal", (100, 100, 100), (150, 150, 150))

# Variables de jeu
mes_fruits = [] 
frequence_lancer = random.randint(30, 100)
compteur = 0
running = True
niveau = 1
score = 0
gravite_actuelle = 0.4
freeze_actif = False
freeze_timer = 0
freeze_duree = 0 # sera défini aléatoirement entre 3 et 5 secondes
is_bomb_exploded = False

# Gestion du son
try:
    # Un seul fichier qui contient "3... 2... 1... GO!"
    son_decompte = pygame.mixer.Sound("Assets/Sounds/decompte_complet.wav")
    son_decompte.set_volume(0.6)
except (pygame.error, FileNotFoundError):
    print("Son manquant, création d'un son vide.")
    son_decompte = pygame.mixer.Sound(buffer=bytearray())

# --- BOUCLE PRINCIPALE ---
while running: 
    
    # 0. RE-CENTRAGE DYNAMIQUE
    largeur_actuelle = screen.get_width()
    centre_x = largeur_actuelle // 2
    
    bouton_1j.rect.centerx = centre_x
    bouton_2j.rect.centerx = centre_x
    bouton_regles.rect.centerx = centre_x
    bouton_scores.rect.centerx = centre_x
    bouton_quitter.rect.centerx = centre_x
    bouton_menu_go.rect.centerx = centre_x
    bouton_menu_go.rect.y = screen.get_height() // 2 + 120

    # 1. GESTION DES ÉVÉNEMENTS
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f or event.key == pygame.K_F11:
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        if etat_jeu == "menu":
            if bouton_1j.est_clique(event):
                nombre_de_joueurs = 1
                etat_jeu = "jeu"
                mes_fruits = []
                # Réinitialisation
                vies_j1 = 3 
                start_ticks = pygame.time.get_ticks() 
                
                # Reset des variables de niveau pour un nouveau jeu
                niveau = 1
                score = 0
                gravite_actuelle = 0.4 
                
                # Reset du freeze
                freeze_actif = False
                freeze_timer = 0
                is_bomb_exploded = False

                son_decompte.stop() # Coupe le son s'il jouait déjà
                son_decompte.play()
                
            if bouton_2j.est_clique(event):
                nombre_de_joueurs = 2
                etat_jeu = "jeu"
                mes_fruits = []
                # Réinitialisation des DEUX joueurs
                vies_j1 = 3
                vies_j2 = 3
                # Réinitialision du score
                score = 0
                start_ticks = pygame.time.get_ticks()
                
                # Reset du freeze
                freeze_actif = False
                freeze_timer = 0
                is_bomb_exploded = False
                son_decompte.stop() # Coupe le son s'il jouait déjà
                son_decompte.play()

            if bouton_regles.est_clique(event): etat_jeu = "regles"
            if bouton_scores.est_clique(event): etat_jeu = "scores"
            if bouton_quitter.est_clique(event): running = False

        elif etat_jeu in ["regles", "scores"]:
            if bouton_retour.est_clique(event): etat_jeu = "menu"
        
        elif etat_jeu == "game_over":
            if bouton_menu_go.est_clique(event):
                etat_jeu = "menu"

        elif etat_jeu == "jeu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                etat_jeu = "menu"
                mes_fruits = [] 
                son_decompte.stop()

            seconds_ecoules = (pygame.time.get_ticks() - start_ticks) / 1000
            
            if seconds_ecoules > 3:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    controller.start_slice(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONUP:
                    controller.end_slice(mes_fruits, screen.get_width(), nombre_de_joueurs)
                if event.type == pygame.KEYDOWN:
                    result = controller.handle_keyboard_inputs(mes_fruits, screen.get_width(), screen.get_height(), event.key, nombre_de_joueurs)
                    if result == "game_over":
                        etat_jeu = "game_over"
                        is_bomb_exploded = True
                        print("BOOM ! Bombe tranchée au clavier !")
                    elif result == "freeze":
                        freeze_actif = True
                        freeze_duree = random.randint(3, 5)
                        freeze_timer = freeze_duree * 60
                        print(f"❄️ FREEZE activé au clavier pour {freeze_duree} secondes !")

    # 2. LOGIQUE ET DESSIN
    
    if etat_jeu == "menu":
        screen.fill((30, 30, 40))
        titre = font_titre.render("FRUIT SLICER", True, (255, 100, 100))
        screen.blit(titre, (screen.get_width()//2 - titre.get_width()//2, 50))
        bouton_1j.dessiner(screen)
        bouton_2j.dessiner(screen)
        bouton_regles.dessiner(screen)
        bouton_scores.dessiner(screen)
        bouton_quitter.dessiner(screen)

    elif etat_jeu == "regles":
        dessiner_regles(screen)
        bouton_retour.dessiner(screen)
        
    elif etat_jeu == "scores":
        dessiner_scores(screen)
        bouton_retour.dessiner(screen)

    # --- ÉCRAN GAME OVER (LOGIQUE MODIFIÉE) ---
    elif etat_jeu == "game_over":
    
        screen.fill((20, 0, 0)) # Fond rouge sombre général
    
        milieu_x = screen.get_width() // 2
    
        if is_bomb_exploded:
            # Affichage centré pour bombe explosée
            txt_go = font_game_over.render("GAME OVER", True, (255, 0, 0))
            txt_boom = font_game_over.render("💥 BOOM !", True, (255, 255, 0))
            txt_egalite = font_raison.render("Égalité ! Les deux joueurs ont perdu simultanément.", True, (200, 200, 200))
            
            screen.blit(txt_go, (screen.get_width()//2 - txt_go.get_width()//2, screen.get_height()//2 - 100))
            screen.blit(txt_boom, (screen.get_width()//2 - txt_boom.get_width()//2, screen.get_height()//2 - 20))
            screen.blit(txt_egalite, (screen.get_width()//2 - txt_egalite.get_width()//2, screen.get_height()//2 + 40))
        else:
            # Ligne de séparation pour garder la cohérence visuelle
            if nombre_de_joueurs == 2:
                pygame.draw.line(screen, (100, 0, 0), (milieu_x, 0), (milieu_x, screen.get_height()), 2)
            
            txt_go = font_game_over.render("GAME OVER", True, (255, 0, 0))
            txt_perdu = font_raison.render("Vous avez perdu !", True, (200, 200, 200))
            txt_gagne = font_game_over.render("VAINQUEUR !", True, (0, 255, 0))

            if nombre_de_joueurs == 1:
                # Affichage classique centré
                screen.blit(txt_go, (screen.get_width()//2 - txt_go.get_width()//2, screen.get_height()//2 - 100))
            else:
                # --- LOGIQUE GAME OVER 2 JOUEURS ---
                
                # Affichage pour le Joueur 1 (Gauche)
                if vies_j1 <= 0:
                    # J1 a perdu
                    screen.blit(txt_go, (milieu_x//2 - txt_go.get_width()//2, screen.get_height()//2 - 100))
                    screen.blit(txt_perdu, (milieu_x//2 - txt_perdu.get_width()//2, screen.get_height()//2 - 20))
                else:
                    # J1 a gagné (car le jeu s'arrête si l'un perd)
                    screen.blit(txt_gagne, (milieu_x//2 - txt_gagne.get_width()//2, screen.get_height()//2 - 100))

                # Affichage pour le Joueur 2 (Droite)
                if vies_j2 <= 0:
                    # J2 a perdu
                    screen.blit(txt_go, (milieu_x + milieu_x//2 - txt_go.get_width()//2, screen.get_height()//2 - 100))
                    screen.blit(txt_perdu, (milieu_x + milieu_x//2 - txt_perdu.get_width()//2, screen.get_height()//2 - 20))
                else:
                    # J2 a gagné
                    screen.blit(txt_gagne, (milieu_x + milieu_x//2 - txt_gagne.get_width()//2, screen.get_height()//2 - 100))

        bouton_menu_go.dessiner(screen)

    # --- ÉCRAN DE JEU ---
    elif etat_jeu == "jeu":
        
        seconds_ecoules = (pygame.time.get_ticks() - start_ticks) / 1000
        en_attente = seconds_ecoules < 3  

        # --- LOGIQUE ---
        if not en_attente:
            # Gestion du freeze
            if freeze_actif:
                freeze_timer -= 1
                if freeze_timer <= 0:
                    freeze_actif = False
                    print("Effet de freeze terminé.")
            
            # Gestion de la souris
            if controller.slicing:
                result = controller.update_slice(pygame.mouse.get_pos(), mes_fruits, screen.get_width(), nombre_de_joueurs)
    
                # --- TRAITEMENT DU RÉSULTAT ---
                if result == "game_over":
                    # La bombe a été tranchée : partie terminée
                    etat_jeu = "game_over"
                    print("BOOM ! Bombe tranchée !")
    
                elif result == "freeze":
                    # Le glaçon a été tranché : activation du freeze
                    freeze_actif = True
                    freeze_duree = random.randint(3, 5)  # Entre 3 et 5 secondes
                    freeze_timer = freeze_duree * 60  # Conversion en frames (60 FPS)
                    print(f"❄️ FREEZE activé pour {freeze_duree} secondes !")

                elif result == 1:  # Point marqué
                    if nombre_de_joueurs == 1:
                        score += 1
                        # Gestion de la montée de niveau tous les 10 points
                        if score > 0 and score % 10 == 0:
                            niveau += 1
                            # Augmentation de la gravité
                            gravite_actuelle = (min(0.4 + (niveau - 1) * 0.03, 1.0))
            compteur += 1
            
            # Ajustement de la fréquence en fonction du niveau (uniquement en mode 1 joueur)
            if nombre_de_joueurs == 1:
                min_freq = max(20, 50 - (niveau - 1) * 2)  # Fréquence minimale diminue avec le niveau
                max_freq = max(40, 150 - (niveau - 1) * 3)  # Maximale aussi
            else:
                min_freq = 30  # Valeurs par défaut pour mode 2 joueurs
                max_freq = 100
            if compteur >= frequence_lancer:
                # Gestion de la zone (2 joueurs ou non)
                if nombre_de_joueurs == 2:
                    zone_joueur = random.choice([1, 2])
                else:
                    zone_joueur = None
                
                # Gravité selon le mode
                gravite_pour_objet = gravite_actuelle if nombre_de_joueurs == 1 else 0.4
                
                # --- 30% DE CHANCE D'OBJET SPÉCIAL (BOMBE OU ICE) ---
                if random.randint(1, 100) <= 30:
                    # Choix aléatoire entre bombe et ice
                    type_special = random.choice(liste_objets_speciaux)
                    
                    if type_special == "bombe":
                        mes_fruits.append(Bombe(screen.get_width(), screen.get_height(), zone_joueur, gravite_pour_objet))
                        print("💣 Bombe apparue !")
                    else:  # type_special == "ice"
                        mes_fruits.append(Glacon(screen.get_width(), screen.get_height(), zone_joueur, gravite_pour_objet))
                        print("❄️ Glaçon apparu !")
                else:
                    # 70% : Fruit normal
                    type_fruit = random.choice(liste_fruits)
                    mes_fruits.append(Fruit(type_fruit, screen.get_width(), screen.get_height(), zone_joueur, gravite_pour_objet))
                
                compteur = 0
                frequence_lancer = random.randint(min_freq, max_freq)

        # --- DESSIN ---
        largeur_ecran = screen.get_width()
        hauteur_ecran = screen.get_height()
        milieu_x = gestionnaire_ecran.afficher_fond(screen, nombre_de_joueurs, font_info)

        # --- GESTION FRUITS ET VIES SÉPARÉES ---
        for f in mes_fruits[:]:
            if not en_attente:
                # Les fruits ne bougent que si pas de freeze actif
                if not freeze_actif:
                    f.update(screen.get_width())
            f.draw(screen)

            # --- DÉTECTION FRUIT RATÉ ---
            if f.y > screen.get_height() + 50: 
                mes_fruits.remove(f)
                
                if not f.sliced and not en_attente:
                    if nombre_de_joueurs == 1:
                        # Mode 1 joueur : on utilise vies_j1 par défaut
                        vies_j1 -= 1
                        if vies_j1 <= 0:
                            etat_jeu = "game_over"
                    else:
                        # Mode 2 joueurs : on regarde le côté
                        if f.x < milieu_x:
                            # C'est un fruit de GAUCHE (Joueur 1)
                            vies_j1 -= 1
                            print(f"J1 a raté ! Vies restantes : {vies_j1}")
                        else:
                            # C'est un fruit de DROITE (Joueur 2)
                            vies_j2 -= 1
                            print(f"J2 a raté ! Vies restantes : {vies_j2}")
                        
                        # Si l'un des deux meurt, c'est Game Over global
                        if vies_j1 <= 0 or vies_j2 <= 0:
                            etat_jeu = "game_over"

        if not en_attente:
            controller.draw_slice(screen)

        # --- AFFICHAGE DES VIES (HUD) ---
        
        if nombre_de_joueurs == 1:
            txt_vies = font_vies.render(f"VIES : {vies_j1}", True, (255, 0, 0))
            screen.blit(txt_vies, (largeur_ecran // 2 - txt_vies.get_width() // 2, 70))
            txt_niveau = font_vies.render(f"NIVEAU : {niveau}", True, (255, 255, 0))
            screen.blit(txt_niveau, (largeur_ecran // 2 - txt_niveau.get_width() // 2, 120))
        else:
            # Vies J1 (Gauche)
            txt_vies_j1 = font_vies.render(f"VIES : {vies_j1}", True, (255, 0, 0))
            screen.blit(txt_vies_j1, (milieu_x // 2 - txt_vies_j1.get_width() // 2, 70))
            
            # Vies J2 (Droite)
            txt_vies_j2 = font_vies.render(f"VIES : {vies_j2}", True, (255, 0, 0))
            screen.blit(txt_vies_j2, (milieu_x + milieu_x // 2 - txt_vies_j2.get_width() // 2, 70))
            
        # --- AFFICHAGE DU FREEZE ---
        if freeze_actif:
            # Overlay semi-transparent bleu
            overlay = pygame.Surface((largeur_ecran, hauteur_ecran))
            overlay.set_alpha(50)  # Transparence
            overlay.fill((0, 200, 255))  # Bleu clair
            screen.blit(overlay, (0, 0))
            
            # Message "FREEZE" avec temps restant
            temps_restant = freeze_timer / 60  # Conversion frames -> secondes
            txt_freeze = font_freeze.render(f"❄️ FREEZE", True, (0, 255, 255))
            
            txt_timer = font_timer.render(f"{temps_restant:.1f}s", True, (255, 255, 255))
            
            # Effet de clignotement pour le message
            if (freeze_timer // 15) % 2 == 0:  # Clignote toutes les 15 frames
                screen.blit(txt_freeze, (largeur_ecran//2 - txt_freeze.get_width()//2, hauteur_ecran//2 - 80))
            
            screen.blit(txt_timer, (largeur_ecran//2 - txt_timer.get_width()//2, hauteur_ecran//2 + 20))


        # --- DÉCOMPTE DÉBUT DE JEU ---
        if en_attente:
            chiffre = int(4 - seconds_ecoules)
            
            surf_phrase = font_phrase.render("Le jeu démarre dans", True, (255, 255, 255))
            surf_chrono = font_chrono.render(str(chiffre), True, (255, 215, 0))
            
            if nombre_de_joueurs == 1:
                rect_phrase = surf_phrase.get_rect(center=(largeur_ecran//2, hauteur_ecran//2 - 60))
                rect_chrono = surf_chrono.get_rect(center=(largeur_ecran//2, hauteur_ecran//2 + 40))
                screen.blit(surf_phrase, rect_phrase)
                screen.blit(surf_chrono, rect_chrono)
            else:
                rect_phrase_j1 = surf_phrase.get_rect(center=(milieu_x//2, hauteur_ecran//2 - 60))
                rect_chrono_j1 = surf_chrono.get_rect(center=(milieu_x//2, hauteur_ecran//2 + 40))
                rect_phrase_j2 = surf_phrase.get_rect(center=(milieu_x + milieu_x//2, hauteur_ecran//2 - 60))
                rect_chrono_j2 = surf_chrono.get_rect(center=(milieu_x + milieu_x//2, hauteur_ecran//2 + 40))
                
                screen.blit(surf_phrase, rect_phrase_j1)
                screen.blit(surf_chrono, rect_chrono_j1)
                screen.blit(surf_phrase, rect_phrase_j2)
                screen.blit(surf_chrono, rect_chrono_j2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()