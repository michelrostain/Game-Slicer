import pygame, random
from constantes import liste_fruits, liste_objets_speciaux, load_assets
import controller
from objets import Fruit, Glacon, Bombe, ParticuleExplosion, ParticuleGlace
from interface import Bouton, dessiner_regles, dessiner_scores
from scores import (
    creer_fichier_scores_si_absent,
    sauvegarder_score,
    reinitialiser_scores,
    charger_scores,
    obtenir_statistiques,
    est_nouveau_record
)

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
            # Fond pour le menu et le game over
            self.fond_menu = pygame.image.load(
                "Assets/Images/Backgrounds/Background0.png"
            ).convert()

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

            self.fond_menu = pygame.Surface((100, 100))
            self.fond_menu.fill((30, 30, 40))  # Gris foncé pour le menu

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
        self.cache_menu = None
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

        # Redimensionnement du fond menu/game over (plein écran)
        self.cache_menu = pygame.transform.scale(self.fond_menu, (largeur, hauteur))

        # Redimensionnement du fond mode 1 joueur (plein écran)
        self.cache_1j = pygame.transform.scale(self.fond_1j, (largeur, hauteur))

        # Redimensionnement du fond J1 (moitié gauche)
        self.cache_2j_gauche = pygame.transform.scale(
            self.fond_2j_gauche, (milieu_x, hauteur)
        )

        # Redimensionnement du fond J2 (moitié droite)
        # Note : largeur - milieu_x gère le cas où la largeur est impaire
        self.cache_2j_droite = pygame.transform.scale(
            self.fond_2j_droite, (largeur - milieu_x, hauteur)
        )

        # Mémorise la taille actuelle pour la prochaine comparaison
        self.derniere_taille = taille_actuelle

        return True  # Le cache a été mis à jour

    def afficher_fond_menu(self, screen):
        """
        Affiche le fond pour le menu principal et l'écran game over.

        Arguments:
            screen (Surface): L'écran Pygame sur lequel dessiner
        """
        largeur = screen.get_width()
        hauteur = screen.get_height()

        # S'assurer que le cache est à jour
        self.mettre_a_jour_cache(largeur, hauteur)

        # Afficher le fond
        screen.blit(self.cache_menu, (0, 0))

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
                (101, 67, 33),  # Couleur marron foncé
                (milieu_x, 0),  # Point de départ (haut)
                (milieu_x, hauteur),  # Point d'arrivée (bas)
                4,  # Épaisseur en pixels
            )

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
creer_fichier_scores_si_absent()

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
# PALETTE DE COULEURS (thème fruits/nature)
# ============================================================================
# Couleurs adaptées au background avec les fruits
# ============================================================================
COULEURS = {
    # Textes principaux (contrastés pour le fond clair)
    "titre": (139, 69, 19),  # Marron bois (SaddleBrown)
    "titre_ombre": (101, 67, 33),  # Marron foncé pour ombre
    # Game Over
    "game_over": (178, 34, 34),  # Rouge foncé (FireBrick)
    "boom": (255, 140, 0),  # Orange vif (DarkOrange)
    "message": (85, 107, 47),  # Vert olive (DarkOliveGreen)
    "score_final": (139, 69, 19),  # Marron
    # Gagnant / Perdant
    "gagnant": (34, 139, 34),  # Vert forêt (ForestGreen)
    "perdant": (178, 34, 34),  # Rouge foncé
    "egalite": (255, 140, 0),  # Orange
    # HUD pendant le jeu (sur fond clair)
    "hud_instruction": (101, 67, 33),  # Marron foncé (remplace blanc)
    "hud_vies": (192, 57, 43),  # Rouge pomme
    "hud_niveau": (230, 126, 34),  # Orange
    "hud_score": (139, 69, 19),  # Marron
    "vies": (192, 57, 43),  # Rouge pomme
    "niveau": (230, 126, 34),  # Orange
    "score": (139, 69, 19),  # Marron
    # Décompte
    "decompte_texte": (85, 107, 47),  # Vert olive
    "decompte_chiffre": (255, 140, 0),  # Orange vif
    # Freeze
    "freeze_texte": (0, 102, 153),  # Bleu océan
    "freeze_timer": (0, 51, 102),  # Bleu foncé
    # Labels joueurs
    "label_j1": (34, 120, 69),  # Vert forêt
    "label_j2": (192, 57, 43),  # Rouge pomme
}

# On crée UN SEUL objet qui gère tout l'affichage des fonds
gestionnaire_ecran = GestionnaireEcran()

# --- ETAT DU JEU ---
etat_jeu = "menu"
nombre_de_joueurs = 1
start_ticks = 0

# NOUVEAU : Vies séparées
vies_j1 = 3
vies_j2 = 3

# Variables pour la saisie du nom du joueur (si nouveau record)
nom_joueur = ""
saisie_nom_active = False
score_sauvegarde = False

# Variables pour l'animation d'explosion
explosion_en_cours = False
explosion_timer = 0
EXPLOSION_DUREE = 60  # Durée de l'animation en frames
is_bomb_exploded = False

# ============================================================================
# CRÉATION DES BOUTONS (couleurs harmonisées thème nature/fruits)
# ============================================================================
screen_center_x = L_ecran // 2

# Couleurs des boutons : (couleur normale, couleur survol)
# Thème : tons naturels, verts, oranges, bruns

# Bouton 1 Joueur - Vert feuille
bouton_1j = Bouton(
    screen_center_x - 150,
    150,
    300,
    55,
    "1 Joueur",
    (76, 153, 0),  # Vert vif
    (102, 178, 50),  # Vert clair au survol
)

# Bouton 2 Joueurs - Vert forêt
bouton_2j = Bouton(
    screen_center_x - 150,
    220,
    300,
    55,
    "2 Joueurs",
    (34, 120, 69),  # Vert forêt
    (50, 150, 90),  # Vert forêt clair
)

# Bouton Comment jouer - Orange fruit
bouton_regles = Bouton(
    screen_center_x - 150,
    290,
    300,
    55,
    "Comment jouer",
    (230, 126, 34),  # Orange
    (243, 156, 79),  # Orange clair
)

# Bouton Scores - Marron bois
bouton_scores = Bouton(
    screen_center_x - 150,
    360,
    300,
    55,
    "Scores",
    (139, 90, 43),  # Marron
    (166, 118, 74),  # Marron clair
)

# Bouton Quitter - Rouge pomme
bouton_quitter = Bouton(
    screen_center_x - 150,
    500,
    300,
    55,
    "Quitter",
    (192, 57, 43),  # Rouge foncé
    (217, 83, 70),  # Rouge clair
)

# Bouton Retour - Gris neutre
bouton_retour = Bouton(
    20, 20, 150, 50, "Retour", (100, 100, 100), (130, 130, 130)  # Gris  # Gris clair
)

# Bouton Menu (Game Over) - Marron bois
bouton_menu_go = Bouton(
    0,
    0,
    300,
    55,
    "Menu Principal",
    (139, 90, 43),  # Marron
    (166, 118, 74),  # Marron clair
)

# Variables de jeu
mes_fruits = []
morceaux_fruits = []
particules_explosion = []
particules_glace = []
frequence_lancer = random.randint(30, 100)
compteur = 0
running = True
niveau = 1
score = 0
gravite_actuelle = 0.4

# Variables pour le freeze (mode 2 joueurs)
freeze_j1_actif = False
freeze_j1_timer = 0
freeze_j1_en_attente = False
freeze_j1_delai_timer = 0

freeze_j2_actif = False
freeze_j2_timer = 0
freeze_j2_en_attente = False
freeze_j2_delai_timer = 0

# Variables pour le mode 1 joueur (gardées pour compatibilité)
freeze_actif = False
freeze_timer = 0
freeze_duree = 0
freeze_en_attente = False
freeze_delai_timer = 0
FREEZE_DELAI_FRAMES = 120  # 2 secondes

# Gestion du son
try:
    # Un seul fichier qui contient "3... 2... 1... GO!"
    son_decompte = pygame.mixer.Sound("Assets/Sounds/decompte_complet.wav")
    son_decompte.set_volume(0.6)
except (pygame.error, FileNotFoundError):
    print("Son manquant, création d'un son vide.")
    son_decompte = pygame.mixer.Sound(buffer=bytearray())
    
try:
    son_sliced = pygame.mixer.Sound("Assets/Sounds/sliced.wav")
    son_sliced.set_volume(0.5)
except (pygame.error, FileNotFoundError):
    print("Son manquant, création d'un son vide.")
    son_sliced = pygame.mixer.Sound(buffer=bytearray())
    
try:
    son_bomb = pygame.mixer.Sound("Assets/Sounds/bomb.wav")
    son_bomb.set_volume(0.7)
except (pygame.error, FileNotFoundError):
    print("Son manquant, création d'un son vide.")
    son_bomb = pygame.mixer.Sound(buffer=bytearray())
    
try:
    son_freeze = pygame.mixer.Sound("Assets/Sounds/freeze.wav")
    son_freeze.set_volume(0.5)
except (pygame.error, FileNotFoundError):
    print("Son manquant, création d'un son vide.")
    son_freeze = pygame.mixer.Sound(buffer=bytearray())
    
try:
    son_win = pygame.mixer.Sound("Assets/Sounds/win.mp3")
    son_win.set_volume(0.6)
except (pygame.error, FileNotFoundError):
    print("Son manquant, création d'un son vide.")
    son_win = pygame.mixer.Sound(buffer=bytearray())
    
def mettre_a_jour_score_et_niveau(points_gagnes):
    """
    Met à jour le score et vérifie si le joueur monte de niveau.
    
    Args:
        points_gagnes (int): Nombre de points à ajouter
    
    Returns:
        bool: True si le joueur a monté de niveau, False sinon
    """
    global score, niveau, gravite_actuelle
    
    score += points_gagnes
    
    # Vérifier montée de niveau tous les 10 points
    nouveau_niveau = (score // 10) + 1
    if nouveau_niveau > niveau:
        niveau = nouveau_niveau
        gravite_actuelle = min(0.4 + (niveau - 1) * 0.03, 1.0)
        print(f"🎉 NIVEAU {niveau} ! Gravité: {gravite_actuelle:.2f}")
        return True
    
    return False
    
# --- BOUCLE PRINCIPALE ---
while running:

    # 0. RE-CENTRAGE DYNAMIQUE
    largeur_actuelle = screen.get_width()
    hauteur_actuelle = screen.get_height()
    centre_x = largeur_actuelle // 2

    bouton_1j.rect.centerx = centre_x
    bouton_2j.rect.centerx = centre_x
    bouton_regles.rect.centerx = centre_x
    bouton_scores.rect.centerx = centre_x
    bouton_quitter.rect.centerx = centre_x
    bouton_menu_go.rect.centerx = centre_x
    bouton_menu_go.rect.y = hauteur_actuelle - 100

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
                morceaux_fruits = []
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
                freeze_en_attente = False
                freeze_delai_timer = 0
                is_bomb_exploded = False

                son_decompte.stop()  # Coupe le son s'il jouait déjà
                son_decompte.play()

            if bouton_2j.est_clique(event):
                nombre_de_joueurs = 2
                etat_jeu = "jeu"
                mes_fruits = []
                morceaux_fruits = []
                # Réinitialisation des DEUX joueurs
                vies_j1 = 3
                vies_j2 = 3
                # Réinitialision du score
                score = 0
                start_ticks = pygame.time.get_ticks()

                # Reset complet du freeze (mode 2 joueurs - séparé)
                freeze_j1_actif = False
                freeze_j1_timer = 0
                freeze_j1_en_attente = False
                freeze_j1_delai_timer = 0

                freeze_j2_actif = False
                freeze_j2_timer = 0
                freeze_j2_en_attente = False
                freeze_j2_delai_timer = 0

                is_bomb_exploded = False
                son_decompte.stop()  # Coupe le son s'il jouait déjà
                son_decompte.play()

            if bouton_regles.est_clique(event):
                etat_jeu = "regles"
            if bouton_scores.est_clique(event):
                etat_jeu = "scores"
            if bouton_quitter.est_clique(event):
                running = False

        elif etat_jeu in ["regles", "scores"]:
            if bouton_retour.est_clique(event):
                etat_jeu = "menu"

            # Touche R pour réinitialiser l'historique (seulement dans l'écran scores)
            if (
                etat_jeu == "scores"
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                reinitialiser_scores()
                print("🗑️ Historique des scores réinitialisé.")

        elif etat_jeu == "game_over":
            if bouton_menu_go.est_clique(event):
                etat_jeu = "menu"

        elif etat_jeu == "jeu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                etat_jeu = "menu"
                mes_fruits = []
                morceaux_fruits = []
                son_decompte.stop()

            seconds_ecoules = (pygame.time.get_ticks() - start_ticks) / 1000

            if seconds_ecoules > 3:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    controller.start_slice(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONUP:
                    score_geste = controller.end_slice(
                        mes_fruits, screen.get_width(), nombre_de_joueurs
                    )
                    print(f"DEBUG: Score geste souris = {score_geste}, total avant = {score}")

                    # Ajoute le score au total (mode 1 joueur uniquement)
                    if (
                        nombre_de_joueurs == 1
                        and isinstance(score_geste, int)
                        and score_geste > 0
                    ):
                        mettre_a_jour_score_et_niveau(score_geste)

                if event.type == pygame.KEYDOWN:
                    result = controller.handle_keyboard_inputs(
                        mes_fruits,
                        screen.get_width(),
                        screen.get_height(),
                        event.key,
                        nombre_de_joueurs,
                        morceaux_fruits
                    )
                    if result == "game_over":
                        son_bomb.play() 
                        
                        # Créer les particules d'explosion (position clavier = centre zone J1)
                        mx = screen.get_width() // 4  # Centre de la zone J1
                        my = screen.get_height() // 2
                        for _ in range(50):
                            particules_explosion.append(ParticuleExplosion(mx, my))
                        
                        explosion_en_cours = True
                        explosion_timer = EXPLOSION_DUREE
                        is_bomb_exploded = True
                        if nombre_de_joueurs == 1:
                            duree_partie = (
                                (pygame.time.get_ticks() - start_ticks) / 1000
                            ) - 3
                            sauvegarder_score(score, niveau, duree_partie)
                        print("BOOM ! Bombe tranchée au clavier !")
                        
                    elif result == "freeze":
                        son_freeze.play()
                        # Particule de glace
                        mx, my = pygame.mouse.get_pos()
                        for _ in range(30):
                            particules_glace.append(ParticuleGlace(mx, my))
                        # Mode 1 joueur
                        if not freeze_actif and not freeze_en_attente:
                            freeze_en_attente = True
                            freeze_delai_timer = FREEZE_DELAI_FRAMES

                    elif result == "freeze_j1":
                        son_freeze.play()
                        mx, my = pygame.mouse.get_pos()
                        for _ in range(30):
                            particules_glace.append(ParticuleGlace(mx, my))
                        # Freeze pour joueur 1 seulement
                        if not freeze_j1_actif and not freeze_j1_en_attente:
                            freeze_j1_en_attente = True
                            freeze_j1_delai_timer = FREEZE_DELAI_FRAMES

                    elif result == "freeze_j2":
                        son_freeze.play()
                        mx, my = pygame.mouse.get_pos()
                        for _ in range(30):
                            particules_glace.append(ParticuleGlace(mx, my))
                        # Freeze pour joueur 2 seulement
                        if not freeze_j2_actif and not freeze_j2_en_attente:
                            freeze_j2_en_attente = True
                            freeze_j2_delai_timer = FREEZE_DELAI_FRAMES
                    elif isinstance(result, int) and result > 0:
                        son_sliced.play()
                    # Score en temps réel (mode 1 joueur)
                    if nombre_de_joueurs == 1:
                        # +1 point de base par fruit
                        points_gagnes = 1
                        # Bonus si combo >= 3
                        combo = controller.get_combo_actuel()
                        if combo >= 3:
                            points_gagnes += 1  # +1 bonus
                        
                        mettre_a_jour_score_et_niveau(points_gagnes)

    # 2. LOGIQUE ET DESSIN

    if etat_jeu == "menu":
        # Affiche le fond du menu (Background0)
        gestionnaire_ecran.afficher_fond_menu(screen)

        # Titre du jeu
        titre = font_titre.render("FRUIT SLICER", True, (255, 100, 100))
        screen.blit(titre, (screen.get_width() // 2 - titre.get_width() // 2, 50))

        # Boutons du menu
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

    # --- ÉCRAN GAME OVER ---
    elif etat_jeu == "game_over":

        gestionnaire_ecran.afficher_fond_menu(screen)

        milieu_x = screen.get_width() // 2
        hauteur_ecran = screen.get_height()

        # Position Y de départ (plus haut pour laisser de la place au bouton)
        y_titre = 80

        # ====================================================================
        # MODE 1 JOUEUR
        # ====================================================================
        if nombre_de_joueurs == 1:
            # Ombre du titre
            txt_go_ombre = font_game_over.render(
                "GAME OVER", True, COULEURS["titre_ombre"]
            )
            screen.blit(
                txt_go_ombre,
                (milieu_x - txt_go_ombre.get_width() // 2 + 3, y_titre + 3),
            )

            # Titre
            txt_go = font_game_over.render("GAME OVER", True, COULEURS["game_over"])
            screen.blit(txt_go, (milieu_x - txt_go.get_width() // 2, y_titre))

            if is_bomb_exploded:
                txt_boom = font_game_over.render("BOOM !", True, COULEURS["boom"])
                screen.blit(
                    txt_boom, (milieu_x - txt_boom.get_width() // 2, y_titre + 80)
                )

                txt_raison = font_raison.render(
                    "Vous avez tranche une bombe !", True, COULEURS["message"]
                )
                screen.blit(
                    txt_raison, (milieu_x - txt_raison.get_width() // 2, y_titre + 150)
                )

                txt_score = font_vies.render(
                    f"Score final : {score}", True, COULEURS["score_final"]
                )
                screen.blit(
                    txt_score, (milieu_x - txt_score.get_width() // 2, y_titre + 200)
                )

                txt_niveau = font_raison.render(
                    f"Niveau atteint : {niveau}", True, COULEURS["niveau"]
                )
                screen.blit(
                    txt_niveau, (milieu_x - txt_niveau.get_width() // 2, y_titre + 250)
                )
            else:
                txt_raison = font_raison.render(
                    "Vous avez perdu toutes vos vies !", True, COULEURS["message"]
                )
                screen.blit(
                    txt_raison, (milieu_x - txt_raison.get_width() // 2, y_titre + 80)
                )

                txt_score = font_vies.render(
                    f"Score final : {score}", True, COULEURS["score_final"]
                )
                screen.blit(
                    txt_score, (milieu_x - txt_score.get_width() // 2, y_titre + 140)
                )

                txt_niveau = font_raison.render(
                    f"Niveau atteint : {niveau}", True, COULEURS["niveau"]
                )
                screen.blit(
                    txt_niveau, (milieu_x - txt_niveau.get_width() // 2, y_titre + 190)
                )

        # ====================================================================
        # MODE 2 JOUEURS
        # ====================================================================
        else:
            if is_bomb_exploded:
                txt_go_ombre = font_game_over.render(
                    "GAME OVER", True, COULEURS["titre_ombre"]
                )
                screen.blit(
                    txt_go_ombre,
                    (milieu_x - txt_go_ombre.get_width() // 2 + 3, y_titre + 3),
                )

                txt_go = font_game_over.render("GAME OVER", True, COULEURS["game_over"])
                screen.blit(txt_go, (milieu_x - txt_go.get_width() // 2, y_titre))

                txt_boom = font_game_over.render("BOOM !", True, COULEURS["boom"])
                screen.blit(
                    txt_boom, (milieu_x - txt_boom.get_width() // 2, y_titre + 80)
                )

                txt_egalite = font_raison.render(
                    "Egalite ! Les deux joueurs ont perdu.", True, COULEURS["egalite"]
                )
                screen.blit(
                    txt_egalite,
                    (milieu_x - txt_egalite.get_width() // 2, y_titre + 150),
                )
                if nombre_de_joueurs == 2:
                    duree_partie = (
                        (pygame.time.get_ticks() - start_ticks) / 1000) - 3
                    sauvegarder_score(0, 1, duree_partie, mode="2j", gagnant="Égalité")
            else:
                quart_gauche = milieu_x // 2
                quart_droite = milieu_x + milieu_x // 2
                centre_y = hauteur_ecran // 2 - 50

                # Joueur 1 (Gauche)
                if vies_j1 <= 0:
                    txt_j1 = font_game_over.render("PERDU", True, COULEURS["perdant"])
                    txt_j1_label = font_raison.render(
                        "Joueur 1", True, COULEURS["message"]
                    )
                else:
                    txt_j1 = font_game_over.render(
                        "GAGNANT !", True, COULEURS["gagnant"]
                    )
                    txt_j1_label = font_raison.render(
                        "Joueur 1", True, COULEURS["message"]
                    )

                screen.blit(txt_j1, (quart_gauche - txt_j1.get_width() // 2, centre_y))
                screen.blit(
                    txt_j1_label,
                    (quart_gauche - txt_j1_label.get_width() // 2, centre_y + 70),
                )

                # Joueur 2 (Droite)
                if vies_j2 <= 0:
                    txt_j2 = font_game_over.render("PERDU", True, COULEURS["perdant"])
                    txt_j2_label = font_raison.render(
                        "Joueur 2", True, COULEURS["message"]
                    )
                else:
                    txt_j2 = font_game_over.render(
                        "GAGNANT !", True, COULEURS["gagnant"]
                    )
                    txt_j2_label = font_raison.render(
                        "Joueur 2", True, COULEURS["message"]
                    )

                screen.blit(txt_j2, (quart_droite - txt_j2.get_width() // 2, centre_y))
                screen.blit(
                    txt_j2_label,
                    (quart_droite - txt_j2_label.get_width() // 2, centre_y + 70),
                )

        # Repositionner le bouton plus bas
        bouton_menu_go.dessiner(screen)

    # --- ÉCRAN DE JEU ---
    elif etat_jeu == "jeu":

        seconds_ecoules = (pygame.time.get_ticks() - start_ticks) / 1000
        en_attente = seconds_ecoules < 3

        # --- LOGIQUE ---

        # étape 1 : Gestion du délai avant activation du freeze différé
        if not en_attente:

            # Gestion du freeze en fonction du mode
            if nombre_de_joueurs == 1:
                # Gestion du freeze différé en mode 1 joueur
                if freeze_en_attente:
                    freeze_delai_timer -= 1
                    if freeze_delai_timer <= 0:
                        # Le délai est écoulé, on active le freeze
                        freeze_en_attente = False
                        freeze_actif = True
                        freeze_duree = random.randint(3, 5)  # Entre 3 et 5 secondes
                        freeze_timer = (
                            freeze_duree * 60
                        )  # Conversion en frames (60 FPS)
                        print(
                            f"FREEZE activé pour {freeze_duree} secondes après le décompte !"
                        )

                # étape 2 : Gestion du freeze actif
                if freeze_actif:
                    freeze_timer -= 1
                    if freeze_timer <= 0:
                        freeze_actif = False
                        print("Effet de freeze terminé.")
            else:
                # MODE 2 JOUEURS : freeze séparé pour chaque joueur

                # Freeze Joueur 1
                if freeze_j1_en_attente:
                    freeze_j1_delai_timer -= 1
                    if freeze_j1_delai_timer <= 0:
                        freeze_j1_en_attente = False
                        freeze_j1_actif = True
                        freeze_j1_timer = random.randint(3, 5) * 60
                        print("FREEZE J1 active !")

                if freeze_j1_actif:
                    freeze_j1_timer -= 1
                    if freeze_j1_timer <= 0:
                        freeze_j1_actif = False
                        print("Freeze J1 termine.")

                # Freeze Joueur 2
                if freeze_j2_en_attente:
                    freeze_j2_delai_timer -= 1
                    if freeze_j2_delai_timer <= 0:
                        freeze_j2_en_attente = False
                        freeze_j2_actif = True
                        freeze_j2_timer = random.randint(3, 5) * 60
                        print("FREEZE J2 active !")

                if freeze_j2_actif:
                    freeze_j2_timer -= 1
                    if freeze_j2_timer <= 0:
                        freeze_j2_actif = False
                        print("Freeze J2 termine.")
                        
            # ====================================================================
            # GESTION DU DÉLAI D'EXPLOSION
            # ====================================================================
            if explosion_en_cours:
                explosion_timer -= 1
                if explosion_timer <= 0:
                    explosion_en_cours = False
                    son_win.play()  # Jouer le son de fin
                    etat_jeu = "game_over"
            
            # Gestion de la souris
            elif controller.slicing:
                result = controller.update_slice(
                    pygame.mouse.get_pos(),
                    mes_fruits,
                    screen.get_width(),
                    nombre_de_joueurs,
                    morceaux_fruits
                )

                # --- TRAITEMENT DU RÉSULTAT ---
                if result == "game_over":
                    # Jouer le son de la bombe
                    son_bomb.play()
                    
                    # Créer les particules d'explosion à la position de la souris
                    mx, my = pygame.mouse.get_pos()
                    for _ in range(50):  # 50 particules
                        particules_explosion.append(ParticuleExplosion(mx, my))
                        
                    explosion_en_cours = True
                    explosion_timer = EXPLOSION_DUREE
                    is_bomb_exploded = True
                    if nombre_de_joueurs == 1:
                        duree_partie = (
                            (pygame.time.get_ticks() - start_ticks) / 1000
                        ) - 3
                        sauvegarder_score(score, niveau, duree_partie)
                    # La bombe a été tranchée : partie terminée
                    print("BOOM ! Bombe tranchée !")

                elif result == "freeze":
                    # Jouer le son du freeze
                    son_freeze.play()
                    
                    # Créer les particules de glace
                    mx, my = pygame.mouse.get_pos()
                    for _ in range(30):  # 30 particules
                        particules_glace.append(ParticuleGlace(mx, my))
                    # Le glaçon a été tranché : activation du freeze différé
                    if not freeze_actif and not freeze_en_attente:
                        freeze_en_attente = True
                        freeze_delai_timer = FREEZE_DELAI_FRAMES  # 2 secondes de délai
                        print("Glaçon tranché ! Freeze différé activé.")
                        
                elif result == "freeze_j1":
                    # Freeze pour joueur 1 seulement
                    if not freeze_j1_actif and not freeze_j1_en_attente:
                        freeze_j1_en_attente = True
                        freeze_j1_delai_timer = FREEZE_DELAI_FRAMES  # 2 secondes de délai
                        print("Glaçon tranché J1 ! Freeze différé J1 activé.")
                
                elif result == "freeze_j2":
                    # Freeze pour joueur 2 seulement
                    if not freeze_j2_actif and not freeze_j2_en_attente:
                        freeze_j2_en_attente = True
                        freeze_j2_delai_timer = FREEZE_DELAI_FRAMES  # 2 secondes de délai
                        print("Glaçon tranché J2 ! Freeze différé J2 activé.")

                elif isinstance(result, int) and result > 0:
                    son_sliced.play()
                    # Score en temps réel (mode 1 joueur)
                    if nombre_de_joueurs == 1:
                        # +1 point de base par fruit
                        points_gagnes = 1
                        # Bonus si combo >= 3
                        combo = controller.get_combo_actuel()
                        if combo >= 3:
                            points_gagnes += 1  # +1 bonus
                        
                        mettre_a_jour_score_et_niveau(points_gagnes)

            compteur += 1

            # Ajustement de la fréquence en fonction du niveau (uniquement en mode 1 joueur)
            if nombre_de_joueurs == 1:
                min_freq = max(
                    20, 50 - (niveau - 1) * 2
                )  # Fréquence minimale diminue avec le niveau
                max_freq = max(40, 150 - (niveau - 1) * 3)  # Maximale aussi
            else:
                min_freq = 30  # Valeurs par défaut pour mode 2 joueurs
                max_freq = 100
            if compteur >= frequence_lancer and not explosion_en_cours:
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
                        mes_fruits.append(
                            Bombe(
                                screen.get_width(),
                                screen.get_height(),
                                zone_joueur,
                                gravite_pour_objet,
                            )
                        )
                        print("💣 Bombe apparue !")
                    else:  # type_special == "ice"
                        mes_fruits.append(
                            Glacon(
                                screen.get_width(),
                                screen.get_height(),
                                zone_joueur,
                                gravite_pour_objet,
                            )
                        )
                        print("❄️ Glaçon apparu !")
                else:
                    # 70% : Fruit normal
                    type_fruit = random.choice(liste_fruits)
                    mes_fruits.append(
                        Fruit(
                            type_fruit,
                            screen.get_width(),
                            screen.get_height(),
                            zone_joueur,
                            gravite_pour_objet,
                        )
                    )

                compteur = 0
                frequence_lancer = random.randint(min_freq, max_freq)

        # --- DESSIN ---
        largeur_ecran = screen.get_width()
        hauteur_ecran = screen.get_height()
        milieu_x = gestionnaire_ecran.afficher_fond(
            screen, nombre_de_joueurs, font_info
        )

        # --- GESTION FRUITS ET VIES SÉPARÉES ---
        for f in mes_fruits[:]:
            if not en_attente:
                if nombre_de_joueurs == 1:
                    # Les fruits ne bougent que si pas de freeze actif
                    if not freeze_actif:
                        f.update(screen.get_width())
                else:
                    # Mode 2J : freeze par zone
                    #  Le fruit bouge seulement si son côté n'est pas en freeze
                    fruit_a_gauche = f.x < milieu_x

                    if fruit_a_gauche:
                        if not freeze_j1_actif:
                            f.update(screen.get_width())
                    else:
                        if not freeze_j2_actif:
                            f.update(screen.get_width())
            # Dessine le fruit
            f.draw(screen)

            # --- DÉTECTION FRUIT RATÉ ---
            if f.y > screen.get_height() + 50:
                mes_fruits.remove(f)

                # ============================================================
                # VÉRIFICATION : On n'enlève une vie QUE pour les FRUITS
                # ============================================================
                # Les glaçons et les bombes ratés ne pénalisent pas le joueur
                # - Glaçon raté : pas de bonus freeze, mais pas de pénalité
                # - Bombe ratée : c'est une BONNE chose de l'avoir évitée !
                # ============================================================

                # On vérifie que ce n'est PAS un glaçon et PAS une bombe
                est_un_fruit = not isinstance(f, (Glacon, Bombe))

                # On enlève une vie SEULEMENT si :
                # 1. C'est un fruit (pas glaçon/bombe)
                # 2. Il n'a pas été tranché
                # 3. Le jeu n'est pas en attente (décompte)
                if est_un_fruit and not f.sliced and not en_attente:
                    if nombre_de_joueurs == 1:
                        # Mode 1 joueur : on utilise vies_j1
                        vies_j1 -= 1
                        print(f"Fruit raté ! Vies restantes : {vies_j1}")
                        if vies_j1 <= 0:
                            son_win.play()
                            duree_partie = (
                                (pygame.time.get_ticks() - start_ticks) / 1000
                            ) - 3
                            sauvegarder_score(score, niveau, duree_partie)
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
                            # Détermine le gagnant
                            if vies_j1 <= 0 and vies_j2 <= 0:
                                gagnant = "egalite"
                            elif vies_j1 <= 0:
                                gagnant = "J2"
                            else:
                                gagnant = "J1"
                            
                            son_win.play()
                            duree_partie = (
                                (pygame.time.get_ticks() - start_ticks) / 1000
                            ) - 3
                            sauvegarder_score(
                                0, 1, duree_partie, mode="2j", gagnant=gagnant
                            )
                            etat_jeu = "game_over"

        # ====================================================================
        # GESTION DES MORCEAUX DE FRUITS (NOUVEAU)
        # ====================================================================
        # Cette section gère les morceaux créés quand un fruit est tranché.
        # Les morceaux ont leur propre physique (séparation, rotation, fade out).
        # ====================================================================
        
        # Mise à jour de chaque morceau (physique + fade out)
        for morceau in morceaux_fruits:
            morceau.update()
        
        # Suppression des morceaux qui ont fini leur animation
        morceaux_fruits = [m for m in morceaux_fruits if not m.est_termine()]
        
        # Affichage de chaque morceau
        for morceau in morceaux_fruits:
            morceau.draw(screen)
            
        # ====================================================================
        # GESTION DES PARTICULES D'EXPLOSION ET DE GLACE
        # ====================================================================
        
        # Mise à jour et affichage des particules d'explosion
        for particule in particules_explosion[:]:
            particule.update()
            particule.draw(screen)
            particles_explosion = [p for p in particules_explosion if not p.est_termine()]
        
        # Mise à jour et affichage des particules de glace
        for particule in particules_glace[:]:
            particule.update()
            particule.draw(screen)
            if particule.est_termine():
                particules_glace.remove(particule)

        if not en_attente:
            controller.draw_slice(screen)

        # --- AFFICHAGE DES VIES ET NIVEAU (HUD) ---

        if nombre_de_joueurs == 1:
            # Instruction en haut (remplace le blanc)
            txt_instruction = font_info.render(
                "Clavier ou Souris", True, COULEURS["hud_instruction"]
            )
            screen.blit(
                txt_instruction,
                (largeur_ecran // 2 - txt_instruction.get_width() // 2, 20),
            )

            # Vies
            txt_vies = font_vies.render(f"VIES : {vies_j1}", True, COULEURS["hud_vies"])
            screen.blit(txt_vies, (largeur_ecran // 2 - txt_vies.get_width() // 2, 60))

            # Niveau
            txt_niveau = font_vies.render(
                f"NIVEAU : {niveau}", True, COULEURS["hud_niveau"]
            )
            screen.blit(
                txt_niveau, (largeur_ecran // 2 - txt_niveau.get_width() // 2, 105)
            )

            # Score (optionnel, affiché pendant le jeu)
            txt_score = font_info.render(
                f"Score : {score}", True, COULEURS["hud_score"]
            )
            screen.blit(
                txt_score, (largeur_ecran // 2 - txt_score.get_width() // 2, 150)
            )
        else:
            # Mode 2 joueurs
            # Label J1
            txt_j1 = font_info.render("J1 (Clavier)", True, COULEURS["label_j1"])
            screen.blit(txt_j1, (milieu_x // 2 - txt_j1.get_width() // 2, 20))

            # Vies J1
            txt_vies_j1 = font_vies.render(
                f"VIES : {vies_j1}", True, COULEURS["hud_vies"]
            )
            screen.blit(txt_vies_j1, (milieu_x // 2 - txt_vies_j1.get_width() // 2, 60))

            # Label J2
            txt_j2 = font_info.render("J2 (Souris)", True, COULEURS["label_j2"])
            screen.blit(
                txt_j2, (milieu_x + milieu_x // 2 - txt_j2.get_width() // 2, 20)
            )

            # Vies J2
            txt_vies_j2 = font_vies.render(
                f"VIES : {vies_j2}", True, COULEURS["hud_vies"]
            )
            screen.blit(
                txt_vies_j2,
                (milieu_x + milieu_x // 2 - txt_vies_j2.get_width() // 2, 60),
            )

        # --- AFFICHAGE DU FREEZE ---
        if nombre_de_joueurs == 1:
            if freeze_actif:
                # Overlay bleu semi-transparent
                overlay = pygame.Surface((largeur_ecran, hauteur_ecran))
                overlay.set_alpha(60)
                overlay.fill((173, 216, 230))  # Bleu clair
                screen.blit(overlay, (0, 0))

                temps_restant = freeze_timer / 60
                txt_freeze = font_freeze.render(
                    "FREEZE", True, COULEURS["freeze_texte"]
                )
                txt_timer = font_timer.render(
                    f"{temps_restant:.1f}s", True, COULEURS["freeze_timer"]
                )

                # Clignotement
                if (freeze_timer // 15) % 2 == 0:
                    screen.blit(
                        txt_freeze,
                        (
                            largeur_ecran // 2 - txt_freeze.get_width() // 2,
                            hauteur_ecran // 2 - 80,
                        ),
                    )
                screen.blit(
                    txt_timer,
                    (
                        largeur_ecran // 2 - txt_timer.get_width() // 2,
                        hauteur_ecran // 2 + 20,
                    ),
                )
        else:
            # Mode 2 joueurs - Freeze par zone
            if freeze_j1_actif:
                overlay_j1 = pygame.Surface((milieu_x, hauteur_ecran))
                overlay_j1.set_alpha(60)
                overlay_j1.fill((173, 216, 230))
                screen.blit(overlay_j1, (0, 0))

                temps_j1 = freeze_j1_timer / 60
                txt_freeze_j1 = font_vies.render(
                    "FREEZE", True, COULEURS["freeze_texte"]
                )
                txt_timer_j1 = font_raison.render(
                    f"{temps_j1:.1f}s", True, COULEURS["freeze_timer"]
                )

                if (freeze_j1_timer // 15) % 2 == 0:
                    screen.blit(
                        txt_freeze_j1,
                        (
                            milieu_x // 2 - txt_freeze_j1.get_width() // 2,
                            hauteur_ecran // 2 - 40,
                        ),
                    )
                screen.blit(
                    txt_timer_j1,
                    (
                        milieu_x // 2 - txt_timer_j1.get_width() // 2,
                        hauteur_ecran // 2 + 10,
                    ),
                )

            if freeze_j2_actif:
                overlay_j2 = pygame.Surface((largeur_ecran - milieu_x, hauteur_ecran))
                overlay_j2.set_alpha(60)
                overlay_j2.fill((173, 216, 230))
                screen.blit(overlay_j2, (milieu_x, 0))

                temps_j2 = freeze_j2_timer / 60
                txt_freeze_j2 = font_vies.render(
                    "FREEZE", True, COULEURS["freeze_texte"]
                )
                txt_timer_j2 = font_raison.render(
                    f"{temps_j2:.1f}s", True, COULEURS["freeze_timer"]
                )

                if (freeze_j2_timer // 15) % 2 == 0:
                    screen.blit(
                        txt_freeze_j2,
                        (
                            milieu_x
                            + (largeur_ecran - milieu_x) // 2
                            - txt_freeze_j2.get_width() // 2,
                            hauteur_ecran // 2 - 40,
                        ),
                    )
                screen.blit(
                    txt_timer_j2,
                    (
                        milieu_x
                        + (largeur_ecran - milieu_x) // 2
                        - txt_timer_j2.get_width() // 2,
                        hauteur_ecran // 2 + 10,
                    ),
                )

        # --- DÉCOMPTE DÉBUT DE JEU ---
        if en_attente:
            chiffre = int(4 - seconds_ecoules)

            # Texte avec couleurs visibles sur fond clair
            surf_phrase = font_phrase.render(
                "Le jeu demarre dans", True, COULEURS["decompte_texte"]
            )
            surf_chrono = font_chrono.render(
                str(chiffre), True, COULEURS["decompte_chiffre"]
            )

            if nombre_de_joueurs == 1:
                rect_phrase = surf_phrase.get_rect(
                    center=(largeur_ecran // 2, hauteur_ecran // 2 - 60)
                )
                rect_chrono = surf_chrono.get_rect(
                    center=(largeur_ecran // 2, hauteur_ecran // 2 + 40)
                )
                screen.blit(surf_phrase, rect_phrase)
                screen.blit(surf_chrono, rect_chrono)
            else:
                # Joueur 1 (gauche)
                rect_phrase_j1 = surf_phrase.get_rect(
                    center=(milieu_x // 2, hauteur_ecran // 2 - 60)
                )
                rect_chrono_j1 = surf_chrono.get_rect(
                    center=(milieu_x // 2, hauteur_ecran // 2 + 40)
                )
                screen.blit(surf_phrase, rect_phrase_j1)
                screen.blit(surf_chrono, rect_chrono_j1)

                # Joueur 2 (droite)
                rect_phrase_j2 = surf_phrase.get_rect(
                    center=(milieu_x + milieu_x // 2, hauteur_ecran // 2 - 60)
                )
                rect_chrono_j2 = surf_chrono.get_rect(
                    center=(milieu_x + milieu_x // 2, hauteur_ecran // 2 + 40)
                )
                screen.blit(surf_phrase, rect_phrase_j2)
                screen.blit(surf_chrono, rect_chrono_j2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
