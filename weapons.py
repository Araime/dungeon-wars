import math
from random import randint

import pygame

from settings import ARROW_SPEED, FIREBALL_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from images import arrow_img, bow_img


class Weapon:

    def __init__(self):
        self.original_image = bow_img
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.arrow_image = arrow_img
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shoot_cd = 300
        arrow = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)  # -ve, because pygame y coordinate increase down the screen
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # get mouse click
        if pygame.mouse.get_pressed()[0] and not self.fired and (pygame.time.get_ticks() - self.last_shot) > shoot_cd:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle, player.attack)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

        # reset mouse click
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(
            self.image,
            ((self.rect.centerx - int(self.image.get_width() / 2)),
             self.rect.centery - int(self.image.get_height() / 2))
        )


class Arrow(pygame.sprite.Sprite):

    def __init__(self, image, x, y, angle, attack):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.attack = attack

        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * ARROW_SPEED)

    def update(self, screen_scroll, obstacle_tiles, enemy_list, power):
        # reset variables
        damage = 0
        dmg_pos = None

        # reposition based on the screen scroll
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check for collision between arrow and tile walls
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        # check if arrow has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # check collision between arrow and enemies
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = self.attack + randint(0, 5) + power
                dmg_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()
                break

        return damage, dmg_pos

    def draw(self, surface):
        surface.blit(
            self.image,
            ((self.rect.centerx - int(self.image.get_width() / 2)),
             self.rect.centery - int(self.image.get_height() / 2))
        )


class Fireball(pygame.sprite.Sprite):

    def __init__(self, image, x, y, target_x, target_y, attack):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist = target_x - x
        y_dist = -(target_y - y)

        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.attack = attack

        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * FIREBALL_SPEED)

    def update(self, screen_scroll, player):
        # reset variables
        damage = 0
        dmg_pos = None

        # reposition based on the screen scroll
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check if fireball has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # check collision with player
        if player.rect.colliderect(self.rect):
            damage = self.attack + randint(-5, 5)
            dmg_pos = player.rect
            player.health -= damage
            self.kill()

        return damage, dmg_pos

    def draw(self, surface):
        surface.blit(
            self.image,
            ((self.rect.centerx - int(self.image.get_width() / 2)),
             self.rect.centery - int(self.image.get_height() / 2))
        )
