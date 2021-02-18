import pygame

SEGMENT_WIDTH = 20
SEGMENT_HEIGHT = 20
WHITE = (255, 255, 255)


class SnakeSegment(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def collides_rect(self, rectangle):
        l1_x = rectangle.x
        l1_y = rectangle.y
        r1_x = rectangle.x + SEGMENT_WIDTH - 1
        r1_y = rectangle.y + SEGMENT_HEIGHT - 1
        l2_x = self.rect.x
        l2_y = self.rect.y
        r2_x = self.rect.x + SEGMENT_WIDTH - 1
        r2_y = self.rect.y + SEGMENT_HEIGHT - 1

        # return l1_x == l2_x and l1_y == l2_y

        if l1_x >= r2_x or l2_x >= r1_x:
            return False
        if l1_y >= r2_y or l2_y >= r1_y:
            return False
        return True

    # stavila sam da poziva nas check umesto ugradjeni
    # ovo se poziva samo iz snake.check_bounds fje
    def check_collision(self, sprite1):
        return self.collides_rect(sprite1)
        # return pygame.sprite.collide_rect(self, sprite1)
