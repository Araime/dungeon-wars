import pygame

from sounds import pickup_sounds


class Item(pygame.sprite.Sprite):

    def __init__(self, x, y, item_type, animation_list, dummy_gem=False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type  # 0: gem, 1: cherry
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_gem = dummy_gem

    def update(self, screen_scroll, player):
        # doesn't apply to the dummy gem that is always displayer at the top of the screen
        if not self.dummy_gem:
            # reposition based on screen scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]

        # check to see if items has been collected by the player
        if self.rect.colliderect(player.rect):
            # coin collected
            if self.item_type == 0:
                player.score += 1
                pickup_sounds[0].play()
            elif self.item_type == 1:
                player.health += 25
                pickup_sounds[1].play()
                if player.health > 100:
                    player.health = 100
            elif self.item_type == 2:
                player.boosting = True
                pickup_sounds[2].play()
            self.kill()

        # handle animation
        animation_cd = 150

        # update image
        self.image = self.animation_list[self.frame_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if animation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
