import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Butterfly Life Cycle Animation")

# Load images
leaf_states = [pygame.image.load(f"leaf_{i}.png") for i in range(1, 6)]
caterpillar = pygame.image.load("caterpillar.png")
branch = pygame.image.load("branch.png")
cocoon = pygame.image.load("cocoon.png")
butterfly_1 = pygame.image.load("butterfly_1.png")
butterfly_2 = pygame.image.load("butterfly_2.png")
egg = pygame.image.load("egg.png")

# Resize images
leaf_states = [pygame.transform.scale(img, (200, 100)) for img in leaf_states]
caterpillar = pygame.transform.scale(caterpillar, (150, 80))
branch = pygame.transform.scale(branch, (300, 100))
cocoon = pygame.transform.scale(cocoon, (80, 150))
butterfly_1 = pygame.transform.scale(butterfly_1, (150, 150))
butterfly_2 = pygame.transform.scale(butterfly_2, (150, 150))
egg = pygame.transform.scale(egg, (50, 50))  # Initial size of the egg
original_egg_size = 50  # Define the original size of the egg

# Positions
leaf_x, leaf_y = 300, 400
caterpillar_x, caterpillar_y = 50, 400
branch_x, branch_y = 250, 150
cocoon_x, cocoon_y = 350, 180
butterfly_x, butterfly_y = 350, 180

# Animation Variables
leaf_index = 0
caterpillar_entering = True  # New stage for caterpillar entering
caterpillar_eating = False
caterpillar_moving = False
forming_cocoon = False
butterfly_emerging = False
butterfly_flying = False
zoom_factor = 2.0  # Start with a zoomed-in view
zooming_out = True  # Start by zooming out
zooming_in = False  # Zoom in at the end
egg_stage = True  # Start with the egg stage

# Add variables for egg position during zoom transitions
egg_target_x, egg_target_y = 40, 550  # Caterpillar's initial position
egg_center_x, egg_center_y = WIDTH // 2, HEIGHT // 2  # Center of the screen

def lerp(start, end, t):
    """Linear interpolation between start and end based on t (0-1)"""
    return start + t * (end - start)

clock = pygame.time.Clock()
frame_counter = 0

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # White background
    frame_counter += 1

    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # print(f"Mouse Coordinates: ({mouse_x}, {mouse_y})")

    # Egg zoom effect
    if egg_stage:
        if zooming_out:
            # Gradually zoom out and move towards caterpillar position
            zoom_factor -= 0.005  # Adjust speed as needed

            # Calculate interpolated position (from center to caterpillar position)
            t = (2.0 - zoom_factor) / 2.0  # Normalized value from 0 to 1
            egg_x = int(lerp(egg_center_x, egg_target_x, t))
            egg_y = int(lerp(egg_center_y, egg_target_y, t))

            # Smoothly scale down the egg
            current_egg_size = int(original_egg_size * zoom_factor)
            egg_zoomed = pygame.transform.scale(egg, (current_egg_size, current_egg_size))

            # Stop zooming out and prepare for the next stage
            if zoom_factor <= 0.2:
                zoom_factor = 1.0
                zooming_out = False
                egg_stage = False  # Transition to main animation

            # Draw the zoomed and moved egg
            screen.blit(egg_zoomed, (egg_x - current_egg_size // 2, egg_y - current_egg_size // 2))

        elif zooming_in:
            # Gradually zoom in and return to center
            zoom_factor += 0.005  # Adjust speed as needed

            # Calculate interpolated position (from caterpillar position to center)
            t = (zoom_factor - 1.0)  # Normalized value from 0 to 1
            egg_x = int(lerp(egg_target_x, egg_center_x, t))
            egg_y = int(lerp(egg_target_y, egg_center_y, t))

            # Smoothly scale up the egg
            current_egg_size = int(original_egg_size * zoom_factor)
            egg_zoomed = pygame.transform.scale(egg, (current_egg_size, current_egg_size))

            # Stop zooming in and prepare for the next cycle
            if zoom_factor >= 2.0:  # Stop zooming in when fully zoomed
                zoom_factor = 2.0
                zooming_in = False
                zooming_out = True  # Restart the zoom-out effect
                egg_stage = True  # Restart the egg stage

                # Reset all animation variables for the next cycle
                caterpillar_x, caterpillar_y = 50, 400  # Reset caterpillar position
                leaf_index = 0
                caterpillar_entering = True
                caterpillar_eating = False
                caterpillar_moving = False
                forming_cocoon = False
                butterfly_emerging = False
                butterfly_flying = False
            # Draw the zoomed and moved egg
            screen.blit(egg_zoomed, (egg_x - current_egg_size // 2, egg_y - current_egg_size // 2))

    # Main animation logic
    elif caterpillar_entering:
        screen.blit(leaf_states[leaf_index], (leaf_x, leaf_y))
        screen.blit(caterpillar, (caterpillar_x, caterpillar_y))
        
        if caterpillar_x < 320:  # Move caterpillar to the leaf position
            caterpillar_x += 1  # Adjust speed as needed
        else:  # Once at the leaf position, start eating
            caterpillar_entering = False
            caterpillar_eating = True

    elif caterpillar_eating:
        screen.blit(leaf_states[leaf_index], (leaf_x, leaf_y))
        shake_offset = 2 if frame_counter % 10 < 5 else -2
        screen.blit(caterpillar, (caterpillar_x, caterpillar_y + shake_offset))
        
        if frame_counter % 40 == 0 and leaf_index < 4:
            leaf_index += 1
        elif leaf_index == 4:
            caterpillar_eating = False
            caterpillar_moving = True

    elif caterpillar_moving:
        screen.blit(branch, (branch_x, branch_y))
        if caterpillar_x < branch_x + 50:
            caterpillar_x += 2
            caterpillar_y -= 1
        else:
            caterpillar_moving = False
            forming_cocoon = True
        screen.blit(caterpillar, (caterpillar_x, caterpillar_y))
    elif forming_cocoon:
        screen.blit(branch, (branch_x, branch_y))

        # Initialize variables for rotation, shrinking, and fading
        if 'rotation_angle' not in locals():
            rotation_angle = 0  # Start with no rotation
            caterpillar_alpha = 255  # Fully opaque caterpillar
            cocoon_alpha = 0  # Fully transparent cocoon

        # Rotate and shrink the caterpillar
        rotation_angle += 5  # Rotate by 5 degrees per frame
        caterpillar_width = max(10, caterpillar.get_width() - 2)  # Gradually shrink width
        caterpillar_height = max(5, caterpillar.get_height() - 1)  # Gradually shrink height
        caterpillar = pygame.transform.scale(caterpillar, (caterpillar_width, caterpillar_height))
        rotated_caterpillar = pygame.transform.rotate(caterpillar, rotation_angle)

        # Fade out the caterpillar
        caterpillar_alpha = max(0, caterpillar_alpha - 2)  # Reduce alpha by 2 per frame
        caterpillar_surface = rotated_caterpillar.copy()
        caterpillar_surface.set_alpha(caterpillar_alpha)

        # Fade in the cocoon
        cocoon_alpha = min(255, cocoon_alpha + 2)  # Increase alpha by 2 per frame
        cocoon_surface = cocoon.copy()
        cocoon_surface.set_alpha(cocoon_alpha)

        # Draw the caterpillar and cocoon
        screen.blit(caterpillar_surface, (caterpillar_x, caterpillar_y))
        screen.blit(cocoon_surface, (cocoon_x, cocoon_y))

        # Transition to the next state when the caterpillar is fully faded out
        if caterpillar_alpha == 0 and cocoon_alpha == 255:
            forming_cocoon = False
            butterfly_emerging = True

    elif butterfly_emerging:
        screen.blit(branch, (branch_x, branch_y))
        screen.blit(cocoon, (cocoon_x, cocoon_y))
        if frame_counter % 50 == 0:
            butterfly_emerging = False
            butterfly_flying = True

    elif butterfly_flying:
        screen.blit(branch, (branch_x, branch_y))
        if frame_counter % 10 < 5:
            screen.blit(butterfly_1, (butterfly_x, butterfly_y))
        else:
            screen.blit(butterfly_2, (butterfly_x, butterfly_y))
        
        butterfly_x -= 2
        butterfly_y += 2

        if butterfly_y > 650:  # Once off screen, zoom back into the egg
            butterfly_x, butterfly_y = 350, 180
            caterpillar_x, caterpillar_y = -150, 420
            leaf_index = 0
            caterpillar = pygame.transform.scale(pygame.image.load("caterpillar.png"), (150, 80))
            rotation_angle = 0
            caterpillar_alpha = 255
            cocoon_alpha = 0
            forming_cocoon = False
            butterfly_emerging = False
            butterfly_flying = False
            caterpillar_entering = True
            caterpillar_eating = False
            caterpillar_moving = False
            zooming_in = True
            egg_stage = True
            butterfly_flying = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)  # 60 FPS

pygame.quit()
