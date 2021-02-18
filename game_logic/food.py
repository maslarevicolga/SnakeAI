import pygame
import random
import numpy as np

GREEN = (0, 255, 0)

FOOD_NUMBER = 1000
SEGMENT_WIDTH = 20
SEGMENT_HEIGHT = 20
SEGMENT_MARGIN = 5


class Food(pygame.sprite.Sprite):

    coordinates = []

    def __init__(self, x_bound, y_bound):
        super().__init__()

        self.start_y = None
        self.start_x = None
        self.coordinates = []

        self.index = 0
        self.image = pygame.Surface([SEGMENT_WIDTH, SEGMENT_HEIGHT])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.x_bound = x_bound
        self.y_bound = y_bound

    @staticmethod
    def initialize_food(game_bounds):
        Food.index = 0
        Food.coordinates = []
        segment_x_size = SEGMENT_WIDTH + SEGMENT_MARGIN
        segment_y_size = SEGMENT_HEIGHT + SEGMENT_MARGIN
        rand_x = np.random.randint(game_bounds['min_x'] // segment_x_size, game_bounds['max_x'] // segment_x_size - 1, (FOOD_NUMBER,), dtype='int64')
        rand_y = np.random.randint(game_bounds['min_y'] // segment_y_size, game_bounds['max_y'] // segment_y_size - 1, (FOOD_NUMBER,), dtype='int64')
        for i in range(FOOD_NUMBER):
            Food.coordinates.append([rand_x[i] * segment_x_size + SEGMENT_MARGIN, rand_y[i] * segment_y_size + SEGMENT_MARGIN])

    def generate(self):
        if self.index == len(Food.coordinates):
            self.index = 0
            print('!!!FOOD OVERFLOW!!!')

        self.rect.x = Food.coordinates[self.index][0]
        self.rect.y = Food.coordinates[self.index][1]
        self.index += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
