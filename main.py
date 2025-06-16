import pygame
import sys
from penguin import Penguin

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Penguin Trainer")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 32)
button_up = pygame.Rect(100, 400, 100, 40)
button_down = pygame.Rect(440, 400, 100, 40)

def draw_buttons():
    pygame.draw.rect(screen, (0, 255, 0), button_up)
    pygame.draw.rect(screen, (255, 0, 0), button_down)
    screen.blit(font.render("👍", True, (0, 0, 0)), (button_up.x + 35, button_up.y + 5))
    screen.blit(font.render("👎", True, (0, 0, 0)), (button_down.x + 35, button_down.y + 5))


# Load penguin images
penguin_sprites = {
    "idle": pygame.image.load("assets/idle_right.png").convert_alpha(),
    "walk_left_1": pygame.image.load("assets/walk_left.png").convert_alpha(),
    "walk_left_2": pygame.image.load("assets/walk_left_turn.png").convert_alpha(),
    "walk_right_1": pygame.image.load("assets/walk_right.png").convert_alpha(),
    "walk_right_2": pygame.image.load("assets/walk_right_turn.png").convert_alpha(),
}

penguin_rect = penguin_sprites["idle"].get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Penguin agent
actions = ["idle", "waddle_left", "waddle_right"]
penguin = Penguin(actions)

# Animation state
current_action = "idle"
animation_sequence = []
animation_index = 0
animation_timer = 0
frame_duration = 15  # frames per sprite
movement_per_frame = 5  # smaller step

def start_animation(action):
    global animation_sequence

    if action == "waddle_left":
        animation_sequence = ["walk_left_1", "walk_left_2", "walk_left_1"]
    elif action == "waddle_right":
        animation_sequence = ["walk_right_1", "walk_right_2", "walk_right_1"]
    else:
        animation_sequence = ["idle"]

    return 0  # reset index

def move_during_animation(action, frame_index):
    if action == "waddle_left":
        penguin_rect.x -= movement_per_frame
    elif action == "waddle_right":
        penguin_rect.x += movement_per_frame

    # Keep penguin inside screen horizontally
    if penguin_rect.left < 0:
        penguin_rect.left = 0
    if penguin_rect.right > WIDTH:
        penguin_rect.right = WIDTH

    # clamping vertically 
    if penguin_rect.top < 0:
        penguin_rect.top = 0
    if penguin_rect.bottom > HEIGHT:
        penguin_rect.bottom = HEIGHT


# Main loop
running = True
while running:
    screen.fill((150, 200, 255))

    # Draw penguin
    current_frame = animation_sequence[animation_index] if animation_sequence else "idle"
    screen.blit(penguin_sprites[current_frame], penguin_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_up.collidepoint(event.pos):
                penguin.update_q(actions.index(current_action), reward=1, next_state="idle")
                current_action = "idle"
                animation_index = start_animation(current_action)

            elif button_down.collidepoint(event.pos):
                penguin.update_q(actions.index(current_action), reward=-1, next_state="idle")
                current_action = "idle"
                animation_index = start_animation(current_action)

    # Animation timing & updates
    if animation_timer <= 0:
        # Move a bit with each frame of animation
        move_during_animation(current_action, animation_index)

        # Next frame
        animation_index += 1

        if animation_index >= len(animation_sequence):
            # Animation over thus choose next action
            action_index = penguin.get_action()
            current_action = actions[action_index]
            animation_index = start_animation(current_action)

        animation_timer = frame_duration
    else:
        animation_timer -= 1

    # Draw buttons
    draw_buttons()

    # Update display and tick
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

