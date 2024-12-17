import pygame
import random
import os

# Initialize Pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("heckin cats")

# High-score file
high_score_file = "high_score.txt"

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read().strip())
    return 0

def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Load images
try:
    dog_left_image = pygame.image.load('dog_left.png')
    dog_right_image = pygame.image.load('dog_right.png')
    dog_left_speed = pygame.image.load('dog_left_speed.png') # New image for speed potion left
    dog_right_speed = pygame.image.load('dog_right_speed.png') # New image for speed potion right
    dog_left_shield = pygame.image.load('dog_left_shield.png') # New image for shield potion left
    dog_right_shield = pygame.image.load('dog_right_shield.png') # New image for shield potion right
    bone_image = pygame.image.load('bone.png')
    speed_potion_image = pygame.image.load('speed_potion.png')
    shield_potion_image = pygame.image.load('shield_potion.png')
    background_image = pygame.image.load('background.jpg')
    cat_left_image = pygame.image.load('cat_left.png')
    cat_right_image = pygame.image.load('cat_right.png')

    dog_left_image = pygame.transform.scale(dog_left_image, (50, 50))
    dog_right_image = pygame.transform.scale(dog_right_image, (50, 50))
    dog_left_speed = pygame.transform.scale(dog_left_speed, (50, 50))
    dog_right_speed = pygame.transform.scale(dog_right_speed, (50, 50))
    dog_left_shield = pygame.transform.scale(dog_left_shield, (50, 50))
    dog_right_shield = pygame.transform.scale(dog_right_shield, (50, 50))
    bone_image = pygame.transform.scale(bone_image, (30, 30))
    speed_potion_image = pygame.transform.scale(speed_potion_image, (30, 30))
    shield_potion_image = pygame.transform.scale(shield_potion_image, (30, 30))
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    cat_left_image = pygame.transform.scale(cat_left_image, (40, 40))
    cat_right_image = pygame.transform.scale(cat_right_image, (40, 40))

except pygame.error as e:
    print(f"Error loading images: {e}")
    exit()

# Load sound effects
try:
    bone_sound = pygame.mixer.Sound('bone_collect.wav')
    cat_collision_sound = pygame.mixer.Sound('cat_collision.wav')
    potion_collect_sound = pygame.mixer.Sound('potion_collect.wav')
except pygame.error as e:
    print(f"Error loading sounds: {e}")
    exit()

# Font settings
font = pygame.font.SysFont(None, 35)
game_over_font = pygame.font.SysFont(None, 80)

def show_game_over_screen(score, high_score):
    screen.fill((0, 0, 0))
    game_over_text = game_over_font.render("heckin cats got ya", True, (255, 0, 0))
    score_text = font.render(f"Bones Eaten: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (200, 200, 200))

    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 1.7))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 1.4))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return "restart"
        if keys[pygame.K_q]:
            pygame.quit()
            exit()

def main():
    global dog_x, dog_y, dog_facing, score, lives, bone_x, bone_y, cats

    # Game variables
    dog_width, dog_height = 50, 50
    dog_x, dog_y = screen_width // 2, screen_height - dog_height - 10
    dog_speed = 5
    dog_facing = "right"
    score = 0
    lives = 3

    speed_potion = {"x": None, "y": None, "active": False, "spawn_time": None}
    shield_potion = {"x": None, "y": None, "active": False, "spawn_time": None}

    bone_width, bone_height = 30, 30
    bone_x = random.randint(0, screen_width - bone_width)
    bone_y = random.randint(0, screen_height - bone_height)

    cats = [
        {
            "x": random.randint(0, screen_width - 50),
            "y": random.randint(0, screen_height // 2 - 50),
            "speed_x": random.choice([7, 10]),
            "speed_y": random.choice([7, 10]),
            "facing": "right"
        } for _ in range(4)
    ]

    potion_duration = 7
    potion_spawn_interval = 5000
    last_potion_spawn = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        if current_time - last_potion_spawn >= potion_spawn_interval:
            if not speed_potion["x"] and not shield_potion["x"]:
                if random.choice([True, False]):
                    speed_potion["x"] = random.randint(0, screen_width - 30)
                    speed_potion["y"] = random.randint(0, screen_height - 30)
                else:
                    shield_potion["x"] = random.randint(0, screen_width - 30)
                    shield_potion["y"] = random.randint(0, screen_height - 30)
                last_potion_spawn = current_time

        if speed_potion["x"] and current_time - last_potion_spawn > 5000:
            speed_potion["x"], speed_potion["y"] = None, None
        if shield_potion["x"] and current_time - last_potion_spawn > 5000:
            shield_potion["x"], shield_potion["y"] = None, None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dog_x -= dog_speed
            dog_facing = "left"
        if keys[pygame.K_RIGHT]:
            dog_x += dog_speed
            dog_facing = "right"
        if keys[pygame.K_UP]:
            dog_y -= dog_speed
        if keys[pygame.K_DOWN]:
            dog_y += dog_speed

        dog_x = max(0, min(screen_width - dog_width, dog_x))
        dog_y = max(0, min(screen_height - dog_height, dog_y))

        if (dog_x < bone_x + bone_width and dog_x + dog_width > bone_x and
            dog_y < bone_y + bone_height and dog_y + dog_height > bone_y):
            score += 1
            bone_x = random.randint(0, screen_width - bone_width)
            bone_y = random.randint(0, screen_height - bone_height)
            bone_sound.play()

        if (speed_potion["x"] and
            dog_x < speed_potion["x"] + 30 and dog_x + dog_width > speed_potion["x"] and
            dog_y < speed_potion["y"] + 30 and dog_y + dog_height > speed_potion["y"]):
            dog_speed = 10
            speed_potion["active"] = True
            potion_collect_sound.play()
            speed_potion["x"], speed_potion["y"] = None, None
            pygame.time.set_timer(pygame.USEREVENT + 1, potion_duration * 1000)

        if (shield_potion["x"] and
            dog_x < shield_potion["x"] + 30 and dog_x + dog_width > shield_potion["x"] and
            dog_y < shield_potion["y"] + 30 and dog_y + dog_height > shield_potion["y"]):
            shield_potion["active"] = True
            potion_collect_sound.play()
            shield_potion["x"], shield_potion["y"] = None, None
            pygame.time.set_timer(pygame.USEREVENT + 2, potion_duration * 1000)

        for cat in cats:
            cat["x"] += cat["speed_x"]
            cat["y"] += cat["speed_y"]
            if cat["x"] <= 0 or cat["x"] >= screen_width - 50:
                cat["speed_x"] = -cat["speed_x"]
            if cat["y"] <= 0 or cat["y"] >= screen_height - 50:
                cat["speed_y"] = -cat["speed_y"]
            cat["facing"] = "right" if cat["speed_x"] > 0 else "left"

            if shield_potion["active"]:
                continue

            if (dog_x < cat["x"] + 50 and dog_x + dog_width > cat["x"] and
                dog_y < cat["y"] + 50 and dog_y + dog_height > cat["y"]):
                lives -= 1
                cat_collision_sound.play()
                dog_x, dog_y = screen_width // 2, screen_height - dog_height - 10
                if lives <= 0:
                    running = False

        screen.blit(background_image, (0, 0))

        # Render the correct dog image based on potion state
        if speed_potion["active"]:
            if dog_facing == "left":
                screen.blit(dog_left_speed, (dog_x, dog_y))
            else:
                screen.blit(dog_right_speed, (dog_x, dog_y))
        elif shield_potion["active"]:
            if dog_facing == "left":
                screen.blit(dog_left_shield, (dog_x, dog_y))
            else:
                screen.blit(dog_right_shield, (dog_x, dog_y))
        else:
            if dog_facing == "left":
                screen.blit(dog_left_image, (dog_x, dog_y))
            else:
                screen.blit(dog_right_image, (dog_x, dog_y))

        for cat in cats:
            cat_image = cat_left_image if cat["facing"] == "left" else cat_right_image
            screen.blit(cat_image, (cat["x"], cat["y"]))

        screen.blit(bone_image, (bone_x, bone_y))

        if speed_potion["x"]:
            screen.blit(speed_potion_image, (speed_potion["x"], speed_potion["y"]))
        if shield_potion["x"]:
            screen.blit(shield_potion_image, (shield_potion["x"], shield_potion["y"]))

        score_text = font.render(f"Bones: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                dog_speed = 5
                speed_potion["active"] = False
            if event.type == pygame.USEREVENT + 2:
                shield_potion["active"] = False

    if score > load_high_score():
        save_high_score(score)
    if show_game_over_screen(score, load_high_score()) == "restart":
        main()

main()