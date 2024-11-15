import pygame
from pygame.locals import *
import random
import subprocess  # Importer subprocess pour exécuter un autre script Python

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
COLOR_DARK_ORANGE = (255, 123, 0)

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
paused = False  # État de pause
lane_marker_move_y = 0  # Initialiser le mouvement des marqueurs de voie
menu_button_pressed = False  # État du bouton Menu pour l'animation

# Position et dimensions du bouton Menu (centré)
menu_button_rect = pygame.Rect(width // 2 - 75, height // 2 - 25, 150, 50)

# Position du bouton stop/start pour alignement symétrique avec le score
stop_start_text_pos = (width - 60, 20)

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

# Fonction pour retourner au menu
def return_to_menu():
    """Quitte le jeu et retourne au menu."""
    pygame.quit()  # Quitter Pygame proprement
    subprocess.call(["python", "menu.py"])  # Lancer le menu
    exit()  # Terminer le processus actuel

# Boucle principale du jeu
running = True
while running:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            # Vérifier si le bouton Menu est cliqué
            if paused and menu_button_rect.collidepoint(event.pos):
                menu_button_pressed = True  # Activer l'animation de clic
                print("Retour au menu")
                return_to_menu()
            elif pygame.Rect(stop_start_text_pos[0], stop_start_text_pos[1], 50, 30).collidepoint(event.pos):
                paused = not paused
                pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()
        elif event.type == MOUSEBUTTONUP and menu_button_pressed:
            menu_button_pressed = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                paused = not paused
                pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()
            elif event.key == K_RETURN and paused:  # Si la touche Entrée est pressée en pause
                print("Retour au menu via Entrée")
                return_to_menu()
            elif event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

    if not paused:
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
                vehicle = Vehicle(image, lane, height / -2)
                vehicle_group.add(vehicle)
        for vehicle in vehicle_group:
            vehicle.rect.y += speed
            if vehicle.rect.top >= height:
                vehicle.kill()
                score += 1
                if score % 5 == 0:
                    speed += 1
        vehicle_group.draw(screen)

        # Afficher le score
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        score_text = font.render('Score: ' + str(score), True, COLOR_TEXT)
        screen.blit(score_text, (20, 20))
        
        # Vérifier les collisions
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            pygame.mixer.music.stop()
            explosion_sound.play()
            crash_rect.center = player.rect.center
            
    # Afficher le texte Stop ou Start
    stop_start_text = font.render("Start" if paused else "Stop", True, COLOR_TEXT)
    screen.blit(stop_start_text, stop_start_text_pos)

    # Afficher le bouton Menu si le jeu est en pause
    if paused:
        menu_button_color = COLOR_DARK_ORANGE if menu_button_pressed else COLOR_ORANGE
        pygame.draw.rect(screen, menu_button_color, menu_button_rect, border_radius=10)
        menu_text = font.render("Menu", True, COLOR_TEXT)
        screen.blit(menu_text, menu_text.get_rect(center=menu_button_rect.center))

    pygame.display.update()

# Quitter Pygame
pygame.mixer.music.stop()
pygame.quit()
