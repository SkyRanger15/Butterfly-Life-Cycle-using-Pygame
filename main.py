import pygame
import os

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
bg = pygame.image.load("bg.png") 

# Load egg animation frames
egg_frames = [pygame.image.load(os.path.join("ezgif-split", f"ezgif-frame-{i:03d}.png")) for i in range(7, 101)]

# Resize images
leaf_states = [pygame.transform.scale(img, (200, 100)) for img in leaf_states]
caterpillar = pygame.transform.scale(caterpillar, (150, 80))
branch = pygame.transform.scale(branch, (300, 100))
cocoon = pygame.transform.scale(cocoon, (80, 150))
butterfly_1 = pygame.transform.scale(butterfly_1, (150, 150))
butterfly_2 = pygame.transform.scale(butterfly_2, (150, 150))

# Positions
leaf_x, leaf_y = 300, 400
caterpillar_x, caterpillar_y = 50, 400
branch_x, branch_y = 250, 150
cocoon_x, cocoon_y = 350, 180
butterfly_x, butterfly_y = 350, 180
egg_target_x, egg_target_y = 40, 400  # Caterpillar's initial position

# Animation Variables
leaf_index = 0
caterpillar_entering = True
caterpillar_eating = False
caterpillar_moving = False
forming_cocoon = False
butterfly_emerging = False
butterfly_flying = False
egg_animation_playing = True  # Start with the animation sequence
current_egg_frame = 0

clock = pygame.time.Clock()
frame_counter = 0

# Game loop
running = True
while running:
    screen.blit(bg, (0, 0))  # White background
    frame_counter += 1

    # Egg animation logic
    if egg_animation_playing:
        scaled_egg_frame = pygame.transform.scale(egg_frames[current_egg_frame], (150, 150))  # Adjust size as needed
        screen.blit(scaled_egg_frame, (egg_target_x, egg_target_y))  # Draw at caterpillar position  # Draw at caterpillar position

        # Advance to the next frame
        if frame_counter % 5 == 0:  # Adjust speed by changing the modulus value
            current_egg_frame += 1

        # Check if the animation is complete
        if current_egg_frame >= len(egg_frames):
            current_egg_frame = 0  # Restart the animation
            egg_animation_playing = False  # Transition to the next stage
            caterpillar_entering = True  # Restart the cycle
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
        
        # Move the butterfly toward the egg position
        if butterfly_y < egg_target_y:
            butterfly_x -= 2
            butterfly_y += 2
        else:
            # Butterfly reaches the egg position
            screen.blit(butterfly_1 if frame_counter % 10 < 5 else butterfly_2, (butterfly_x, butterfly_y))
            scaled_egg_frame = pygame.transform.scale(egg_frames[0], (150, 150))  # Adjust size as needed
            screen.blit(scaled_egg_frame, (egg_target_x, egg_target_y))
            screen.blit(butterfly_1 if frame_counter % 10 < 5 else butterfly_2, (butterfly_x, butterfly_y))

            # Check if the butterfly has left the screen
            butterfly_y += 2  # Move the butterfly off the screen
            if butterfly_y > HEIGHT:
                butterfly_x, butterfly_y = 350, 180
                caterpillar_x, caterpillar_y = 50,400
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
                egg_animation_playing = True  # Start the egg animation

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)  # 60 FPS

pygame.quit()
