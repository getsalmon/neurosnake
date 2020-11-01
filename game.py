import random

import pygame


class Snake:
    def __init__(self, init_length=10):
        self.current_position = (2, 3)
        self.current_vector = (1, 0)
        self.pos_array = [(self.current_position[0] + i, self.current_position[1]) for i in range(init_length)]

    def get_vector(self):
        return self.current_vector

    def get_position(self):
        return self.current_position

    def get_head(self):
        return self.pos_array[-1]

    def get_new_head(self):
        head = self.get_head()
        vec = self.get_vector()
        return head[0] + vec[0], head[1] + vec[1]

    def update(self, enlarge=False):
        start_pos = 0 if enlarge else 1
        self.pos_array = self.pos_array[start_pos:] + [self.get_new_head()]

    def update_vector(self, new_vector):
        if new_vector and self.current_vector[0] != new_vector[0] and self.current_vector[1] != new_vector[1]:
            self.current_vector = new_vector


class Graphic:
    def __init__(self, field):
        w, h = field
        self.block_size = 20
        self.surface_size = (w * self.block_size, h * self.block_size)
        self.surface = pygame.display.set_mode(self.surface_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.brick = self.init_brick()
        self.apple = self.init_apple()
        self.font = pygame.font.SysFont('consolas', 12)

    def init_brick(self):
        margin = 2
        brick = pygame.Surface((self.block_size, self.block_size))
        pygame.draw.rect(brick, pygame.Color('blue'), [0, 0, self.block_size, self.block_size])
        pygame.draw.rect(
            brick, pygame.Color('tomato'),
            [margin, margin, self.block_size - 2 * margin, self.block_size - 2 * margin]
        )
        return brick

    def init_apple(self):
        apple = pygame.Surface((self.block_size, self.block_size))
        pygame.draw.rect(apple, pygame.Color('green'), [0, 0, self.block_size, self.block_size])
        return apple

    def get_draw_pos(self, pos):
        return [pos[0] * self.block_size, pos[1] * self.block_size]

    def draw_debug(self, snake, apple_pos):
        msg = f'Len: {len(snake)}\nHead: {snake[-1]}\nApple:{apple_pos}'
        parts = msg.split('\n')
        for i in range(len(parts)):
            surface = self.font.render(parts[i], True, (0xFF, 0xFF, 0xFF))
            h_margin = (len(parts)-i)*15
            self.surface.blit(surface, (self.surface_size[0] - 100, self.surface_size[1] - h_margin))

    def redraw(self, snake_arr, apple_pos=None):
        self.surface.fill((0, 0, 0))
        if apple_pos:
            self.surface.blit(self.apple, self.get_draw_pos(apple_pos))
        for elem in snake_arr:
            self.surface.blit(self.brick, self.get_draw_pos(elem))
        self.draw_debug(snake_arr, apple_pos)
        pygame.display.flip()


class GameLogic:
    def __init__(self, snake, field):
        self.snake = snake
        self.field = field
        self.apple_pos = self.generate_apple()

    def generate_apple(self):
        while True:
            pos_x = random.randint(0, self.field[0]-1)
            pos_y = random.randint(0, self.field[1]-1)
            if (pos_x, pos_y) not in self.snake.pos_array:
                return pos_x, pos_y

    def restart(self):
        self.snake = Snake()
        self.apple_pos = self.generate_apple()

    def is_restart(self):
        new_head = self.snake.get_new_head()
        return (
                new_head[0] < 0
                or new_head[1] < 0
                or new_head[0] >= self.field[0]
                or new_head[1] >= self.field[1]
                or new_head in self.snake.pos_array
        )

    def update(self):
        if self.is_restart():
            self.restart()
            return
        enlarge = self.snake.get_new_head() == self.apple_pos
        self.snake.update(enlarge)
        if enlarge:
            self.apple_pos = self.generate_apple()

    def update_vector(self, new_vector):
        self.snake.update_vector(new_vector)


def play():
    field = (40, 20)
    pygame.init()
    pygame.font.init()
    gr = Graphic(field)
    gl = GameLogic(Snake(), field)

    vector_dict = {
        pygame.K_LEFT: (-1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_RIGHT: (1, 0),
        pygame.K_DOWN: (0, 1)
    }

    while 1:
        new_vector = None
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                new_vector = vector_dict.get(e.key)

        gl.update_vector(new_vector)
        gl.update()
        gr.redraw(gl.snake.pos_array, gl.apple_pos)
        pygame.time.wait(500)


if __name__ == '__main__':
    play()
