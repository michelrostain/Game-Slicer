import pygame, random
from constantes import images

# Classe pour représenter un fruit dans le jeu
class Fruit:
    def __init__(self, type_de_fruit, largeur, hauteur, zone_joueur=None, gravity=0.4):
        # Initialisation du type de fruit (ex: "pomme", "banane", etc.)
        self.type = type_de_fruit
        # Indicateur si le fruit a été tranché
        self.sliced = False
        # Rayon du fruit pour les collisions et l'affichage
        self.radius = 60  # Légèrement réduit pour mieux coller aux fruits fins
        
        # Stockage de la zone du joueur (1 pour gauche, 2 pour droite, None pour mode 1 joueur)
        self.zone_joueur = zone_joueur
        
        # --- GESTION INTELLIGENTE DES IMAGES ---
        # Récupération de l'image brute depuis les constantes
        raw_image = images.get(self.type)
        # Dictionnaire pour stocker les variantes d'image (pour les poires avec états)
        self.images_set = None
        
        # Gravité appliquée au fruit
        self.gravity = gravity

        if isinstance(raw_image, dict):
            # Cas d'un fruit avec plusieurs états (ex: poire avec "up", "down", "cut")
            self.images_set = {}
            
            # STRATÉGIE : On utilise l'image "cut" pour déterminer la taille cible
            # Toutes les images auront la même LARGEUR que "cut" après redimensionnement
            
            HAUTEUR_CIBLE = 160  # Hauteur fixe pour l'affichage
            
            # 1. On redimensionne d'abord l'image "cut" avec la hauteur cible
            if "cut" in raw_image:
                img_cut = raw_image["cut"]
                ratio_cut = img_cut.get_width() / img_cut.get_height()
                largeur_cut = int(HAUTEUR_CIBLE * ratio_cut)
                self.images_set["cut"] = pygame.transform.smoothscale(
                    img_cut, 
                    (largeur_cut, HAUTEUR_CIBLE)
                )
                
                # 2. On redimensionne "up" et "down" pour avoir la MÊME LARGEUR que "cut"
                for key in ["up", "down"]:
                    if key in raw_image:
                        img_orig = raw_image[key]
                        # On force la même largeur que "cut", en calculant la hauteur proportionnelle
                        ratio_orig = img_orig.get_width() / img_orig.get_height()
                        hauteur_proportionnelle = int(largeur_cut / ratio_orig)
                        
                        # Si la hauteur calculée dépasse HAUTEUR_CIBLE, on ajuste
                        if hauteur_proportionnelle > HAUTEUR_CIBLE:
                            # On garde HAUTEUR_CIBLE et on recalcule la largeur
                            self.images_set[key] = pygame.transform.smoothscale(
                                img_orig,
                                (int(HAUTEUR_CIBLE * ratio_orig), HAUTEUR_CIBLE)
                            )
                        else:
                            # On utilise la largeur de "cut"
                            self.images_set[key] = pygame.transform.smoothscale(
                                img_orig,
                                (largeur_cut, hauteur_proportionnelle)
                            )
            else:
                # Fallback si pas d'image "cut"
                for key, img_orig in raw_image.items():
                    ratio = img_orig.get_width() / img_orig.get_height()
                    nouvelle_largeur = int(HAUTEUR_CIBLE * ratio)
                    self.images_set[key] = pygame.transform.smoothscale(
                        img_orig, 
                        (nouvelle_largeur, HAUTEUR_CIBLE)
                    )
            
            # Image initiale : état "up" (fruit montant)
            self.image = self.images_set["up"]

        elif raw_image is not None:
            # Cas d'un fruit simple (sans états multiples)
            HAUTEUR_CIBLE = 160
            # Calcul du ratio pour conserver les proportions
            ratio = raw_image.get_width() / raw_image.get_height()
            nouvelle_largeur = int(HAUTEUR_CIBLE * ratio)
            # Redimensionnement
            self.image = pygame.transform.smoothscale(raw_image, (nouvelle_largeur, HAUTEUR_CIBLE))
        else:
            # Pas d'image disponible : on utilisera un cercle coloré
            self.image = None

        # --- POSITIONNEMENT INITIAL ---
        # Calcul du milieu de l'écran
        milieu_x = largeur // 2
        if zone_joueur == 1:
            # Zone joueur 1 : côté gauche de l'écran
            self.x = random.randint(100, milieu_x - 100)
        elif zone_joueur == 2:
            # Zone joueur 2 : côté droite de l'écran
            self.x = random.randint(milieu_x + 100, largeur - 100)
        else:
            # Mode 1 joueur : position aléatoire sur tout l'écran
            self.x = random.randint(100, largeur - 100)
        
        # Position verticale initiale : en haut de l'écran
        self.y = hauteur
        # Vitesses initiales (aléatoires pour un mouvement naturel)
        self.speed_x = random.uniform(-10, 10)  # Vitesse horizontale
        self.speed_y = random.uniform(-20, -10)  # Vitesse verticale (vers le haut au départ)
        # Gravité pour simuler la chute
        self.gravity = gravity
        
        # Couleur de secours si pas d'image (pour debug)
        self.color = (255, 0, 0)
        if self.type == "banane": self.color = (255, 255, 0)
        elif self.type == "orange": self.color = (255, 165, 0)

    def update(self, largeur_ecran, speed_factor=1):
        # Mise à jour de la physique du fruit
        # Application de la gravité à la vitesse verticale
        self.speed_y += self.gravity * speed_factor
        # Mise à jour des positions basées sur les vitesses
        self.x += self.speed_x * speed_factor
        self.y += self.speed_y * speed_factor

        # Changement d'image pour les fruits avec états (ex: poire)
        if self.images_set and not self.sliced:
            if self.speed_y < 0:
                self.image = self.images_set["up"]  # Fruit montant
            else:
                self.image = self.images_set["down"]  # Fruit descendant

        # --- REBONDS SUR LES BORDS DE L'ÉCRAN ---
        # Bord gauche : rebond si le fruit sort à gauche
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -1  # Inversion de la direction horizontale
        
        # Bord droit : rebond si le fruit sort à droite
        if self.x + self.radius > largeur_ecran:
            self.x = largeur_ecran - self.radius
            self.speed_x *= -1
        
        # --- CONFINEMENT AUX ZONES EN MODE 2 JOUEURS ---
        # Si le fruit est assigné à une zone spécifique (mode 2 joueurs), il ne peut pas traverser le milieu
        if self.zone_joueur is not None:
            milieu_x = largeur_ecran // 2
            if self.zone_joueur == 1:
                # Zone joueur 1 (gauche) : rebond sur le bord droit de sa zone
                if self.x + self.radius > milieu_x:
                    self.x = milieu_x - self.radius
                    self.speed_x *= -1
            elif self.zone_joueur == 2:
                # Zone joueur 2 (droite) : rebond sur le bord gauche de sa zone
                if self.x - self.radius < milieu_x:
                    self.x = milieu_x + self.radius
                    self.speed_x *= -1

    def couper(self):
        # Méthode appelée lorsque le fruit est tranché
        self.sliced = True
        # Changement d'image si le fruit a des états (ex: poire coupée)
        if self.images_set:
            self.image = self.images_set["cut"]
            self.speed_y = -5  # Petit saut visuel vers le haut après la coupe

    def draw(self, screen):
        # Affichage du fruit sur l'écran
        if self.image:
            # Centrage de l'image sur la position x,y
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
        else:
            # Affichage de secours : cercle coloré
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Glacon:
    def __init__(self, largeur, hauteur, gravity=0.4):
        self.type = "glacon"
        self.sliced = False
        self.images_set = None
        
        self.radius = 40
        self.color = (173, 216, 230)  # Bleu clair
        
        self.x = random.randint(100, largeur - 100)
        self.y = hauteur
        self.speed_x = random.uniform(-8, 8)
        self.speed_y = random.uniform(-18, -12)
        self.gravity = gravity
    
    def update(self, largeur_ecran, speed_factor=1):
        """Met à jour le glaçon"""
        # Le glaçon est aussi affecté par le speed_factor (il peut s'auto-geler si on veut)
        self.speed_y += self.gravity * speed_factor
        self.x += self.speed_x * speed_factor
        self.y += self.speed_y * speed_factor
        
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -1
        
        if self.x + self.radius > largeur_ecran:
            self.x = largeur_ecran - self.radius
            self.speed_x *= -1
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Effet de reflet blanc
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x - 10), int(self.y - 10)), 10)