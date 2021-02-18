import os

from game_logic.snake import SnakeAi
from game_logic.params import *
from time import time

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import keras
import numpy as np
from game_logic.game import App, SEGMENT_MARGIN
import glob


class Trainer:

    def __init__(self, save_name):
        self.start_time = time()
        self.save_name = save_name
        self.app = App()
        self.all_snakes = []

    def run(self):
        self._empty_weight_directory()
        self._create_snakes()
        for i in range(GENERATION_NUMBER):
            self.train_timestamp_start = time()
            self.app.run(self.all_snakes, i)
            self.train_timestamp_died = time()
            self.all_snakes = self.app.dead_snakes
            self._print_generation_stats(i)
            self._log_gen(i)
            if i % LOG_WEIGHTS_GENERATION == 0:
                self.save_best('gen' + str(i))
            self._breed_snakes()
            print('breed: ', time() - self.train_timestamp_died)
        self.save_best('gen' + str(GENERATION_NUMBER))

    def _print_generation_stats(self, gen):
        print(self._get_print_string(gen))

    def _empty_weight_directory(self):
        if os.path.isdir(self.save_name):
            files = glob.glob(self.save_name + '\\*')
            for f in files:
                os.remove(f)

    def _log_gen(self, gen):
        os.makedirs(self.save_name, exist_ok=True)
        with open(os.path.join(self.save_name, 'log.txt'), 'a+') as log_out:
            log_out.write(self._get_print_string(gen))

    def _get_print_string(self, gen) -> str:
        print_str = ['---------- GEN {} ----------'.format(gen)]
        print_str += ['{:3} | {:7} | {:3} | {}'.format(index, snake.fitness_score, snake.my_score, snake.reason_died) for index, snake in enumerate(self.all_snakes)]
        best, = self._get_best_snakes(1)
        print_str += ['Best snake fitness: {}\n'.format(best.fitness_score)]
        print_str += ['time_died: ' + str(self.train_timestamp_died - self.train_timestamp_start)]
        return '\n'.join(print_str)

    def _create_snakes(self):
        self.all_snakes = []
        for i in range(POPULATION - len(self.all_snakes)):
            snake = SnakeAi(self.app, length=SNAKE_LENGTH)
            self.all_snakes.append(snake)

    def _breed_snakes(self):
        best_snakes = self._get_best_snakes(DONT_MUTATE + DONT_MUTATE * 3)
        new_generation_snakes = []
        new_generation_snakes += self._snake_copies(best_snakes)
        for i in range(POPULATION - len(new_generation_snakes)):
            id_parent_1, id_parent_2 = np.random.permutation(len(best_snakes))[:2]
            parent_1 = best_snakes[id_parent_1]
            parent_2 = best_snakes[id_parent_2]
            mutation_param = self._get_mutation_param(i)
            snake = self._generate_snake(parent_1, parent_2, mutation_param)
            new_generation_snakes.append(snake)
        self.all_snakes = new_generation_snakes

    def _get_mutation_param(self, i: int) -> float:
        param = [1.] * DONT_MUTATE
        param += [0.9] * 5
        param += [0.8] * 5
        param += [0.7] * 5
        param += [0.6] * 5
        param += [0.5] * 5
        if i >= len(param):
            return 0.85
        else:
            return param[i]

    def _generate_snake(self, snake_parent_1, snake_parent_2, mutation_param) -> SnakeAi:
        snake = SnakeAi(self.app, SNAKE_LENGTH)

        weight = self._get_combined_weights(snake_parent_1.model.model, snake_parent_2.model.model)
        snake.model.model.set_weights(weight)
        self._mutate_weights(snake.model.model, mutation_param)
        return snake

    def _mutate_weights(self, model: keras.Sequential, mutation_param: float):
        if mutation_param < 0 or mutation_param > 1:
            raise ValueError('Mutation param out of bounds')

        weights = model.get_weights()
        weight_list = []
        for w in weights:
            orig_shape = w.shape
            flat = w.flatten()
            mutation_choice = np.random.rand(flat.shape[0])
            mutation_val = np.random.rand(flat.shape[0]) * 2 - 1
            flat = np.where(mutation_choice > mutation_param, mutation_val * flat, flat)
            weight_list.append(flat.reshape(orig_shape))
        model.set_weights(weight_list)

    def _get_combined_weights(self, model1: keras.Sequential, model2: keras.Sequential):
        weight1 = model1.get_weights()
        weight2 = model2.get_weights()
        weight_list = []
        for i in range(len(weight1)):
            orig_shape = weight1[i].shape
            flat1 = weight1[i].flatten()
            flat2 = weight2[i].flatten()
            choice = np.random.rand(flat1.shape[0])
            z = np.where(choice > 0.5, flat1, flat2)
            weight_list.append(z.reshape(orig_shape))

        return weight_list

    def _get_best_snakes(self, number_of_snakes) -> list:
        snakes_scores = [snake.fitness_score for snake in self.all_snakes]
        snakes_scores = np.array(snakes_scores)
        best_snakes = []
        for i in range(number_of_snakes):
            id_best = np.argmax(snakes_scores)
            snakes_scores[id_best] = -(2 ** 31)
            best_snakes.append(self.all_snakes[id_best])

        return best_snakes

    def save_best(self, name):
        best1, = self._get_best_snakes(1)
        best1.model.save_weights(name, self.save_name)

    def _snake_copies(self, best_snakes) -> list:
        new_snakes = []
        for snake in best_snakes:
            copy_snake = self._generate_snake(snake, snake, 1.)
            new_snakes.append(copy_snake)
        return new_snakes


if __name__ == '__main__':
    for i in range(TRAINING_NUM):
        trainer = Trainer('trainset_1\\snake_' + str(i))
        trainer.run()
        print('Done ' + str(i))
