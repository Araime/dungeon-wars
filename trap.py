from random import randint

import pygame

from images import trap_animation


class Trap(pygame.sprite.Sprite):

    def __init__(self, x, y, waiting=False):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = trap_animation
        self.frame_index = 0
        self.animation_cd = 50
        self.waiting_cd = 2000
        self.waiting = waiting
        self.danger = False
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, screen_scroll, player, enemy_list):
        # reset variables
        damage = 0
        dmg_pos = None

        # reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # check if tile has been collided with the player
        if self.danger:
            if not player.trap_hit:
                if self.rect.colliderect(player.rect):
                    damage = 10 + randint(-5, 5)
                    dmg_pos = player.rect
                    player.health -= damage
                    player.trap_hit = True
                    player.last_hit = pygame.time.get_ticks()

            # check if tile has been collided with the enemy
            for enemy in enemy_list:
                if not enemy.trap_hit:
                    if self.rect.colliderect(enemy.rect):
                        damage = 20 + randint(-5, 5)
                        dmg_pos = enemy.rect
                        enemy.health -= damage
                        enemy.trap_hit = True
                        enemy.last_hit = pygame.time.get_ticks()

        # handle animation
        # update image
        self.image = self.animation_list[self.frame_index]

        # open a trap
        if not self.danger and not self.waiting:
            if self.frame_index < len(self.animation_list) - 1:
                # check if enough time has passed since the last update
                if pygame.time.get_ticks() - self.update_time > self.animation_cd:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()

            # check if animation has finished
            if self.frame_index == len(self.animation_list) - 1:
                self.danger = True
                self.waiting = True
        # close a trap
        elif self.danger and not self.waiting:
            # check if animation has finished
            if self.frame_index > 0:
                # check if enough time has passed since the last update
                if pygame.time.get_ticks() - self.update_time > self.animation_cd:
                    self.frame_index -= 1
                    self.update_time = pygame.time.get_ticks()

            # check if animation has finished
            if self.frame_index == 0:
                self.danger = False
                self.waiting = True

        # check if waiting has finished
        if self.waiting:
            if pygame.time.get_ticks() - self.update_time > self.waiting_cd:
                self.update_time = pygame.time.get_ticks()
                self.waiting = False

        return damage, dmg_pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
