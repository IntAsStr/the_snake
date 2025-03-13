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


class GameObject:
    """Родительский класс."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка объектов."""
        pass


class Apple(GameObject):
    """Структура яблока."""

    def __init__(self, snake_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions=None):
        """Рандомное появление яблока на поле."""
        if snake_positions is None:
            return Snake.positions
        while True:
            # Генерируем случайную позицию
            self.position = (
                randint(0, GRID_SIZE) * GRID_SIZE,
                randint(0, GRID_SIZE) * GRID_SIZE
            )

            if self.position not in snake_positions:
                break

        return self.position

    def draw(self):
        """Отрисовка яблочка."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Структура Змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    # Метод draw класса Snake
    def draw(self):
        """Отрисовка змейки."""
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

    def get_snake_position(self):
        """Поиск всей змейки."""
        return self.positions

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Проверка границ экрана (ps.Заметка для ревью делал с помощью gpt
        # логику понял но сам до такого догадаться не смог)
        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT

        if new_head_x < 0:
            new_head_x += SCREEN_WIDTH
        if new_head_y < 0:
            new_head_y += SCREEN_HEIGHT

        new_head_position = (new_head_x, new_head_y)

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    # Сбрасывает змейку в начальное состояние
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 1
        self.last = None
        self.direction = (1, 0)
        self.next_direction = None


class QuitGameError(Exception):
    """Ошибка, возникающая при закрытии игры."""

    print('Игра закрыта пользователем')


def handle_keys(game_object):
    """Назначение направления движения змейки и выхода из игры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise QuitGameError
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
    snake = Snake()
    apple = Apple(snake.positions)
    running = True
    while running:
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake_head = snake.get_head_position()

        # поедание яблочка.
        if snake_head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Если змейка укусит хвост
        if snake_head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        clock.tick(SPEED)
        apple.draw()
        snake.move()
        snake.update_direction()
        snake.draw()
        pygame.display.update()
        try:
            handle_keys(snake)
        except QuitGameError:
            running = False
            pygame.quit()


if __name__ == '__main__':
    main()
