import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BALL_SPEED = 5
PADDLE_SPEED = 7
MAX_SCORE = 10
ERROR_MARGIN = 10  # IA paddle margin of error
BALL_ACCELERATION = 1.1  # Acceleration factor for each paddle hit

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)

    def draw(self, window):
        pygame.draw.rect(window, WHITE, self.rect)

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed_x = BALL_SPEED * random.choice((1, -1))
        self.speed_y = BALL_SPEED * random.choice((1, -1))
        self.max_speed = 15  # Vitesse maximale

    def draw(self, window):
        pygame.draw.ellipse(window, WHITE, self.rect)

    def bounce(self, paddle):
        # Calculer où la balle touche la raquette (de -1 à 1)
        relative_hit = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        # Ajouter un effet sur speed_y basé sur la position
        self.speed_y = relative_hit * 7  # 7 Vitesse max ajustable, si au dessus balle passe à travers
        # Limiter speed_y
        self.speed_y = max(-self.max_speed, min(self.max_speed, self.speed_y))
        # Inverser speed_x avec accélération
        self.speed_x = -self.speed_x * BALL_ACCELERATION
        # Ajouter un petit aléa pour plus de fun
        self.speed_y += random.uniform(-1, 1)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y = -self.speed_y
        # Limiter la vitesse
        self.speed_x = max(-self.max_speed, min(self.max_speed, self.speed_x))
        self.speed_y = max(-self.max_speed, min(self.max_speed, self.speed_y))

# Initialize objects
left_paddle = Paddle(50, HEIGHT // 2 - 50)
right_paddle = Paddle(WIDTH - 60, HEIGHT // 2 - 50)
ball = Ball(WIDTH // 2, HEIGHT // 2)

# Load sounds
ping_sound = pygame.mixer.Sound("ping.wav")
pong_sound = pygame.mixer.Sound("pong.wav")
goal_sound = pygame.mixer.Sound("goal.wav")

# Scores
left_score = 0
right_score = 0

# Font for the score
font = pygame.font.Font(None, 74)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Control the left paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        left_paddle.move(-PADDLE_SPEED)
    if keys[pygame.K_DOWN]:
        left_paddle.move(PADDLE_SPEED)

    # Control the right paddle (simple AI with error margin)
    if right_paddle.rect.centery < ball.rect.y - ERROR_MARGIN:
        right_paddle.move(PADDLE_SPEED)
    elif right_paddle.rect.centery > ball.rect.y + ERROR_MARGIN:
        right_paddle.move(-PADDLE_SPEED)

    # Move the ball
    ball.move()

    # Collision with paddles
    if ball.rect.colliderect(left_paddle.rect):
        ball.rect.left = left_paddle.rect.right  # repositionnement
        ball.bounce(left_paddle)
        ping_sound.play()
    elif ball.rect.colliderect(right_paddle.rect):
        ball.rect.right = right_paddle.rect.left  # repositionnement
        ball.bounce(right_paddle)
        pong_sound.play()

    # Check for goals
    if ball.rect.left < 0:
        right_score += 1
        goal_sound.play()
        pygame.time.delay(500)  # Delay after goal
        ball = Ball(WIDTH // 2, HEIGHT // 2)
    if ball.rect.right > WIDTH:
        left_score += 1
        goal_sound.play()
        pygame.time.delay(500)  # Delay after goal
        ball = Ball(WIDTH // 2, HEIGHT // 2)

    # Check for maximum score
    if left_score >= MAX_SCORE or right_score >= MAX_SCORE:
        pygame.quit()
        sys.exit()

    # Drawing
    window.fill(BLACK)
    left_paddle.draw(window)
    right_paddle.draw(window)
    ball.draw(window)

    # Draw center line
    for i in range(0, HEIGHT, 20):
        pygame.draw.rect(window, WHITE, (WIDTH // 2 - 1, i, 2, 10))

    # Display scores
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    window.blit(left_text, (WIDTH // 4, 20))
    window.blit(right_text, (3 * WIDTH // 4, 20))

    pygame.display.flip()
    pygame.time.Clock().tick(60)