import pygame 
from pygame.locals import *
import random

pygame.init()

# Dimensions de la fenêtre adaptées au menu
width, height = (444, 790)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Car Game')

# Couleurs
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Taille de la route et des marquages
road_width = 300
marker_width = 10
marker_height = 50

# Coordonnées des voies
left_lane = 122  # Position de la première voie (gauche)
center_lane = 222
right_lane = 322
lanes = [left_lane, center_lane, right_lane]

# Route et marquages de bord
road = (72, 0, road_width, height)
left_edge_marker = (67, 0, marker_width, height)
right_edge_marker = (367, 0, marker_width, height)

# Pour animer le mouvement des marquages de voie
lane_marker_move_y = 0

# Coordonnées de départ du joueur
player_x = 222
player_y = 600

# Paramètres de la fenêtre et de la boucle de jeu
clock = pygame.time.Clock()
fps = 120

# Paramètres du jeu
gameover = False
speed = 2
score = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Redimensionner l'image pour qu'elle ne soit pas plus large que la voie
        image_scale = 45 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)

# Groupes de sprites
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Création de la voiture du joueur
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Charger les images des véhicules
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = [pygame.image.load('images/' + image_filename) for image_filename in image_filenames]

# Charger l'image de crash
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

# Boucle principale du jeu
running = True
while running:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Déplacer la voiture du joueur avec les flèches gauche/droite
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                
            # Vérifier les collisions latérales après le changement de voie
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

    # Dessiner l'herbe
    screen.fill(green)
    
    # Dessiner la route
    pygame.draw.rect(screen, gray, road)
    
    # Dessiner les marquages de bord
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)
    
    # Dessiner les marquages de voie
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        
    # Dessiner la voiture du joueur
    player_group.draw(screen)
    
    # Ajouter un véhicule
    if len(vehicle_group) < 2:
        add_vehicle = all(vehicle.rect.top >= vehicle.rect.height * 1.5 for vehicle in vehicle_group)
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
    
    # Déplacer les véhicules
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            if score > 0 and score % 5 == 0:
                speed += 1
    
    # Dessiner les véhicules
    vehicle_group.draw(screen)
    
    # Afficher le score
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    text = font.render('Score: ' + str(score), True, white)
    screen.blit(text, (20, 20))
    
    # Vérifier les collisions frontales
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
            
    # Afficher "Game Over" si le joueur a perdu
    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, height // 2 - 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text = font.render('Game over. Play again? (Y/N)', True, white)
        text_rect = text.get_rect(center=(width / 2, height / 2))
        screen.blit(text, text_rect)
            
    pygame.display.update()

    # Attendre l'entrée de l'utilisateur pour rejouer ou quitter
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    gameover = False
                    running = False

pygame.quit()
