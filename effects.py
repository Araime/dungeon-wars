import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from images import death_animation


class DamageText(pygame.sprite.Sprite):

    def __init__(self, x, y, damage, colour, font):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.image = self.font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, screen_scroll):
        # reposition based on the screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # move damage text up
        self.rect.y -= 1

        # delete the counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


class Death(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = death_animation
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, screen_scroll):
        # reposition based on the screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # handle animation
        animation_cd = 80

        # update image
        self.image = self.animation_list[self.frame_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if animation has finished
        if self.frame_index >= len(self.animation_list):
            self.kill()


class ScreenFade:

    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self, surface):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(surface, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(surface, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(surface, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(surface, self.colour, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        elif self.direction == 2:
            # 192 384 576 768
            pygame.draw.rect(surface, self.colour, (0, 0, 0 + self.fade_counter, 192))
            pygame.draw.rect(surface, self.colour, (SCREEN_WIDTH - self.fade_counter, 192, SCREEN_WIDTH + self.fade_counter, 192))
            pygame.draw.rect(surface, self.colour, (0, 384, 0 + self.fade_counter, 192))
            pygame.draw.rect(surface, self.colour, (SCREEN_WIDTH - self.fade_counter, 576, SCREEN_WIDTH + self.fade_counter, 192))

        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete
