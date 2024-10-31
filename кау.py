import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 30
ENEMY_SIZE = 30
EXP_POINT_SIZE = 20
SPECIAL_EXP_POINT_SIZE = 25
TARGET_SCORE = 480
TIME_LIMIT = 30

# Цвета
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Создание окна игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Like Game")

# Класс игрока
class Player:
    def __init__(self):
        self.position = [WIDTH // 1, HEIGHT // 1]
        self.score = 0
        self.radius = PLAYER_SIZE // 4

    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.position, self.radius)

    def move(self, direction):
        if direction == "UP" and self.position[1] > self.radius:
            self.position[1] -= 4
        elif direction == "DOWN" and self.position[1] < HEIGHT - self.radius:
            self.position[1] += 4
        elif direction == "LEFT" and self.position[0] > self.radius:
            self.position[0] -= 4
        elif direction == "RIGHT" and self.position[0] < WIDTH - self.radius:
            self.position[0] += 4

# Класс врага
class Enemy:
    def __init__(self):
        self.position = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        self.rect = pygame.Rect(self.position[0], self.position[1], ENEMY_SIZE, ENEMY_SIZE)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

    def move(self, player_pos):
        if self.position[0] < player_pos[0]:
            self.position[0] += 2
        elif self.position[0] > player_pos[0]:
            self.position[0] -= 2
        if self.position[1] < player_pos[1]:
            self.position[1] += 2
        elif self.position[1] > player_pos[1]:
            self.position[1] -= 2
        self.rect.topleft = self.position

# Класс очков опыта
class ExperiencePoint:
    def __init__(self, special=False):
        self.position = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        self.is_special = special
        self.size = SPECIAL_EXP_POINT_SIZE if special else EXP_POINT_SIZE

    def draw(self):
        color = GREEN if self.is_special else BLUE
        pygame.draw.circle(screen, color, self.position, self.size // 2)

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy() for _ in range(4)]
    experience_points = [ExperiencePoint() for _ in range(23)]
    experience_points.append(ExperiencePoint(special=True))  # Добавление специальной очки
    timer = TIME_LIMIT
    start_ticks = pygame.time.get_ticks()  # Получить текущее время в миллисекундах

    while True:
        screen.fill(BLACK)
        player.draw()
        
        for enemy in enemies:
            enemy.move(player.position)
            enemy.draw()

        for exp in experience_points:
            exp.draw()

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move("UP")
        if keys[pygame.K_DOWN]:
            player.move("DOWN")
        if keys[pygame.K_LEFT]:
            player.move("LEFT")
        if keys[pygame.K_RIGHT]:
            player.move("RIGHT")

        # Проверка на сбор очков опыта
        for exp in experience_points[:]:
            exp_rect = pygame.Rect(exp.position[0], exp.position[1], exp.size, exp.size)
            player_rect = pygame.Rect(player.position[0] - player.radius, player.position[1] - player.radius, PLAYER_SIZE, PLAYER_SIZE)
            if player_rect.colliderect(exp_rect):
                player.score += 100 if exp.is_special else 30
                experience_points.remove(exp)

        # Проверка на поражение
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                print("Game Over! You were caught by an enemy.")
                pygame.quit()
                sys.exit()

        # Проверка на победу
        if player.score >= TARGET_SCORE:
            print("You win! Your score: ", player.score)
            pygame.quit()
            sys.exit()
        
        # Таймер
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Измеряем время в секундах
        if seconds >= TIME_LIMIT:
            print("Game Over! Time's up.")
            pygame.quit()
            sys.exit()
        
        # Отображение очков и времени
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        timer_text = font.render(f"Time: {TIME_LIMIT - seconds}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)

# Запуск игры
if __name__ == "__main__":
    main()