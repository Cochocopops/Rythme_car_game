import pygame
from pygame.locals import *
import random
import subprocess
import csv
from datetime import datetime

# Variables globales pour l'utilisateur
player_name = "Player"  # Ce nom doit être récupéré de `menu.py` dans un contexte intégré
player_score = 0

# Initialiser Pygame et la musique
pygame.init()
pygame.mixer.init()

# Dimensions de la fenêtre
width, height = (444, 790)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Car Game')

# Charger et jouer la musique en boucle
pygame.mixer.music.load("data/audio/Game.mp3")
pygame.mixer.music.play(-1)

# Charger le son d'explosion
explosion_sound = pygame.mixer.Sound("data/audio/Explosion.mp3")

# Couleurs pour l'interface
COLOR_BACKGROUND = (30, 30, 30)
COLOR_ROAD = (50, 50, 70)
COLOR_MARKER = (70, 70, 90)
COLOR_TEXT = (200, 200, 200)
COLOR_ORANGE = (255, 152, 0)
COLOR_CRASH = (255, 0, 0)
COLOR_BUTTON_TEXT = (255, 255, 255)

# Largeur de la route et positions des voies
road_width = 300
left_lane = 122
center_lane = 222
right_lane = 322
lanes = [left_lane, center_lane, right_lane]

# Position de départ du joueur
player_x = 222
player_y = 600

# Variables de jeu
clock = pygame.time.Clock()
fps = 120
gameover = False
speed = 2
score = 0
paused = False
lane_marker_move_y = 0

# Position pour le texte Start/Stop et bouton Menu
start_stop_text_pos = (width - 100, 20)
menu_button_rect = pygame.Rect(width // 2 - 75, height // 2 + 100, 150, 50)

# Classes de véhicules
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_scale = 45 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('data/assets/car.png')
        super().__init__(image, x, y)

# Groupes de sprites pour le joueur et les autres véhicules
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Création du véhicule joueur
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Charger les images des autres véhicules
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = [pygame.image.load('data/assets/' + img) for img in image_filenames]

# Charger l'image de crash
crash = pygame.image.load('data/assets/crash.png')
crash_rect = crash.get_rect()

# Fonction pour enregistrer le score final dans scores.csv
def save_score():
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scores.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([player_name, "", current_date, score])

# Fonction pour retourner au menu
def return_to_menu():
    save_score()  # Sauvegarder le score avant de quitter
    pygame.quit()
    subprocess.call(["python", "menu.py"])
    exit()

# Boucle principale du jeu
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and not gameover:
                paused = not paused
                pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()
            elif event.key == K_RETURN and gameover:  # Retour au menu depuis le Game Over
                return_to_menu()
            elif event.key == K_LEFT and not paused and not gameover and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and not paused and not gameover and player.rect.center[0] < right_lane:
                player.rect.x += 100
        elif event.type == MOUSEBUTTONDOWN:
            # Vérifie si le bouton "Menu" est cliqué
            if gameover and menu_button_rect.collidepoint(event.pos):
                return_to_menu()
            # Vérifie si le texte Start/Stop est cliqué en haut à droite
            if start_stop_text_pos[0] <= event.pos[0] <= start_stop_text_pos[0] + 80 and start_stop_text_pos[1] <= event.pos[1] <= start_stop_text_pos[1] + 30 and not gameover:
                paused = not paused
                pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()

    if not paused and not gameover:
        # Dessiner l'arrière-plan et la route
        screen.fill(COLOR_BACKGROUND)
        pygame.draw.rect(screen, COLOR_ROAD, (72, 0, road_width, height))

        # Dessiner les marqueurs de voie
        lane_marker_move_y = (lane_marker_move_y + speed * 2) % (50 * 2)
        for y in range(-100, height, 100):
            pygame.draw.rect(screen, COLOR_MARKER, (left_lane + 45, y + lane_marker_move_y, 10, 50))
            pygame.draw.rect(screen, COLOR_MARKER, (center_lane + 45, y + lane_marker_move_y, 10, 50))

        # Mettre à jour et dessiner le joueur
        player_group.draw(screen)

        # Ajouter et déplacer les autres véhicules
        if len(vehicle_group) < 2:
            if all(vehicle.rect.top >= vehicle.rect.height * 1.5 for vehicle in vehicle_group):
                lane = random.choice(lanes)
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, -100)
                vehicle_group.add(vehicle)

        for vehicle in vehicle_group:
            vehicle.rect.y += speed
            if vehicle.rect.top >= height:
                vehicle.kill()
                score += 1
                if score % 5 == 0:
                    speed += 1
        vehicle_group.draw(screen)

        # Vérifier les collisions
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            pygame.mixer.music.stop()
            explosion_sound.play()
            crash_rect.center = player.rect.center

    # Afficher le score en jeu
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    score_text = font.render(f'Score: {score}', True, COLOR_TEXT)
    screen.blit(score_text, (20, 20))

    # Afficher le texte "Start" ou "Stop" en haut à droite, similaire au score
    start_stop_text = "Start" if paused else "Stop"
    start_stop_display = font.render(start_stop_text, True, COLOR_BUTTON_TEXT)
    screen.blit(start_stop_display, start_stop_text_pos)

    # Gestion du Game Over
    if gameover:
        # Afficher "GAME OVER" en haut
        screen.blit(crash, crash_rect)
        gameover_font = pygame.font.Font(None, 72)
        gameover_text = gameover_font.render("GAME OVER", True, COLOR_CRASH)
        screen.blit(gameover_text, gameover_text.get_rect(center=(width // 2, height // 2 - 100)))

        # Afficher le score centré, en blanc, avec une taille de police plus grande
        score_font = pygame.font.Font(None, 48)
        final_score_text = score_font.render(f"Score : {score}", True, COLOR_BUTTON_TEXT)
        screen.blit(final_score_text, final_score_text.get_rect(center=(width // 2, height // 2)))

        # Afficher le bouton "Menu" (style similaire au bouton Play)
        pygame.draw.rect(screen, COLOR_ORANGE, menu_button_rect, border_radius=10)
        button_text = font.render("Menu", True, COLOR_BUTTON_TEXT)
        screen.blit(button_text, button_text.get_rect(center=menu_button_rect.center))

    pygame.display.update()

# Quitter Pygame
pygame.mixer.music.stop()
pygame.quit()
