import pygame

from game_logic.food import Food
from game_logic.snake import Snake, SnakeAi, SHOW_GUI

FRAMERATE = 2000

SEGMENT_WIDTH = 20
SEGMENT_HEIGHT = 20
SEGMENT_MARGIN = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (211, 211, 211)


class App:

    def __init__(self, width=800, height=600):

        self.game_bound = {
            'min_x': 0,
            'max_x': width,
            'min_y': 100,
            'max_y': height,
            'width': width - 0,
            'height': height - 100
        }

        self.all_snakes = []
        self.dead_snakes = []
        self.score_board = pygame.Surface((width, 100))
        self.running = True
        self.max_score = 0
        if SHOW_GUI:
            pygame.init()
            pygame.font.init()

            self.font = pygame.font.Font('freesansbold.ttf', 20)
            self.score_text = self.font.render("Best score: " + str(self.max_score), True, RED)
            self.score_text_pos = self.score_text.get_rect()

            self.score_text_pos.centerx = self.score_board.get_rect().centerx - self.score_text.get_rect().width
            self.score_text_pos.centery = self.score_board.get_rect().centery

            self.screen = pygame.display.set_mode([self.game_bound['max_x'], self.game_bound['max_y']])
            pygame.display.set_caption('SnakeAI')
        self.clock = pygame.time.Clock()
        Food.initialize_food(self.game_bound)

    def _initialize(self, all_snakes):
        self.all_snakes = all_snakes
        self.running = True
        self.max_score = 0
        self.dead_snakes = []

    def go_left(self):
        for snake in self.all_snakes:
            if snake.on_vertical():
                snake.go_left()

    def go_right(self):
        for snake in self.all_snakes:
            if snake.on_vertical():
                snake.go_right()

    def go_up(self):
        for snake in self.all_snakes:
            if snake.on_horizontal():
                snake.go_up()

    def go_down(self):
        for snake in self.all_snakes:
            if snake.on_horizontal():
                snake.go_down()

    def move(self):
        for snake in self.all_snakes:
            snake.move(self.game_bound)

    def run(self, all_snakes, generation):
        self._initialize(all_snakes)
        Food.initialize_food(self.game_bound)
        while self.running:
            if SHOW_GUI:
                # pygame.event.get()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.go_left()
                        elif event.key == pygame.K_RIGHT:
                            self.go_right()
                        elif event.key == pygame.K_UP:
                            self.go_up()
                        elif event.key == pygame.K_DOWN:
                            self.go_down()

            for snake in self.all_snakes:
               snake.generate_ai_move()

            if SHOW_GUI:
                self.screen.fill(BLACK)
                self.score_board.fill(GREY)
                self.score_text = self.font.render("Best score: " + str(self.max_score) + "   generation: " +
                                                   str(generation) + "   alive: " + str(len(self.all_snakes)), True, RED)

            # Update
            self.move()
            if SHOW_GUI:
                for snake in self.all_snakes:
                    snake.food.draw(self.screen)
                    snake.draw(self.screen)
                    pygame.draw.rect(self.screen, RED, snake.head().rect, 3)

                self.score_board.blit(self.score_text, self.score_text_pos)

            for snake in self.all_snakes:
                snake.check_collides()
                if not snake.alive:
                    self.dead_snakes.append(snake)
                    self.all_snakes.remove(snake)

            if len(self.all_snakes) == 0:
                self.running = False
                pass
            for snake in self.all_snakes:
                new_score = snake.collides_food()
                if new_score > self.max_score:
                    self.max_score = new_score

            if SHOW_GUI:
                self.screen.blit(self.score_board, (0, 0))
                pygame.display.update()
            self.clock.tick(FRAMERATE)


if __name__ == '__main__':
    app = App()
    snake = SnakeAi(app)
    snake.model.model.load_weights(r'C:\Users\Dinbo-PC\Desktop\Snake\game_logic\weights\gen30.w')
    app.run([snake], 0)