"""Это импорт, который делает что-то полезное."""
from random import randint


import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Это публичный метод, который делает что-то полезное."""

    def __init__(self):
        """Это публичный метод, который делает что-то полезное."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Это публичный метод, который делает что-то полезное."""
        pass


class Apple(GameObject):
    """Это публичный метод, который делает что-то полезное."""

    def __init__(self):
        """Это публичный метод, который делает что-то полезное."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (
            randint(0, GRID_SIZE) * GRID_SIZE,
            randint(0, GRID_SIZE) * GRID_SIZE
            )

    def randomize_position(self):
        """Это публичный метод, который делает что-то полезное."""
        self.position = (
            randint(0, GRID_SIZE) * GRID_SIZE,
            randint(0, GRID_SIZE) * GRID_SIZE
            )

    def draw(self):
        """Это публичный метод, который делает что-то полезное."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инит змейки."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.last = None
        self.length = 2
        self.direction = (1, 0)
        self.next_direction = None

    # Метод draw класса Snake
    def draw(self):
        """Это публичный метод, который делает что-то полезное."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Поиск головы змейки."""
        return self.positions[0]

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.get_head_position()
        new_head_position = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE
            )

        if new_head_position[0] < 0:
            new_head_position = (SCREEN_WIDTH - GRID_SIZE, head_y)
        elif new_head_position[0] >= SCREEN_WIDTH:
            new_head_position = (0, head_y)

        if new_head_position[1] < 0:
            new_head_position = (head_x, SCREEN_HEIGHT - GRID_SIZE)
        elif new_head_position[1] >= SCREEN_HEIGHT:
            new_head_position = (head_x, 0)

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    # Сбрасывает змейку в начальное состояние
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 2
        self.direction = (1, 0)
        self.next_direction = None


def handle_keys(game_object):
    """Это публичный метод, который делает что-то полезное."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Это главная функция."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED - 3)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.move()
        snake.update_direction()
        pygame.display.update()
        # Тут опишите основную логику игры.
        if len(snake.positions) > snake.length:
            snake.positions.pop()
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            if apple.position == snake.positions:
                apple.randomize_position()
            else:
                apple.randomize_position()

        # Если змейка укусит хвост
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            pygame.display.update()

        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#           elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#           elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
