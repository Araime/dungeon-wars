import csv
from os import getcwd, listdir, path
from random import randint

import pygame

from button import Button
from settings import *
from character import Character
from effects import DamageText, ScreenFade
from images import *
from items import Item
from sounds import *
from weapons import Weapon
from world import World

pygame.mixer.init()
STOPPED_PLAYING = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(STOPPED_PLAYING)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Dungeon Wars')

# create clock for maintaining frame rate
clock = pygame.time.Clock()

# define path variables
res_dir = path.join(path.dirname(__file__), 'resources')
lvl_dir = path.join(getcwd(), 'levels')
mus_dir = path.join(res_dir, 'music')

# define game variables
level = 1
total_enemies = 0
level_complete = False
start_game = False
pause_game = False
start_intro = False
screen_scroll = [0, 0]
track = randint(1, 5)
max_track = len(listdir(mus_dir))

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font
font = pygame.font.Font(path.join(res_dir, 'fonts', 'AtariClassic.ttf'), 20)


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for displaying game info
def draw_info(health):
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50))

    # draw lives
    half_heart_draw = False
    for i in range(5):
        if health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (health % 20) > 0 and not half_heart_draw:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_draw = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))

    # level
    draw_text(f'LEVEL: {level}', font, WHITE, 450, 15)

    # weapon power
    draw_text(f'POW: {player.power}', font, WHITE, 650, 15)

    # show score
    draw_text(f'x{player.score}', font, WHITE, SCREEN_WIDTH - 100, 15)


# function to reset level
def reset_level():
    damage_txt_group.empty()
    arrow_group.empty()
    item_group.empty()
    death_group.empty()
    fireball_group.empty()
    trap_group.empty()
    a_decor_tiles_group.empty()
    a_upper_tiles_group.empty()

    # create empty layers lists
    lower_world_data = []
    decor_world_data = []
    upper_world_data = []

    # lower layer
    for row in range(ROWS):
        r = [-1] * COLS
        lower_world_data.append(r)

    # decor layer
    for row in range(ROWS):
        r = [-1] * COLS
        decor_world_data.append(r)

    # upper layer
    for row in range(ROWS):
        r = [-1] * COLS
        upper_world_data.append(r)

    return lower_world_data, decor_world_data, upper_world_data


# function to load level
def load_level_layers_data():
    # lower
    with open(path.join(lvl_dir, f'level{level}_lower_data.csv'), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                lower_world_data[x][y] = int(tile)

    # decor
    with open(path.join(lvl_dir, f'level{level}_decor_data.csv'), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                decor_world_data[x][y] = int(tile)

    # upper
    with open(path.join(lvl_dir, f'level{level}_upper_data.csv'), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                upper_world_data[x][y] = int(tile)

    return lower_world_data, decor_world_data, upper_world_data


# load music
pygame.mixer.music.load(path.join(mus_dir, f'Action {track}.wav'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(fade_ms=5000)

# create empty layers lists
lower_world_data = []
decor_world_data = []
upper_world_data = []

# lower layer
for row in range(ROWS):
    r = [-1] * COLS
    lower_world_data.append(r)

# decor layer
for row in range(ROWS):
    r = [-1] * COLS
    decor_world_data.append(r)

# upper layer
for row in range(ROWS):
    r = [-1] * COLS
    upper_world_data.append(r)

lower_world_data, decor_world_data, upper_world_data = load_level_layers_data()

world = World()
world.process_data(lower_world_data, decor_world_data, upper_world_data)

# create player
player = world.player

# create players weapon
bow = Weapon()

# extract enemies from world data
enemy_list = world.enemy_list

# define total_enemies variable
total_enemies = len(enemy_list)

# create sprite groups
damage_txt_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
death_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
trap_group = pygame.sprite.Group()
a_decor_tiles_group = pygame.sprite.Group()
a_upper_tiles_group = pygame.sprite.Group()

# create dummy gem
score_gem = Item(SCREEN_WIDTH - 115, 23, 0, gem_images, True)
item_group.add(score_gem)

# add the items from the level data
for item in world.item_list:
    item_group.add(item)

# add the a_tiles from the lower and decor layers level data
for item in world.a_decor_tiles_list:
    a_decor_tiles_group.add(item)

# add the a_tiles from the upper layer level data
for item in world.a_upper_tiles_list:
    a_upper_tiles_group.add(item)

# add the trap from the lower layer level data
for item in world.trap_list:
    trap_group.add(item)

# create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, RED, 4)

# create buttons
restart_btn = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 50, restart_img)
start_btn = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2 - 150, start_img)
resume_btn = Button(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 150, resume_img)
exit_btn = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img)

# main game loop
run = True
while run:
    # control frame rate
    clock.tick(FPS)

    # draw menu
    if not start_game:
        screen.blit(menu_img, (0, 0))
        if start_btn.draw(screen):
            start_game = True
            start_intro = True
        if exit_btn.draw(screen):
            run = False
    else:
        if pause_game:
            screen.fill(MENU_BG)
            if resume_btn.draw(screen):
                pause_game = False
            if exit_btn.draw(screen):
                run = False
        else:
            screen.fill(BG)

            if player.alive:
                # calculate player movement
                dx = 0
                dy = 0
                if moving_right:
                    dx = SPEED
                if moving_left:
                    dx = -SPEED
                if moving_up:
                    dy = -SPEED
                if moving_down:
                    dy = SPEED

                # move player
                screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)

                # update all objects
                world.update(screen_scroll)
                for trap in trap_group:
                    damage, dmg_pos = trap.update(screen_scroll, player, enemy_list)
                    if damage:
                        dmg_txt = DamageText(dmg_pos.centerx, dmg_pos.y, str(damage), YELLOW, font)
                        damage_txt_group.add(dmg_txt)
                        player_hit_snd.play()
                a_decor_tiles_group.update(screen_scroll, player)
                for enemy in enemy_list:
                    damage, dmg_pos, fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll)
                    if fireball:
                        fireball_group.add(fireball)
                        magic_snd.play()
                    if damage:
                        dmg_txt = DamageText(dmg_pos.centerx, dmg_pos.y, str(damage), YELLOW, font)
                        damage_txt_group.add(dmg_txt)
                        player_hit_snd.play()
                    if enemy.alive:
                        death = enemy.update()
                        if death:
                            death_group.add(death)
                            death_snd.play()
                            total_enemies -= 1
                player.update()
                arrow = bow.update(player)
                if arrow:
                    arrow_group.add(arrow)
                    shot_snd.play()
                for arrow in arrow_group:
                    damage, dmg_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list, player.power)
                    if damage:
                        dmg_txt = DamageText(dmg_pos.centerx, dmg_pos.y, str(damage), RED, font)
                        damage_txt_group.add(dmg_txt)
                        hit_snd.play()
                damage_txt_group.update(screen_scroll)
                for fireball in fireball_group:
                    damage, dmg_pos = fireball.update(screen_scroll, player)
                    if damage:
                        dmg_txt = DamageText(dmg_pos.centerx, dmg_pos.y, str(damage), YELLOW, font)
                        damage_txt_group.add(dmg_txt)
                        player_hit_snd.play()
                item_group.update(screen_scroll, player)
                death_group.update(screen_scroll)
                world.update_upper(screen_scroll)
                a_upper_tiles_group.update(screen_scroll, player)

            # draw player on screen
            world.draw(screen)
            trap_group.draw(screen)
            a_decor_tiles_group.draw(screen)
            for enemy in enemy_list:
                if enemy.alive:
                    enemy.draw(screen)
            player.draw(screen)
            bow.draw(screen)
            for arrow in arrow_group:
                arrow.draw(screen)
            for fireball in fireball_group:
                fireball.draw(screen)
            damage_txt_group.draw(screen)
            item_group.draw(screen)
            death_group.draw(screen)
            world.draw_upper(screen)
            a_upper_tiles_group.draw(screen)
            draw_info(player.health)
            score_gem.draw(screen)

            # check if weapon boosted
            if player.boosting:
                player.power += 1
                player.boosting = False
                boost_txt = DamageText(player.rect.centerx, player.rect.y, 'bow upgrade', SPRING_GREEN, font)
                damage_txt_group.add(boost_txt)

            # check level complete
            if level_complete and not total_enemies:
                start_intro = True
                level += 1
                temp_score = player.score
                temp_health = player.health
                tmp_pow = player.power
                lower_world_data, decor_world_data, upper_world_data = reset_level()

                # load level data and create world
                lower_world_data, decor_world_data, upper_world_data = load_level_layers_data()
                world = World()
                world.process_data(lower_world_data, decor_world_data, upper_world_data)
                player = world.player
                player.score = temp_score
                player.health = temp_health
                player.power = tmp_pow
                enemy_list = world.enemy_list
                total_enemies = len(enemy_list)
                score_gem = Item(SCREEN_WIDTH - 115, 23, 0, gem_images, True)
                item_group.add(score_gem)
                # add the items from the level data
                for item in world.item_list:
                    item_group.add(item)

                # add the a_tiles from the lower and decor layers level data
                for item in world.a_decor_tiles_list:
                    a_decor_tiles_group.add(item)

                # add the a_tiles from the upper layer level data
                for item in world.a_upper_tiles_list:
                    a_upper_tiles_group.add(item)

                # add the trap from the lower layer level data
                for item in world.trap_list:
                    trap_group.add(item)

            # show intro
            if start_intro:
                if intro_fade.fade(screen):
                    start_intro = False
                    intro_fade.fade_counter = 0

            # show death screen
            if not player.alive:
                if death_fade.fade(screen):
                    if restart_btn.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        lower_world_data, decor_world_data, upper_world_data = reset_level()

                        # load level data and create world
                        lower_world_data, decor_world_data, upper_world_data = load_level_layers_data()
                        world = World()
                        world.process_data(lower_world_data, decor_world_data, upper_world_data)
                        player = world.player
                        enemy_list = world.enemy_list
                        total_enemies = len(enemy_list)
                        score_gem = Item(SCREEN_WIDTH - 115, 23, 0, gem_images, True)
                        item_group.add(score_gem)
                        # add the items from the level data
                        for item in world.item_list:
                            item_group.add(item)

                        # add the a_tiles from the lower and decor layers level data
                        for item in world.a_decor_tiles_list:
                            a_decor_tiles_group.add(item)

                        # add the a_tiles from the upper layer level data
                        for item in world.a_upper_tiles_list:
                            a_upper_tiles_group.add(item)

                        # add the trap from the lower layer level data
                        for item in world.trap_list:
                            trap_group.add(item)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # music changer
        if STOPPED_PLAYING == event.type:
            # change track
            track += 1
            if track > max_track:
                track = 1
            pygame.mixer.music.load(path.join(mus_dir, f'Action {track}.wav'))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(fade_ms=5000)

        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pause_game = True

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.flip()

pygame.quit()
