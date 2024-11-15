import pygame
import subprocess
import csv
from PIL import Image
from datetime import datetime

# Screen dimensions
sizeX, sizeY = (444, 790)
screen = pygame.display.set_mode((sizeX, sizeY))

# Colors
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_ORANGE = pygame.Color(255, 152, 0)
COLOR_BACKGROUND = pygame.Color(30, 30, 30)
COLOR_LINE = pygame.Color(100, 100, 100)

# Menu class
class Menu:
    def __init__(self):
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
        pygame.mixer.music.play(-1)

        # Initialize scores and inputs
        self.best_score = self.get_best_score()  # Get the best score from CSV
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.name_active = True
        self.age_active = False
        self.player_name = ""
        self.player_age = ""
        self.play_button_active = False

        # Position of "Scores" button for top 5 scores
        self.scores_button_rect = pygame.Rect(sizeX // 2 - 75, 90, 150, 50)

    def load_gif(self, path):
        gif = Image.open(path)
        frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_surface = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
            frames.append(frame_surface)
        return frames

    def draw_background(self):
        if self.frames:
            screen.blit(self.frames[self.frame_index], (0, 0))
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw_text(self, text, x, y, color=COLOR_WHITE, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    def get_best_score(self):
        """Retrieve the highest score from scores.csv."""
        try:
            with open("scores.csv", "r") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header if present
                scores = [int(row[3]) for row in reader if row[3].isdigit()]
            return max(scores) if scores else 0
        except (FileNotFoundError, ValueError):
            return 0

    def save_user_data(self):
        """Save the user's name, age, current date, and initial score to scores.csv."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("scores.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.player_name, self.player_age, current_date, "0"])

    def display_scores_table(self):
        """Display the top 5 scores with names, dates (day/month/year format), and scores in a structured table."""
        try:
            with open("scores.csv", "r") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header if present
                scores = sorted(reader, key=lambda x: int(x[3]), reverse=True)[:5]
        except FileNotFoundError:
            scores = [["Nom", "Date", "Score"]]  # Default header if no scores

        # Display the GIF background and top scores
        score_running = True
        while score_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    score_running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    score_running = False

            # Draw GIF background
            if self.frames:
                screen.blit(self.frames[self.frame_index], (0, 0))
                self.frame_index = (self.frame_index + 1) % len(self.frames)

            # Display title centered
            title_font = pygame.font.Font(None, 48)
            self.draw_text("Top 5 Scores", sizeX // 2, 100, COLOR_ORANGE, title_font)

            # Column headers
            header_font = pygame.font.Font(None, 36)
            self.draw_text("Nom", sizeX // 5, 160, COLOR_ORANGE, header_font)
            self.draw_text("Date", sizeX // 2, 160, COLOR_ORANGE, header_font)
            self.draw_text("Score", 4 * sizeX // 5, 160, COLOR_ORANGE, header_font)

            # Display top scores
            for i, row in enumerate(scores):
                name, date_str, score = row[0], row[2].split()[0], row[3]
                formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%y")
                y_position = 200 + i * 40
                self.draw_text(name, sizeX // 5, y_position, COLOR_WHITE)
                self.draw_text(formatted_date, sizeX // 2, y_position, COLOR_WHITE)
                self.draw_text(score, 4 * sizeX // 5, y_position, COLOR_WHITE)

            pygame.display.update()
            self.clock.tick(10)

    def display(self):
        self.draw_background()
        self.draw_text(f"Meilleur Score: {self.best_score}", sizeX // 2, 50)

        # "Scores" button
        pygame.draw.rect(screen, COLOR_WHITE, self.scores_button_rect, border_radius=10)
        self.draw_text("Scores", sizeX // 2, 115, COLOR_BLACK)

        if self.name_active:
            self.draw_text("Entrez votre nom:", sizeX // 2, sizeY - 200)
            name_surface = self.font.render(self.player_name, True, COLOR_ORANGE)
            screen.blit(name_surface, (sizeX // 2 - name_surface.get_width() // 2, sizeY - 170))
        elif self.age_active:
            self.draw_text("Entrez votre âge:", sizeX // 2, sizeY - 200)
            age_surface = self.font.render(self.player_age, True, COLOR_ORANGE)
            screen.blit(age_surface, (sizeX // 2 - age_surface.get_width() // 2, sizeY - 170))

        # "Play" button
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
            if menu.name_active:
                if event.key == pygame.K_BACKSPACE:
                    menu.player_name = menu.player_name[:-1]
                elif event.key == pygame.K_RETURN and menu.player_name.strip():
                    menu.name_active = False
                    menu.age_active = True
                else:
                    menu.player_name += event.unicode
            elif menu.age_active:
                if event.key == pygame.K_BACKSPACE:
                    menu.player_age = menu.player_age[:-1]
                elif event.key == pygame.K_RETURN and menu.player_age.strip().isdigit():
                    menu.age_active = False
                    menu.play_button_active = True
                    menu.save_user_data()
                    pygame.mixer.music.stop()
                    pygame.quit()
                    subprocess.run(["python", "game.py", menu.player_name, menu.player_age])
                    running = False
                else:
                    if event.unicode.isdigit():
                        menu.player_age += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if menu.play_button_active and (sizeX // 2 - 75 <= mouse_x <= sizeX // 2 + 75 and sizeY - 120 <= mouse_y <= sizeY - 70):
                pygame.mixer.music.stop()
                pygame.quit()
                subprocess.run(["python", "game.py", menu.player_name, menu.player_age])
                running = False
            elif menu.scores_button_rect.collidepoint(mouse_x, mouse_y):
                menu.display_scores_table()

    if running:
        menu.display()
    pygame.display.flip()
    menu.clock.tick(10)

pygame.quit()
