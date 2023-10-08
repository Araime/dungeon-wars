import pygame


class AnimatedTile(pygame.sprite.Sprite):

    def __init__(self, x, y, animation_list, animation_cd):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = animation_list
        self.frame_index = 0
        self. animation_cd = animation_cd
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, screen_scroll, player):
        # reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # handle animation
        # update image
        self.image = self.animation_list[self.frame_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > self. animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if animation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
