import pygame
import numpy as np
import math
from game_logic.ai_model import SnakeModel
from game_logic.food import Food
from game_logic.segment import SnakeSegment
from game_logic.params import *

SEGMENT_WIDTH = 20
SEGMENT_HEIGHT = 20
SEGMENT_MARGIN = 5


class Snake(pygame.sprite.Group):
    id_snake = 0

    def __init__(self, game, length=3):
        super().__init__()
        self.id = Snake.id_snake
        self.game = game
        Snake.id_snake += 1
        self.start_x = self.game.game_bound['min_x'] + self.game.game_bound['width'] // 2 + SEGMENT_MARGIN
        self.start_y = self.game.game_bound['min_y'] + self.game.game_bound['height'] // 2 + SEGMENT_MARGIN
        self.length = length
        self.game_bound = self.game.game_bound
        self.snake_segments = []
        self.my_score = 0
        self.alive = True
        self.segment_width = SEGMENT_WIDTH
        self.segment_height = SEGMENT_HEIGHT
        self.segment_margin = SEGMENT_MARGIN
        self.last_removed = None

        self.segment_size = self.segment_width + self.segment_margin

        self.food = Food((self.game_bound['min_x'], self.game_bound['max_x']),
                         (self.game_bound['min_y'], self.game_bound['max_y']))
        self.food.generate()

        for i in range(self.length):
            x = self.start_x - self.segment_size * i
            y = self.start_y
            self.add_segment(x, y)

        self.x_speed = 1
        self.y_speed = 0
        self.reason_died = 'Alive'

    def get_dist_food(self) -> list:
        center_x = self.food.rect.x
        center_y = self.food.rect.y
        dist_x = center_x - self.head().x
        dist_y = center_y - self.head().y
        return [dist_x, dist_y]

    def check_bounds(self, x_next_speed, y_next_speed):
        '''
        :return: True if colides with something, else folse
        '''
        x_new = self.head().x + x_next_speed * (SEGMENT_WIDTH + SEGMENT_MARGIN)
        y_new = self.head().y + y_next_speed * (SEGMENT_HEIGHT + SEGMENT_MARGIN)
        if x_new < self.game_bound['min_x'] or x_new > self.game_bound['max_x']:
            return True
        if y_new < self.game_bound['min_y'] or y_new > self.game_bound['max_y']:
            return True

        new_segment = SnakeSegment(x_new, y_new, self.segment_width, self.segment_height)
        for segment in self.tail()[:-1]:
            if new_segment.check_collision(segment):
                return True
        return False

    def get_state(self) -> list:
        forward_state = self.check_bounds(self.x_speed, self.y_speed)
        if self.on_horizontal():
            left_speed = [0, -1 if self.x_speed == 1 else 1]
            right_speed = [0, 1 if self.x_speed == 1 else -1]
        else:
            left_speed = [-1 if self.y_speed == -1 else 1, 0]
            right_speed = [1 if self.y_speed == -1 else -1, 0]

        left_state = self.check_bounds(left_speed[0], left_speed[1])
        right_state = self.check_bounds(right_speed[0], right_speed[1])
        return [forward_state, left_state, right_state]

    def die(self, reason):
        self.alive = False
        self.reason_died = reason

    def check_collides(self):
        x = self.head().x
        y = self.head().y
        if (x > self.game_bound['max_x']) or (x < self.game_bound['min_x']):
            self.die('wall')
        if (y > self.game_bound['max_y']) or (y < self.game_bound['min_y']):
            self.die('wall')
        if self.collides_body(self.tail()):
            self.die('body')

    def add_segment(self, x, y, index=None):
        if index is None:
            index = self.length
        segment = SnakeSegment(x, y, self.segment_width, self.segment_height)
        self.snake_segments.insert(index, segment)
        self.add(segment)
        self.length += 1

    def pop(self):
        last_segment = self.snake_segments.pop()
        self.last_removed = last_segment
        self.remove(last_segment)
        self.length -= 1

    def head(self):
        return self.snake_segments[0]

    def tail(self):
        return self.snake_segments[1:]

    def on_horizontal(self):
        return self.y_speed == 0

    def on_vertical(self):
        return self.x_speed == 0

    def go_left(self):
        self.x_speed = -1
        self.y_speed = 0

    def go_right(self):
        self.x_speed = 1
        self.y_speed = 0

    def go_up(self):
        self.x_speed = 0
        self.y_speed = -1

    def go_down(self):
        self.x_speed = 0
        self.y_speed = 1

    def turn_left(self):
        self.x_speed, self.y_speed = self.y_speed, -self.x_speed

    def turn_right(self):
        self.x_speed, self.y_speed = -self.y_speed, self.x_speed

    def move(self, bound):
        if self.alive:
            self.pop()
            x = self.head().x + self.x_speed * self.segment_size
            y = self.head().y + self.y_speed * self.segment_size
            self.add_segment(x, y, 0)

    def collides_rect(self, rectangle):
        l1_x = rectangle.x
        l1_y = rectangle.y
        r1_x = rectangle.x + SEGMENT_WIDTH - 1
        r1_y = rectangle.y + SEGMENT_HEIGHT - 1
        l2_x = self.head().x
        l2_y = self.head().y
        r2_x = self.head().x + SEGMENT_WIDTH - 1
        r2_y = self.head().y + SEGMENT_HEIGHT - 1

        # return l1_x == l2_x and l1_y == l2_y

        if l1_x >= r2_x or l2_x >= r1_x:
            return False
        if l1_y >= r2_y or l2_y >= r1_y:
            return False
        return True

    def eat(self):
        self.my_score += 1
        self.food.generate()
        return self.my_score

    def grow(self):
        self.add_segment(self.last_removed.rect.x, self.last_removed.rect.y)

    def collides_food(self):
        if self.collides_rect(self.food.rect):
            new_score = self.eat()
            self.grow()
            return new_score
        return self.my_score

    def collides_body(self, group):
        for sprite in group:
            if self.collides_rect(sprite.rect):
                return True
        return False


class SnakeAi(Snake):

    def __init__(self, game, length=3):

        super().__init__(game, length)
        self.model = SnakeModel()
        self.fitness_score = 0
        self.pity_timer = PITY_TIMER
        self.visited = set()
        self.previous_distance = (99999, 99999)

    def _update_speed(self, speed_list: np.array):
        next_move = np.argmax(speed_list)
        if next_move == 0:
            self.turn_left()
        elif next_move == 1:
            self.turn_right()

    def _update_position_tracing(self):
        position = (self.head().x, self.head().y, self.x_speed, self.y_speed)
        if position not in self.visited:
            if RESET_PITY_ON_NEW:
                self.pity_timer = PITY_TIMER
            self.visited.add(position)
        else:
            self.pity_timer -= PUNISH_TIMER_ALREADY_VISITED
            self.fitness_score -= PUNISH_ALREADY_VISITED

    def move(self, bound):
        super(SnakeAi, self).move(bound)
        if self.alive:
            self.fitness_score += REWARD_DISTANCE_TRAVELED
            self.pity_timer -= 1
            self._update_position_tracing()
            if self.pity_timer <= 0:
                self.die('timeout')
            x_dist, y_dist = self.get_dist_food()
            if abs(x_dist) < abs(self.previous_distance[0]) or abs(y_dist) < abs(self.previous_distance[1]):
                self.fitness_score += REWARD_CLOSER_TO_FOOD
            else:
                self.fitness_score -= PUNISH_FURTHER_FROM_FOOD
            self.previous_distance = x_dist, y_dist

    def die(self, reason: str):
        super(SnakeAi, self).die(reason)
        self.fitness_score += len(self.visited) * REWARD_NEW_TILE_VISITED
        if reason == 'timeout':
            self.fitness_score -= PUNISH_DEATH

    def eat(self):
        self.fitness_score += REWARD_FOOD_EAT
        if RESET_PITY_ON_EAT:
            self.pity_timer = PITY_TIMER
        self.visited = set()
        return super(SnakeAi, self).eat()

    def generate_ai_move(self):
        if self.alive:
            # self.x_speed = 1
            model_input = np.array(self.get_state())
            model_input = np.append(model_input, [self.x_speed, self.y_speed])
            food_x, food_y = self.get_dist_food()
            food_distance = math.sqrt(food_x ** 2 + food_y ** 2)
            food_vector = [sign(food_x), sign(food_y)]
            model_input = np.append(model_input, food_vector)
            # model_input = np.append(model_input, [food_distance / 800])
            speed = self.model.predict(model_input)
            self._update_speed(speed)


def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0
