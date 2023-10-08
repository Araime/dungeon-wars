import math
from random import randint

import pygame

from effects import Death
from images import char_animations, fireball_img
from settings import *
from weapons import Fireball


class Enemy:

    def __init__(self, x, y, health, attack, char_type, boss):
        self.x = x
        self.y = y
        self.char_type = char_type
        self.boss = boss
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

        # create pathfinder and matrix
        # self.matrix = []
        # self.pathfinder = None
        # if self.char_type != 0:
        #     self.matrix = matrix
        #     self.pathfinder = PathFinder()

        # define attack range
        self.attack_range = 0
        if self.char_type == 11:
            self.attack_range = BOSS_ATTACK_RANGE
        else:
            self.attack_range = ATTACK_RANGE

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def move(self, dx, dy, obstacle_tiles):
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

    def check_wall(self, x, y):
        return (x, y) not in self.matrix

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.rect.x + dx * TILE_SIZE), int(self.rect.y)):
            self.rect.x += dx
        if self.check_wall(int(self.rect.x), int(self.rect.y + dy * TILE_SIZE)):
            self.rect.y += dy

    def ai(self, player, obstacle_tiles, screen_scroll):
        damage = None
        dmg_pos = None
        fireball = None

        clipped_line = ()
        stun_cooldown = 100
        dx = 0
        dy = 0

        # reposition mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # create a line of sight from the enemy to the player
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))

        if self.alive:
            # check if line of sight passes through an obstacle tile
            for obstacle in obstacle_tiles:
                if obstacle[1].clipline(line_of_sight):
                    clipped_line = obstacle[1].clipline(line_of_sight)

            # check distance to player
            dist = math.sqrt(
                ((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centery - player.rect.centery) ** 2)
            )
            if not clipped_line and dist > RANGE:
                if self.rect.centerx > player.rect.centerx:
                    dx = -ENEMY_SPEED
                if self.rect.centerx < player.rect.centerx:
                    dx = ENEMY_SPEED
                if self.rect.centery > player.rect.centery:
                    dy = -ENEMY_SPEED
                if self.rect.centery < player.rect.centery:
                    dy = ENEMY_SPEED

            if not self.stunned:
                # move towards player
                self.move(dx, dy, obstacle_tiles)

                # attack player
                if dist < self.attack_range and not self.do_hit:
                    damage = self.attack + randint(-3, 3)
                    dmg_pos = player.rect
                    player.health -= damage
                    self.do_hit = True
                    self.last_attack = pygame.time.get_ticks()

                # boss enemies shoot fireballs
                fireball_cooldown = 700
                if self.boss:
                    if dist < 500:
                        if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                            fireball = Fireball(
                                fireball_img,
                                self.rect.centerx,
                                self.rect.centery,
                                player.rect.centerx,
                                player.rect.centery,
                                self.attack
                            )
                            self.last_attack = pygame.time.get_ticks()

            # check if hit
            if self.hit:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                if self.char_type != 11:
                    self.stunned = True
                self.running = False
                self.update_action(0)

            if pygame.time.get_ticks() - self.last_hit > stun_cooldown:
                self.stunned = False

        return damage, dmg_pos, fireball

    def update(self):
        # reset variables
        death = None

        # reset taking a trap hit
        hit_cooldown = 1000
        if self.trap_hit and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
            self.trap_hit = False

        # reset monster deal damage to player
        if self.char_type != 6:
            if self.do_hit and (pygame.time.get_ticks() - self.last_attack) > hit_cooldown:
                self.do_hit = False

        # check if enemy is died
        if self.health < 0:
            self.health = 0
            self.alive = False
            death = Death(self.rect.centerx, self.rect.centery)

        # check what action is performing
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

        return death

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
