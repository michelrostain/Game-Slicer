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
                    img_cut, (largeur_cut, HAUTEUR_CIBLE)
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
                                (int(HAUTEUR_CIBLE * ratio_orig), HAUTEUR_CIBLE),
                            )
                        else:
                            # On utilise la largeur de "cut"
                            self.images_set[key] = pygame.transform.smoothscale(
                                img_orig, (largeur_cut, hauteur_proportionnelle)
                            )
            else:
                # Fallback si pas d'image "cut"
                for key, img_orig in raw_image.items():
                    ratio = img_orig.get_width() / img_orig.get_height()
                    nouvelle_largeur = int(HAUTEUR_CIBLE * ratio)
                    self.images_set[key] = pygame.transform.smoothscale(
                        img_orig, (nouvelle_largeur, HAUTEUR_CIBLE)
                    )

            # Image initiale : état "up" (fruit montant)
            self.image = self.images_set.get("up", self.images_set.get("cut"))

        elif raw_image is not None:
            # Cas d'un fruit simple (sans états multiples)
            HAUTEUR_CIBLE = 160
            # Calcul du ratio pour conserver les proportions
            ratio = raw_image.get_width() / raw_image.get_height()
            nouvelle_largeur = int(HAUTEUR_CIBLE * ratio)
            # Redimensionnement
            self.image = pygame.transform.smoothscale(
                raw_image, (nouvelle_largeur, HAUTEUR_CIBLE)
            )
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
        self.speed_y = random.uniform(
            -20, -10
        )  # Vitesse verticale (vers le haut au départ)
        # Gravité pour simuler la chute
        self.gravity = gravity

        # Couleur de secours si pas d'image (pour debug)
        self.color = (255, 0, 0)
        if self.type == "banane":
            self.color = (255, 255, 0)
        elif self.type == "orange":
            self.color = (255, 165, 0)

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
                self.image = self.images_set.get(
                    "up", self.images_set.get("cut")
                )  # Fruit montant
            else:
                self.image = self.images_set.get(
                    "down", self.images_set.get("cut")
                )  # Fruit descendant

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
        """
        Méthode appelée lorsque le fruit est tranché par le joueur.
        
        CHANGEMENT PAR RAPPORT À L'ANCIENNE VERSION :
        Avant : Cette méthode changeait simplement l'image du fruit vers "cut"
        Maintenant : Elle retourne les informations nécessaires pour créer 2 morceaux séparés (objets MorceauFruit)
        
        Le fruit original sera supprimé de la liste mes_fruits par le controller,
        et 2 nouveaux MorceauFruit seront créés à la place.
        
        Returns:
            dict: Dictionnaire contenant les infos pour créer les morceaux
                - "x": position X du fruit au moment de la coupe
                - "y": position Y du fruit au moment de la coupe  
                - "image": l'image "cut" du fruit (moitié)
                
            None: Si le fruit n'a pas d'image "cut" disponible
        
        Exemple de retour:
            {
                "x": 450.5,
                "y": 320.0,
                "image": <Surface 80x80>
            }
        """
        # Marque le fruit comme tranché (empêche de le couper à nouveau)
        self.sliced = True

        # Vérifie si le fruit a un ensemble d'images (avec une version "cut")
        if self.images_set and "cut" in self.images_set:
            # Retourne les informations nécessaires pour créer les 2 morceaux
            return {
                "x": self.x,           # Position X actuelle du fruit
                "y": self.y,           # Position Y actuelle du fruit
                "image": self.images_set["cut"]  # Image de la moitié de fruit
            }
        
        # Si pas d'image "cut", retourne None
        # Dans ce cas, le controller supprimera simplement le fruit
        return None

    def draw(self, screen):
        # Affichage du fruit sur l'écran
        if self.image:
            # Centrage de l'image sur la position x,y
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
        else:
            # Affichage de secours : cercle coloré
            pygame.draw.circle(
                screen, self.color, (int(self.x), int(self.y)), self.radius
            )


class Glacon:
    def __init__(self, largeur, hauteur, zone_joueur=None, gravity=0.4):
        self.type = "ice"
        self.sliced = False
        self.images_set = None
        self.zone_joueur = zone_joueur

        self.radius = 40
        self.color = (173, 216, 230)  # Bleu clair

        # Gestion de l'image du glaçon
        raw_image = images.get("ice")
        if raw_image is not None:
            HAUTEUR_CIBLE = 120
            ratio = raw_image.get_width() / raw_image.get_height()
            nouvelle_largeur = int(HAUTEUR_CIBLE * ratio)
            self.image = pygame.transform.smoothscale(
                raw_image, (nouvelle_largeur, HAUTEUR_CIBLE)
            )
        else:
            self.image = None

        # Positionnement initial
        milieu_x = largeur // 2
        if zone_joueur == 1:
            self.x = random.randint(100, milieu_x - 100)
        elif zone_joueur == 2:
            self.x = random.randint(milieu_x + 100, largeur - 100)
        else:
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

        # Confinement aux zones en mode 2 joueurs
        if self.zone_joueur is not None:
            milieu_x = largeur_ecran // 2
            if self.zone_joueur == 1:
                if self.x + self.radius > milieu_x:
                    self.x = milieu_x - self.radius
                    self.speed_x *= -1
            elif self.zone_joueur == 2:
                if self.x - self.radius < milieu_x:
                    self.x = milieu_x + self.radius
                    self.speed_x *= -1

    def draw(self, surface):
        """Afficher l'image si disponible, sinon cercle bleu"""
        if self.image:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, rect)
        else:
            # Fallback : cercle bleu avec reflet
            pygame.draw.circle(
                surface, self.color, (int(self.x), int(self.y)), self.radius
            )
            pygame.draw.circle(
                surface, (255, 255, 255), (int(self.x - 10), int(self.y - 10)), 10
            )

    # Méthode appelée quand le glaçon est tranché
    def couper(self):
        """Méthode appelée quand le glaçon est tranché"""
        self.sliced = True

        # On peut ajouter un effet visuel ici si besoin
        self.speed_y = -5  # Petit saut visuel vers le haut après la coupe
        # Optionnel : changer l'image pour un glaçon brisé si disponible
        # (non implémenté ici pour simplification)


class Bombe:
    def __init__(self, largeur, hauteur, zone_joueur=None, gravity=0.4):
        self.type = "bombe"
        self.sliced = False
        self.images_set = None
        self.zone_joueur = zone_joueur

        self.radius = 40
        self.color = (50, 50, 50)  # Gris foncé (fallback)

        # --- Gestion de l'image bombe.png ---
        raw_image = images.get("bombe")
        if raw_image is not None:
            HAUTEUR_CIBLE = 80
            ratio = raw_image.get_width() / raw_image.get_height()
            nouvelle_largeur = int(HAUTEUR_CIBLE * ratio)
            self.image = pygame.transform.smoothscale(
                raw_image, (nouvelle_largeur, HAUTEUR_CIBLE)
            )
        else:
            self.image = None

        # --- Positionnement (même logique que Fruit) ---
        milieu_x = largeur // 2
        if zone_joueur == 1:
            self.x = random.randint(100, milieu_x - 100)
        elif zone_joueur == 2:
            self.x = random.randint(milieu_x + 100, largeur - 100)
        else:
            self.x = random.randint(100, largeur - 100)

        self.y = hauteur
        self.speed_x = random.uniform(-10, 10)
        self.speed_y = random.uniform(-20, -10)
        self.gravity = gravity

    def update(self, largeur_ecran, speed_factor=1):
        """Met à jour la bombe"""
        self.speed_y += self.gravity * speed_factor
        self.x += self.speed_x * speed_factor
        self.y += self.speed_y * speed_factor

        # Rebonds
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -1

        if self.x + self.radius > largeur_ecran:
            self.x = largeur_ecran - self.radius
            self.speed_x *= -1

        # Confinement aux zones
        if self.zone_joueur is not None:
            milieu_x = largeur_ecran // 2
            if self.zone_joueur == 1:
                if self.x + self.radius > milieu_x:
                    self.x = milieu_x - self.radius
                    self.speed_x *= -1
            elif self.zone_joueur == 2:
                if self.x - self.radius < milieu_x:
                    self.x = milieu_x + self.radius
                    self.speed_x *= -1

    def draw(self, surface):
        """Affiche la bombe"""
        if self.image:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, rect)
        else:
            # Fallback : cercle noir avec mèche
            pygame.draw.circle(
                surface, self.color, (int(self.x), int(self.y)), self.radius
            )
            # Mèche blanche
            pygame.draw.line(
                surface,
                (255, 255, 255),
                (int(self.x), int(self.y) - self.radius),
                (int(self.x), int(self.y) - self.radius - 20),
                3,
            )

    def couper(self):
        """Méthode appelée quand la bombe est tranchée"""
        self.sliced = True

class MorceauFruit:
    """
    Représente un morceau de fruit après tranchage.
    
    Attributs:
        x, y (float): Position du morceau sur l'écran
        image (Surface): Image du morceau (moitié de fruit)
        alpha (int): Opacité actuelle (255 = opaque, 0 = invisible)
        speed_x, speed_y (float): Vitesses horizontale et verticale
        gravity (float): Force de gravité appliquée
        angle (float): Angle de rotation actuel en degrés
        rotation_speed (float): Vitesse de rotation en degrés par frame
        fade_speed (int): Vitesse de disparition (réduction d'alpha par frame)
    """

    def __init__(self, x, y, image, direction="gauche"):
        """
        Crée un nouveau morceau de fruit.
        
        Args:
            x (float): Position X initiale (position du fruit au moment de la coupe)
            y (float): Position Y initiale (position du fruit au moment de la coupe)
            image (Surface): Image du fruit coupé (sera inversée si direction="droite")
            direction (str): "gauche" ou "droite" - détermine le sens de déplacement
        
        Exemple d'utilisation:
            # Quand un fruit est coupé, on crée 2 morceaux :
            morceau_gauche = MorceauFruit(fruit.x, fruit.y, image_cut, "gauche")
            morceau_droite = MorceauFruit(fruit.x, fruit.y, image_cut, "droite")
        """
        
        # Les 2 morceaux démarrent au même endroit (là où était le fruit)
        self.x = x
        self.y = y

        # ====================================================================
        # GESTION DE L'IMAGE SELON LA DIRECTION
        # ====================================================================
        # Pour le morceau GAUCHE : on garde l'image telle quelle
        # Pour le morceau DROIT : on inverse l'image horizontalement (miroir)
        # Cela donne l'illusion de 2 moitiés différentes !
        #
        # pygame.transform.flip(image, flip_x, flip_y)
        #   - flip_x = True  → inverse horizontalement (effet miroir)
        #   - flip_y = False → pas d'inversion verticale
        if direction == "gauche":
            self.image = image
        else:
            # Crée une copie inversée horizontalement pour le morceau droit
            self.image = pygame.transform.flip(image, True, False)

        # ====================================================================
        # OPACITÉ POUR L'EFFET FADE OUT
        # ====================================================================
        # L'alpha va de 255 (totalement visible) à 0 (invisible)
        # On le diminue progressivement à chaque frame
        self.alpha = 255

        # ====================================================================
        # PHYSIQUE DU MORCEAU - VITESSES
        # ====================================================================
        # Les vitesses sont OPPOSÉES selon la direction pour créer l'effet
        # de séparation (les 2 morceaux s'écartent l'un de l'autre)
        #
        # random.uniform(a, b) retourne un nombre décimal aléatoire entre a et b
        # Cela ajoute de la variété à chaque coupe !
        if direction == "gauche":
            # Morceau gauche : va vers la GAUCHE (vitesse X négative)
            self.speed_x = random.uniform(-6, -3)
            # Rotation dans le sens anti-horaire (négatif)
            self.rotation_speed = random.uniform(-8, -4)
        else:
            # Morceau droit : va vers la DROITE (vitesse X positive)
            self.speed_x = random.uniform(3, 6)
            # Rotation dans le sens horaire (positif)
            self.rotation_speed = random.uniform(4, 8)

        # Vitesse verticale initiale : légèrement vers le HAUT
        # Cela crée un petit "saut" avant que la gravité ne fasse retomber le morceau
        # Valeur négative = vers le haut (en pygame, Y augmente vers le bas)
        self.speed_y = random.uniform(-10, -5)

        # ====================================================================
        # PHYSIQUE DU MORCEAU - GRAVITÉ
        # ====================================================================
        # La gravité est ajoutée à speed_y à chaque frame
        # Plus la valeur est grande, plus le morceau tombe vite
        self.gravity = 0.6

        # ====================================================================
        # ROTATION
        # ====================================================================
        # L'angle de rotation commence à 0° et change à chaque frame
        # selon rotation_speed (défini ci-dessus selon la direction)
        self.angle = 0

        # ====================================================================
        # VITESSE DE DISPARITION (FADE OUT)
        # ====================================================================
        # À chaque frame, on soustrait fade_speed à alpha
        # Avec alpha=255 et fade_speed=6, le morceau disparaît en ~42 frames
        # À 60 FPS, cela fait environ 0.7 secondes
        # 
        # on peut ajuster cette valeur :
        #   - Plus grand (ex: 10) = disparition plus rapide
        #   - Plus petit (ex: 3) = disparition plus lente
        self.fade_speed = 6

    def update(self):
        """
        Met à jour la physique du morceau à chaque frame.
        
        Cette méthode doit être appelée une fois par frame dans la boucle
        principale du jeu. Elle gère :
            1. La gravité (le morceau accélère vers le bas)
            2. Le déplacement (position mise à jour selon les vitesses)
            3. La rotation (l'angle augmente/diminue)
            4. Le fade out (l'opacité diminue progressivement)
        
        Note: Pas besoin de passer de paramètres, tout est géré en interne.
        """
        # ====================================================================
        # ÉTAPE 1 : APPLIQUER LA GRAVITÉ
        # ====================================================================
        # On ajoute la gravité à la vitesse verticale
        # Cela simule l'accélération de la chute (comme dans la vraie vie !)
        # Chaque frame, le morceau tombe un peu plus vite
        self.speed_y += self.gravity

        # ====================================================================
        # ÉTAPE 2 : METTRE À JOUR LA POSITION
        # ====================================================================
        # On déplace le morceau selon ses vitesses actuelles
        # speed_x déplace horizontalement (gauche/droite)
        # speed_y déplace verticalement (haut/bas)
        self.x += self.speed_x
        self.y += self.speed_y

        # ====================================================================
        # ÉTAPE 3 : METTRE À JOUR LA ROTATION
        # ====================================================================
        # On ajoute la vitesse de rotation à l'angle actuel
        # Le morceau tourne continuellement sur lui-même
        self.angle += self.rotation_speed

        # ====================================================================
        # ÉTAPE 4 : APPLIQUER LE FADE OUT
        # ====================================================================
        # On diminue l'opacité progressivement
        # max(0, ...) empêche alpha de devenir négatif
        # Une fois à 0, le morceau est complètement invisible
        self.alpha = max(0, self.alpha - self.fade_speed)

    def draw(self, screen):
        """
        Dessine le morceau sur l'écran avec rotation et transparence.
        
        Cette méthode doit être appelée une fois par frame, APRÈS update().
        Elle gère :
            1. La rotation de l'image
            2. L'application de la transparence (alpha)
            3. Le centrage correct de l'image
        
        Args:
            screen (Surface): L'écran pygame sur lequel dessiner
        
        Note: Si alpha <= 0, rien n'est dessiné (optimisation)
        """
        # Si le morceau est complètement invisible, on ne dessine rien
        # Cela évite des calculs inutiles
        if self.alpha <= 0:
            return

        # ====================================================================
        # ÉTAPE 1 : ROTATION DE L'IMAGE
        # ====================================================================
        # pygame.transform.rotate(image, angle) retourne une NOUVELLE image
        # tournée de 'angle' degrés dans le sens anti-horaire
        # 
        # ATTENTION : La rotation change la taille de l'image !
        # Une image 100x100 tournée de 45° devient ~141x141
        # C'est pour ça qu'on recalcule le rect après
        image_tournee = pygame.transform.rotate(self.image, self.angle)

        # ====================================================================
        # ÉTAPE 2 : APPLICATION DE LA TRANSPARENCE
        # ====================================================================
        # Pour appliquer l'alpha à une image, on doit d'abord la convertir
        # avec convert_alpha() pour supporter la transparence par pixel
        #
        # IMPORTANT : On crée une copie pour ne pas modifier l'original
        # car set_alpha() modifie l'image en place
        image_avec_alpha = image_tournee.copy()
        image_avec_alpha.set_alpha(self.alpha)

        # ====================================================================
        # ÉTAPE 3 : CENTRAGE ET AFFICHAGE
        # ====================================================================
        # On récupère le rectangle de l'image et on le centre sur (x, y)
        # Cela garantit que la rotation se fait autour du centre du morceau
        # (sinon l'image "sauterait" à chaque changement d'angle)
        rect = image_avec_alpha.get_rect(center=(int(self.x), int(self.y)))

        # On dessine l'image sur l'écran à la position calculée
        screen.blit(image_avec_alpha, rect)

    def est_termine(self):
        """
        Vérifie si le morceau doit être supprimé.
        
        Un morceau est considéré comme "terminé" quand il est devenu
        complètement invisible (alpha <= 0). À ce moment, il peut être
        retiré de la liste des morceaux pour libérer de la mémoire.
        
        Returns:
            bool: True si le morceau est invisible et doit être supprimé, False sinon
        
        Exemple d'utilisation dans la boucle principale:
            # Supprimer les morceaux terminés
            morceaux_fruits = [m for m in morceaux_fruits if not m.est_termine()]
        """
        return self.alpha <= 0