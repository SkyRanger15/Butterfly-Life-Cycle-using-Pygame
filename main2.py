import pygame
import os

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Butterfly Life Cycle Animation")

# Load images
leaf_states = [pygame.image.load(f"leaf_{i}.png") for i in range(1, 6)]
caterpillar = pygame.image.load("caterpillar.png")
cocoon = pygame.image.load("cocoon.png")
butterfly_1 = pygame.image.load("butterfly_1.png")
butterfly_2 = pygame.image.load("butterfly_2.png")
bg = pygame.image.load("bg.png")

# Load egg animation frames
egg_frames = [pygame.image.load(os.path.join("ezgif-split", f"ezgif-frame-{i:03d}.png")) for i in range(7, 101)]

# Resize images
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
leaf_states = [pygame.transform.scale(img, (200, 100)) for img in leaf_states]
caterpillar = pygame.transform.scale(caterpillar, (150, 80))
cocoon = pygame.transform.scale(cocoon, (80, 150))
butterfly_1 = pygame.transform.scale(butterfly_1, (150, 150))
butterfly_2 = pygame.transform.scale(butterfly_2, (150, 150))

# Positions
leaf_x, leaf_y = 400, 300
caterpillar_x, caterpillar_y = 100, 500
cocoon_x, cocoon_y = 600, 300
butterfly_x, butterfly_y = -200, 200  # Start off-screen
egg_target_x, egg_target_y = 450, 320  # Where egg will be laid

# Animation Variables
leaf_index = 0
current_egg_frame = 0
frame_counter = 0
emerging_progress = 0  # For butterfly emergence animation

# Animation States
BUTTERFLY_ENTERING = 0
BUTTERFLY_LAYING_EGG = 1
EGG_DEVELOPING = 2
CATERPILLAR_ENTERING = 3
CATERPILLAR_EATING = 4
CATERPILLAR_MOVING = 5
FORMING_COCOON = 6
BUTTERFLY_EMERGING = 7
BUTTERFLY_LEAVING = 8

current_state = BUTTERFLY_ENTERING
rotation_angle = 0
caterpillar_alpha = 255
cocoon_alpha = 0

clock = pygame.time.Clock()

def draw_butterfly_emerging():
    # Draw cocoon with decreasing opacity
    cocoon_surface = cocoon.copy()
    cocoon_surface.set_alpha(255 - emerging_progress * 2)
    screen.blit(cocoon_surface, (cocoon_x, cocoon_y))
    
    # Draw butterfly with increasing size and opacity
    size = int(emerging_progress * 1.5)
    butterfly_surface = butterfly_1 if frame_counter % 10 < 5 else butterfly_2
    scaled_butterfly = pygame.transform.scale(butterfly_surface, 
                           (size, size))
    scaled_butterfly.set_alpha(emerging_progress * 2)
    screen.blit(scaled_butterfly, 
               (cocoon_x + 40 - size//2, 
                cocoon_y + 75 - size//2))

# Game loop
running = True
while running:
    screen.blit(bg, (0, 0))
    frame_counter += 1

    # State machine for animation
    if current_state == BUTTERFLY_ENTERING:
        # Butterfly flies in from left
        screen.blit(butterfly_1 if frame_counter % 10 < 5 else butterfly_2, (butterfly_x, butterfly_y))
        butterfly_x += 3
        
        if butterfly_x > egg_target_x - 100:
            current_state = BUTTERFLY_LAYING_EGG
            egg_frame_counter = 0

    elif current_state == BUTTERFLY_LAYING_EGG:
        # Butterfly hovers while egg appears
        screen.blit(butterfly_1 if frame_counter % 10 < 5 else butterfly_2, (butterfly_x, butterfly_y))
        
        if egg_frame_counter < len(egg_frames):
            scaled_egg = pygame.transform.scale(egg_frames[egg_frame_counter], (100, 100))
            screen.blit(scaled_egg, (egg_target_x, egg_target_y))
            if frame_counter % 3 == 0:
                egg_frame_counter += 1
        else:
            current_state = BUTTERFLY_LEAVING

    elif current_state == BUTTERFLY_LEAVING:
        # Butterfly flies away to right
        screen.blit(butterfly_1 if frame_counter % 10 < 5 else butterfly_2, (butterfly_x, butterfly_y))
        butterfly_x += 3
        
        if butterfly_x > WIDTH:
            current_state = EGG_DEVELOPING
            butterfly_x, butterfly_y = -200, 200
            current_egg_frame = 0

    elif current_state == EGG_DEVELOPING:
        # Show egg development
        scaled_egg = pygame.transform.scale(egg_frames[current_egg_frame], (100, 100))
        screen.blit(scaled_egg, (egg_target_x, egg_target_y))
        
        if frame_counter % 5 == 0:
            current_egg_frame += 1
        
        if current_egg_frame >= len(egg_frames):
            current_state = CATERPILLAR_ENTERING
            caterpillar_x, caterpillar_y = egg_target_x - 100, egg_target_y + 50

    elif current_state == CATERPILLAR_ENTERING:
        screen.blit(leaf_states[leaf_index], (leaf_x, leaf_y))
        screen.blit(caterpillar, (caterpillar_x, caterpillar_y))

        if caterpillar_x < leaf_x + 20:
            caterpillar_x += 1
        else:
            current_state = CATERPILLAR_EATING

    elif current_state == CATERPILLAR_EATING:
        screen.blit(leaf_states[leaf_index], (leaf_x, leaf_y))
        shake_offset = 2 if frame_counter % 10 < 5 else -2
        screen.blit(caterpillar, (caterpillar_x, caterpillar_y + shake_offset))

        if frame_counter % 40 == 0 and leaf_index < 4:
            leaf_index += 1
        elif leaf_index == 4:
            current_state = CATERPILLAR_MOVING

    elif current_state == CATERPILLAR_MOVING:
        if caterpillar_x < cocoon_x:
            caterpillar_x += 2
            caterpillar_y -= 1
        else:
            current_state = FORMING_COCOON
        screen.blit(caterpillar, (caterpillar_x, caterpillar_y))

    elif current_state == FORMING_COCOON:
        rotation_angle += 5
        caterpillar_width = max(10, caterpillar.get_width() - 2)
        caterpillar_height = max(5, caterpillar.get_height() - 1)
        caterpillar = pygame.transform.scale(caterpillar, (caterpillar_width, caterpillar_height))
        rotated_caterpillar = pygame.transform.rotate(caterpillar, rotation_angle)

        caterpillar_alpha = max(0, caterpillar_alpha - 2)
        caterpillar_surface = rotated_caterpillar.copy()
        caterpillar_surface.set_alpha(caterpillar_alpha)

        cocoon_alpha = min(255, cocoon_alpha + 2)
        cocoon_surface = cocoon.copy()
        cocoon_surface.set_alpha(cocoon_alpha)

        screen.blit(caterpillar_surface, (caterpillar_x, caterpillar_y))
        screen.blit(cocoon_surface, (cocoon_x, cocoon_y))

        if caterpillar_alpha == 0 and cocoon_alpha == 255:
            current_state = BUTTERFLY_EMERGING
            emerging_progress = 0

    elif current_state == BUTTERFLY_EMERGING:
        draw_butterfly_emerging()
        emerging_progress += 1
        
        if emerging_progress >= 128:
            current_state = BUTTERFLY_ENTERING  # Start cycle again
            # Reset variables
            leaf_index = 0
            caterpillar = pygame.transform.scale(pygame.image.load("caterpillar.png"), (150, 80))
            rotation_angle = 0
            caterpillar_alpha = 255
            cocoon_alpha = 0
            butterfly_x, butterfly_y = cocoon_x, cocoon_y  # New butterfly starts here

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
