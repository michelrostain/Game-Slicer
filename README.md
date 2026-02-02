# 🍉 Game Slicer

Un jeu de type "Fruit Ninja" développé en Python avec Pygame ! Tranchez des fruits, évitez les bombes et tentez de battre le meilleur score !

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Description

**Game Slicer** est un jeu d'arcade où le joueur doit trancher un maximum de fruits en les découpant avec la souris ou le clavier. Le jeu propose deux modes :

- **Mode 1 Joueur** : Jouez seul et tentez de battre votre meilleur score !
- **Mode 2 Joueurs** : Affrontez un ami en écran partagé !

### ✨ Fonctionnalités

- 🍎 **4 types de fruits** : Pommes, Poires, Bananes et Oranges avec des animations expressives
- 💣 **Bonus Bombe** : Attention ! Trancher une bombe = Game Over !
- 🧊 **Bonus Glace (Ice)** : Gèle l'écran pendant 3 à 5 secondes aléatoirement
- 📈 **Système de niveaux** : La difficulté augmente progressivement (gravité et vitesse)
- 🎯 **Système de combo** : Tranchez plusieurs fruits d'un coup pour obtenir des bonus !
- 🏆 **Tableau des scores** : Sauvegarde automatique des meilleurs scores
- 🎵 **Effets sonores** : Sons immersifs pour chaque action
- 🎨 **Animations** : Particules d'explosion, effets de gel, fruits coupés animés

## 🛠️ Installation

### Prérequis

Avant d'installer le jeu, assurez-vous d'avoir **Python 3.x** installé sur votre ordinateur.

#### Vérifier si Python est installé

Ouvrez un terminal (ou invite de commandes) et tapez :

```bash
python --version
```

ou

```bash
python3 --version
```

Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/).

### Étape 1 : Cloner le repository

```bash
git clone https://github.com/michelrostain/Game-Slicer.git
cd Game-Slicer
```

### Étape 2 : Créer un environnement virtuel (recommandé)

**Sur Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**Sur macOS/Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer Pygame

Le jeu utilise uniquement **Pygame** comme dépendance externe. Installez-le avec pip :

```bash
pip install pygame
```

> 💡 **Note pour les débutants** : Si la commande `pip` ne fonctionne pas, essayez `pip3` ou `python -m pip install pygame`

### Étape 4 : Lancer le jeu

```bash
python main.py
```

ou

```bash
python3 main.py
```

## 🎮 Comment jouer ?

### Mode 1 Joueur

| Action | Contrôle |
|--------|----------|
| Trancher les fruits | **Clic gauche maintenu** + déplacer la souris |

### Mode 2 Joueurs

| Joueur | Touches |
|--------|---------|
| **Joueur 1** (gauche) | Z, E, S, D |
| **Joueur 2** (droite) | ↑, ↓, ←, → (flèches directionnelles) |

### Règles du jeu

1. **Tranchez les fruits** pour marquer des points
2. **Évitez les bombes** 💣 - Si vous en tranchez une, c'est Game Over !
3. **Attrapez les glaçons** 🧊 - Ils gèlent l'écran temporairement (avantage !)
4. **Faites des combos** - Tranchez plusieurs fruits d'un coup pour des bonus :
   - 3+ fruits = +1 point bonus par fruit supplémentaire

### Système de niveaux

La difficulté augmente au fil du jeu :
- La **gravité** des fruits augmente
- La **vitesse** de spawn augmente
- Plus de fruits apparaissent simultanément

## 📁 Structure du projet

```
Game-Slicer/
├── Assets/
│   ├── Images/
│   │   ├── Backgrounds/      # Fonds d'écran
│   │   ├── Fruits/           # Images des fruits (angry, scared, cut)
│   │   └── Special/          # Images bombe et glace
│   └── Sounds/               # Effets sonores
├── main.py                   # Point d'entrée du jeu
├── constantes.py             # Configuration et chargement des assets
├── objets.py                 # Classes Fruit, Bombe, Glacon, Particules
├── controller.py             # Gestion du slicing et des contrôles
├── interface.py              # Boutons et interface utilisateur
├── scores.py                 # Gestion des scores (sauvegarde JSON)
├── scores.json               # Fichier de sauvegarde des scores
└── .gitignore
```

## 🔧 Dépannage

### "pygame not found" ou "ModuleNotFoundError: No module named 'pygame'"

Réinstallez Pygame :
```bash
pip uninstall pygame
pip install pygame
```

### Le jeu ne trouve pas les images

Assurez-vous d'être dans le bon répertoire avant de lancer le jeu :
```bash
cd chemin/vers/Game-Slicer
python main.py
```

### L'écran est noir ou le jeu freeze

- Vérifiez que votre version de Python est 3.7 ou supérieure
- Mettez à jour Pygame : `pip install --upgrade pygame`

## 👥 Collaborateurs

Ce projet a été développé par :

| Contributeur | GitHub |
|--------------|--------|
| **Michel Rostain** | [@michelrostain](https://github.com/michelrostain) |
| **Manon Sigaud** | [@Manonsigilla](https://github.com/Manonsigilla) 
| **Ahamada Assmine** | [@AAssmine](https://github.com/AAssmine) 

## 📜 Licence

Ce projet est sous licence libre. Vous êtes libre de l'utiliser, le modifier et le distribuer.

## 🙏 Remerciements

- Inspiré par le célèbre jeu **Fruit Ninja**
- Développé avec ❤️ en Python et Pygame

---

**Amusez-vous bien et que le meilleur trancheur gagne ! 🍉🔪**
