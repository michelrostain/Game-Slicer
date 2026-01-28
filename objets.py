import pygame, random
from constantes import images

class Fruit:
    def __init__(self, type_de_fruit, largeur, hauteur):
        self.type=type_de_fruit
        # Association de l'image aux types de fruits sélectionnés
        images_trouvees = images.get(self.type)
        # Redimensionnement de l'image
        if images_trouvees is not None:
            self.image=pygame.transform.scale(images_trouvees, (100, 100))
        else:
            self.image=None

        # Récupération de la hauteur pour s'adapter au mode plein écran
        # surface_actuelle = pygame.display.get_surface()
        # largeur, hauteur = surface_actuelle.get_size()

        # 1. Apparence
        self.radius = 30
        
        # 2. Position de départ (en bas de l'écran) en cours, suivant plein écran ou pas
        self.x = random.randint(100, largeur-100)
        self.y = hauteur  
        
        # 3. Physique du saut
        # Vitesse horizontale (un peu vers la gauche ou la droite)
        self.speed_x = random.uniform(-10, 10) 
        # Vitesse verticale (impulsion vers le haut, donc négative)
        self.speed_y = random.uniform(-40, -14) 
        self.color="white"
        
        self.gravity = 0.4
        self.radius = 30
        # if type_de_fruit == ("pomme"):
        #     self.color= ("green")
        if type_de_fruit == ("poire"):
            self.color = ("blue")
        if type_de_fruit == ("orange"):
            self.color = ("orange")
        if type_de_fruit == ("banane"):
            self.color = ("yellow")


    def update(self, largeur_ecran):
        # On applique la gravité à la vitesse verticale
        self.speed_y += self.gravity
        
        # On met à jour la position avec les vitesses
        self.x += self.speed_x
        self.y += self.speed_y

        # Gestion du rebond à gauche
        if self.x - self.radius <0:
            self.x=self.radius
            self.speed_x*=-1

        # Gestion du rebond à droite
        if self.x + self.radius > largeur_ecran:
            self.x=largeur_ecran-self.radius
            self.speed_x*=-1


    def draw(self, surface):
        # On importe l'image
        if self.image:
            surface.blit(self.image, (int(self.x) -50, int(self.y)-50)) # les "-25" servent à ventrer la photo au centre. Notre rescale étant de 50 par 50, on a donc le centre qui est à 25.
        else :
        # Si image pas trouvée
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        


class bombe:
    def __init__(self):
        # 1. Apparence
        self.radius = 40
        self.color = (255, 255, 255) 


class ice:
    def __init__(self):
        self.radius = 40
        self.color = (255, 255, 255) 
