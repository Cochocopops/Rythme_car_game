# Rythme Car Game - README

## Vue d'ensemble

**Rythme Car Game** est un jeu de rythme où les joueurs conduisent une voiture tout en évitant des obstacles sur la route, avec pour objectif d'obtenir le meilleur score. Le jeu inclut un menu interactif, un système de gestion des scores, et un gameplay immersif avec musique de fond et effets sonores.

## Vidéos de démonstration

### Vidéo 1
[Vidéo 1 - Lien GitHub](https://github.com/user-attachments/assets/6bf89fb6-f086-4fa7-92a2-c2b34a57e060)

### Vidéo 2
[Vidéo 2 - Lien GitHub](https://github.com/user-attachments/assets/fcab05fe-a906-4d64-b7c5-7173061e4e29)

---

## Fonctionnalités

- **Menu dynamique** :  
  - Fond animé avec un GIF.  
  - Musique de fond : "Night Rider".  
  - Champs pour saisir le nom et l'âge du joueur.  
  - Affichage du meilleur score des sessions précédentes.  
  - Accès au tableau des 5 meilleurs scores.

- **Mécanismes de jeu** :  
  - Contrôlez une voiture qui peut changer de voie.  
  - Des véhicules apparaissent aléatoirement en tant qu'obstacles.  
  - La partie se termine en cas de collision.  
  - La difficulté augmente avec le score.

- **Écran de fin de partie** :  
  - Affiche le score final du joueur.  
  - Option pour retourner au menu.

- **Pause** :  
  - Mettez le jeu en pause ou reprenez avec la barre d'espace.

- **Gestion des scores** :  
  - Les scores des joueurs sont sauvegardés dans un fichier CSV.  
  - Les meilleurs scores sont affichés dans le menu.

---

## Pré-requis

Le projet nécessite les dépendances suivantes (listées dans `requirements.txt`) :
- **Pillow** (11.0.0) - Pour le traitement des GIFs.
- **pygame** (2.6.1) - Pour le développement du jeu.

Installez les dépendances avec :
```bash
pip install -r requirements.txt
```
---

## Instructions de jeu

### Navigation dans le menu :
- Entrez votre nom et votre âge.
- Cliquez sur **"Play"** ou appuyez sur Entrée pour commencer la partie.
- Accédez aux 5 meilleurs scores en cliquant sur le bouton **"Scores"**.

### Contrôles du jeu :
- **Déplacer la voiture à gauche** : Flèche gauche.
- **Déplacer la voiture à droite** : Flèche droite.
- **Pause/Reprendre** : Barre d'espace.
- **Retourner au menu** : Touche Entrée (après *"Game Over"*).

### Objectif :
Évitez les collisions et obtenez le score le plus élevé possible.

---

## Notes pour les développeurs

### Assets utilisés :
- **Fond GIF** : `data/assets/Intro.gif`
- **Musique** :
  - Menu : `data/audio/Night Rider.mp3`
  - Jeu : `data/audio/Game.mp3`
  - Collision : `data/audio/Explosion.mp3`
- **Sprites des voitures** : `data/assets/`

### Gestion des scores :
- Les scores sont mis à jour dynamiquement dans `scores.csv`.
- Seule la session la plus récente d’un joueur est mise à jour.

### Améliorations futures :
- Ajouter davantage de types de véhicules et des obstacles dynamiques.
- Implémenter un mode multijoueur.
- Améliorer les visuels et les animations des collisions.

---

## Liens utiles
- **Prototype Figma** : [Car Rhythm Game - Figma](https://www.figma.com/design/kj3WOnmfUVPsRU5jTDYrFH/Car-Rhythm-Game?node-id=0-1&m=dev&t=ZsFqjizqDA1D8xZb-1)



