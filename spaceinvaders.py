import pygame
import random

# Initialise pygame module

pygame.init()

# Initalise the mixer module (sound effects)

pygame.mixer.init()

# Load sound effects
shoot_sound = pygame.mixer.Sound('./shoot.wav')
explosion_sound = pygame.mixer.Sound('./explosion.wav')
shoot_sound.set_volume(0.3)  
explosion_sound.set_volume(0.3)  

# Load images
background_image = pygame.image.load('./background.png')

player_image = pygame.image.load('./player.png')
enemy_image = pygame.image.load('./enemy.png')
# Flip horizontally so they face the player
enemy_image = pygame.transform.flip(enemy_image, False, True)
bullet_image = pygame.image.load('./bullet.png')

# Scale enemy and bullet images
enemy_image = pygame.transform.scale(enemy_image, (100, 100))
bullet_image = pygame.transform.scale(bullet_image, (20, 40))

# Load icon
icon_image = pygame.image.load('./icon.png')

# Set dimensions for game window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Window title
pygame.display.set_caption('Space Invaders')

# Font for the score display
font = pygame.font.Font(None, 36)

# Player class
class Player:
    def __init__(self, x, y, width, height, speed): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self, screen):
        screen.blit(player_image, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        
# Enemy class

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self, screen):
        screen.blit(enemy_image, (self.x, self.y))
    
    def move(self):
        self.y += self.speed
    
    def reached_bottom(self):
        return self.y >= screen_height

# Bullet class

class Bullet:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
    
    def draw(self, screen):
        screen.blit(bullet_image, (self.x, self.y))

    def move(self):
        self.y -= self.speed

    def collides_with(self, enemy):
        return (self.x < enemy.x + enemy.width and
                self.x + self.width > enemy.x and
                self.y < enemy.y + enemy.height and
                self.y + self.height > enemy.y)

# Function for the game start screen
def start_screen(): 
    screen.fill((0, 0, 0))
    title_text = font.render('Space Invaders', True, (255, 255, 255))
    instructions_text = font.render('Press any key to start', True, (255, 255, 255))
    screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - title_text.get_height() / 2))
    screen.blit(instructions_text, (screen_width / 2 - instructions_text.get_width() / 2, screen_height / 2 + instructions_text.get_height()))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                return

# Function for the game over screen
def game_over(score):
    screen.fill((0,0,0))
    game_over_text = font.render('Game Over', True, (255, 255, 255))
    score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2 - game_over_text.get_height() / 2))
    screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, screen_height / 2 + score_text.get_height()))
    pygame.display.flip()
    pygame.time.wait(4000) # Wait 4 seconds before exiting

# Create player instance
player = Player(screen_width / 2, screen_height - 150, 50, 50, 5)

# Create enemy instances
enemies = []    
# Create 5 enemies, append each to the enemies list
for i in range(5):
    enemy = Enemy(random.randrange(0, screen_width-50), random.randrange(-1000, -50), 80, 50, 1.2)   
    enemies.append(enemy) 

# Initialise the last time an enemy was added
last_enemy_time = pygame.time.get_ticks()

# Display the start screen
start_screen()

# Create list to hold the bullets
bullets = []

# Initialise score variable
score = 0

# Initalise last bullet time (for adding fire delay)
last_bullet_time = pygame.time.get_ticks()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        # if user clicks the exit button
        if event.type == pygame.QUIT:
            running = False
        # if spacebar is pressed, create bullet object
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_time = pygame.time.get_ticks()
                if current_time - last_bullet_time >= 1000:
                    bullet = Bullet(player.x + player.width / 2 - -29 , player.y, 10, 20, 2)
                    # Append bullet to the bullet list
                    bullets.append(bullet)
                    shoot_sound.play()  
                    last_bullet_time = current_time
    
    # Player movement
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Enemy movement 
    # Iterate through the enemies list and call the move method
    for enemy in enemies:
        enemy.move()
        # End the game if enemy reaches the bottom
        if enemy.reached_bottom():
            running = False
            break
    
    # Bullet movement and collision detection
    for bullet in bullets:
        bullet.move()
        for enemy in enemies:
            if bullet.collides_with(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1 # Increase the score every enemy kill 
                explosion_sound.play()
                break 
    
    # Add new enemy if enough time has passed
    current_time = pygame.time.get_ticks()
    # 2000 is 2 seconds
    if current_time - last_enemy_time > 2000:
         enemy = Enemy(random.randrange(0, screen_width-50), random.randrange(-1000, -50), 80, 50, 1.2)
         enemies.append(enemy)
         last_enemy_time = current_time

    # Draw the background image
    screen.blit(background_image,(0, 0))

    # Draw the player
    player.draw(screen)

    # Draw the enemies
    for enemy in enemies:
        enemy.draw(screen)

    # Draw the bullets
    for bullet in bullets:
        bullet.draw(screen)

    # Display the score
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

# Display the game over screen
game_over(score)

# Quit the game
pygame.quit()