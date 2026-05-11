import pygame
import sys

# Initialize Pygame
pygame.init()

# Setup the window (Retro resolution, then scaled up)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OpoSqueue - HPC Dashboard")

# Colors
BG_COLOR = (30, 30, 30)  # Dark grey
WHITE = (255, 255, 255)

# Load your Logo
try:
    logo = pygame.image.load("assets/logo.png").convert_alpha()
    # Scale it up if it's too small (keeping the pixels sharp)
    logo = pygame.transform.scale(logo, (logo.get_width() * 4, logo.get_height() * 4))
except:
    logo = None
    print("Logo not found in assets/")

def main_menu():
    while True:
        screen.fill(BG_COLOR)
        
        # Draw Logo
        if logo:
            screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, 50))
        
        # Simple placeholder for "Opossum waiting for bus"
        pygame.draw.rect(screen, (100, 100, 100), (500, 300, 200, 250)) # Opossum placeholder
        
        # Draw Buttons (Simplified for now)
        font = pygame.font.SysFont("Courier", 24)
        options = ["NEW CONNECTION", "SAVED", "DOCUMENTATION", "EXIT"]
        
        for i, text in enumerate(options):
            label = font.render(text, True, WHITE)
            screen.blit(label, (100, 300 + (i * 50)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()