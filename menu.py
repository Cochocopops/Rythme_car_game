import pygame 
import subprocess
import csv
from PIL import Image

# Screen dimensions
sizeX, sizeY = (444, 790)
screen = pygame.display.set_mode((sizeX, sizeY))

# Colors
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_LIGHT_GRAY = pygame.Color(200, 200, 200)
COLOR_ORANGE = pygame.Color(255, 152, 0)
COLOR_BACKGROUND = pygame.Color(30, 30, 30)

# Menu class
class Menu:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Rythme Car Game - Menu")
        self.clock = pygame.time.Clock()
        
        # Load background GIF
        try:
            self.frames = self.load_gif("data/assets/Intro.gif")
            self.frame_index = 0
        except FileNotFoundError:
            print("Error: GIF 'Intro.gif' not found.")
            self.frames = None

        # Load background music
        pygame.mixer.init()
        pygame.mixer.music.load("data/audio/Night Rider.mp3")
        pygame.mixer.music.play(-1)  # Loop playback

        # Initialize scores and inputs
        self.best_score = 0  # Best score
        self.last_score = None  # Last score from the previous game (None means no game played yet)
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)  # Font for the last score
        self.name_active = True  # Enable name input
        self.age_active = False  # Enable age input after name
        self.player_name = ""
        self.player_age = ""
        self.play_button_active = False  # Activate the Play button only after inputs are complete
        self.showing_scores = False  # Flag to indicate score table is displayed

    def load_gif(self, path):
        """Load GIF and extract frames as pygame surfaces."""
        gif = Image.open(path)
        frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_surface = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
            frames.append(frame_surface)
        return frames

    def draw_background(self):
        """Display GIF animation as background."""
        if self.frames:
            screen.blit(self.frames[self.frame_index], (0, 0))
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw_text(self, text, x, y, color=COLOR_WHITE, font=None):
        """Display centered text."""
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    def display_scores_table(self):
        """Display the table of scores."""
        self.showing_scores = True
        try:
            with open("scores.csv", "r") as file:
                scores = list(csv.reader(file))
        except FileNotFoundError:
            scores = [["Name", "Date", "Score"]]  # Default header

        # Display scores on a new background
        self.draw_background()
        title_font = pygame.font.Font(None, 48)
        self.draw_text("Player Scores", sizeX // 2, 50, COLOR_ORANGE, title_font)

        for i, row in enumerate(scores):
            row_text = "   ".join(row)
            color = COLOR_ORANGE if i == 0 else COLOR_WHITE  # Highlight the header
            self.draw_text(row_text, sizeX // 2, 100 + i * 30, color)

        pygame.display.update()

    def display(self):
        """Display the main menu with text, scores, and buttons."""
        self.draw_background()

        # Display the best score at the top
        self.draw_text(f"Meilleur Score: {self.best_score}", sizeX // 2, 50)

        # Draw "Show Scores" button below the best score
        scores_button_color = COLOR_LIGHT_GRAY  # Discreet button
        pygame.draw.rect(screen, scores_button_color, (sizeX // 2 - 75, 100, 150, 50), border_radius=10)
        self.draw_text("Scores", sizeX // 2, 125, COLOR_BLACK)

        # Display the last score slightly above the center, only if a game has been played
        if self.last_score is not None:
            self.draw_text(str(self.last_score), sizeX // 2, sizeY // 2 - 50, COLOR_WHITE, self.large_font)

        # Show prompt for entering name or age
        if self.name_active:
            self.draw_text("Entrez votre nom:", sizeX // 2, sizeY - 200)
            name_surface = self.font.render(self.player_name, True, COLOR_ORANGE)
            screen.blit(name_surface, (sizeX // 2 - name_surface.get_width() // 2, sizeY - 170))
        elif self.age_active:
            self.draw_text("Entrez votre âge:", sizeX // 2, sizeY - 200)
            age_surface = self.font.render(self.player_age, True, COLOR_ORANGE)
            screen.blit(age_surface, (sizeX // 2 - age_surface.get_width() // 2, sizeY - 170))

        # Draw "Play" button
        play_button_color = COLOR_ORANGE
        pygame.draw.rect(screen, play_button_color, (sizeX // 2 - 75, sizeY - 120, 150, 50), border_radius=10)
        self.draw_text("Play", sizeX // 2, sizeY - 95)

# Create the Menu object
menu = Menu()

# Main menu loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if menu.showing_scores:
                if event.key == pygame.K_RETURN:
                    menu.showing_scores = False  # Return to main menu
            elif menu.name_active:
                if event.key == pygame.K_BACKSPACE:
                    menu.player_name = menu.player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if menu.player_name.strip():
                        menu.name_active = False  # Disable name input
                        menu.age_active = True    # Enable age input
                else:
                    menu.player_name += event.unicode
            elif menu.age_active:
                if event.key == pygame.K_BACKSPACE:
                    menu.player_age = menu.player_age[:-1]
                elif event.key == pygame.K_RETURN:
                    if menu.player_age.strip().isdigit():
                        menu.age_active = False  # Disable age input
                        menu.play_button_active = True  # Activate "Play" button
                        pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "game.py"])  # Launch the game
                        running = False  # Exit menu loop after launching the game
                else:
                    if event.unicode.isdigit():  # Allow only digits for age input
                        menu.player_age += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if menu.showing_scores:
                continue  # Ignore mouse clicks while showing scores

            # Check if "Play" button is clicked
            if sizeX // 2 - 75 <= mouse_x <= sizeX // 2 + 75 and sizeY - 120 <= mouse_y <= sizeY - 70:
                if menu.play_button_active:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    subprocess.run(["python", "game.py"])
                    running = False  # Exit menu loop after launching the game

            # Check if "Scores" button is clicked
            if sizeX // 2 - 75 <= mouse_x <= sizeX // 2 + 75 and 100 <= mouse_y <= 150:
                menu.display_scores_table()

    if running and not menu.showing_scores:
        menu.display()
    pygame.display.flip()
    menu.clock.tick(10)

pygame.mixer.music.stop()
pygame.quit()