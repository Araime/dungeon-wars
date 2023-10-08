import math
from random import randint

import pygame

from effects import Death
from images import char_animations, fireball_img
from settings import *
from weapons import Fireball


class Character:

    def __init__(self, x, y, health, attack, char_type):
        self.x = x
        self.y = y
        self.char_type = char_type
        self.score = 0
        self.flip = False
        self.animation_list = char_animations[self.char_type]
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        self.locate = False
        self.hit = False
        self.do_hit = False
        self.trap_hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned = False
        self.attack = attack
        self.power = 0
        self.boosting = False

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def move(self, dx, dy, obstacle_tiles, exit_tile=None):
        screen_scroll = [0, 0]
        level_complete = False
        self.running = False

        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        # check for collision with map in x direction
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            # check for collision
            if obstacle[1].colliderect(self.rect):
                # check which side the collision is from
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right

        # check for collision with map in y direction
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            # check for collision
            if obstacle[1].colliderect(self.rect):
                # check which side the collision is from
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        # logic only applicable to player
        if self.char_type == 0:
            # check collision with exit tile
            if exit_tile[1].colliderect(self.rect):
                # ensure player is close to the center of the exit tile
                exit_dist = math.sqrt(
                    ((self.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.rect.centery - exit_tile[1].centery) ** 2)
                )
                if exit_dist < 30:
                    level_complete = True

            # update scroll based on player position
            # move camera left and right
            if self.rect.right > (SCREEN_WIDTH - SCROLL_THRESH):
                screen_scroll[0] = (SCREEN_WIDTH - SCROLL_THRESH) - self.rect.right
                self.rect.right = SCREEN_WIDTH - SCROLL_THRESH
            if self.rect.left < SCROLL_THRESH:
                screen_scroll[0] = SCROLL_THRESH - self.rect.left
                self.rect.left = SCROLL_THRESH

            # move camera up and down
            if self.rect.bottom > (SCREEN_HEIGHT - SCROLL_THRESH):
                screen_scroll[1] = (SCREEN_HEIGHT - SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = SCREEN_HEIGHT - SCROLL_THRESH
            if self.rect.top < SCROLL_THRESH:
                screen_scroll[1] = SCROLL_THRESH - self.rect.top
                self.rect.top = SCROLL_THRESH

        return screen_scroll, level_complete

    def update(self):
        # reset player taking a hit
        hit_cooldown = 1000
        if self.trap_hit and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
            self.trap_hit = False

        # reset monster deal damage to player
        if self.char_type != 6:
            if self.do_hit and (pygame.time.get_ticks() - self.last_attack) > hit_cooldown:
                self.do_hit = False

        # check if character is died
        if self.health < 0:
            self.health = 0
            self.alive = False

        # check what action the player is performing
        if self.running:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle

        animation_cooldown = 100
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
