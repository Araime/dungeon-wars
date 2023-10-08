from os import listdir, path

import pygame

from settings import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# helper function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))


# define path variables
res_dir = path.join(path.dirname(__file__), 'resources')
img_dir = path.join(res_dir, 'images')
char_dir = path.join(img_dir, 'characters')
tile_dir = path.join(img_dir, 'tiles')
btn_dir = path.join(img_dir, 'buttons')
lower_tile_dir = path.join(img_dir, 'tiles', 'lower')
decor_tile_dir = path.join(img_dir, 'tiles', 'decor')
upper_tile_dir = path.join(img_dir, 'tiles', 'upper')
animated_tiles_dir = path.join(img_dir, 'animated_tiles')

# load background for main menu
menu_img = pygame.image.load(path.join(img_dir, 'backgrounds', 'Dungeon-door-skull.png')).convert_alpha()
menu_img = pygame.transform.scale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# load button images
restart_img = scale_img(pygame.image.load(path.join(btn_dir, 'button_restart.png')).convert_alpha(), BUTTON_SCALE)
start_img = scale_img(pygame.image.load(path.join(btn_dir, 'button_start.png')).convert_alpha(), BUTTON_SCALE)
resume_img = scale_img(pygame.image.load(path.join(btn_dir, 'button_resume.png')).convert_alpha(), BUTTON_SCALE)
exit_img = scale_img(pygame.image.load(path.join(btn_dir, 'button_exit.png')).convert_alpha(), BUTTON_SCALE)

# load heart
heart_empty = scale_img(pygame.image.load(path.join(img_dir, 'items', 'heart_empty.png')).convert_alpha(), HEART_SCALE)
heart_half = scale_img(pygame.image.load(path.join(img_dir, 'items', 'heart_half.png')).convert_alpha(), HEART_SCALE)
heart_full = scale_img(pygame.image.load(path.join(img_dir, 'items', 'heart_full.png')).convert_alpha(), HEART_SCALE)

# load gem images
gem_images = []
for i in range(5):
    img = scale_img(pygame.image.load(path.join(img_dir, 'items', f'gem-{i}.png')).convert_alpha(), GEM_SCALE)
    gem_images.append(img)

# load cherry images
cherry_images = []
for i in range(7):
    img = scale_img(pygame.image.load(path.join(img_dir, 'items', f'cherry-{i}.png')).convert_alpha(), ITEM_SCALE)
    cherry_images.append(img)

# load crystal images
crystal_images = []
for i in range(7):
    img = scale_img(pygame.image.load(path.join(img_dir, 'items', f'crystal-{i}.png')).convert_alpha(), GEM_SCALE)
    crystal_images.append(img)

item_images = [gem_images, cherry_images, crystal_images]

# load weapon images
bow_img = scale_img(
    pygame.image.load(path.join(img_dir, 'weapons', 'bow.png')).convert_alpha(),
    WEAPON_SCALE
)
arrow_img = scale_img(
    pygame.image.load(path.join(img_dir, 'weapons', 'arrow.png')).convert_alpha(),
    WEAPON_SCALE
)
fireball_img = scale_img(
    pygame.image.load(path.join(img_dir, 'weapons', 'fireball.png')).convert_alpha(),
    FIREBALL_SCALE
)

# load character images
char_animations = []
char_types = [
    'player',
    'tiny_zombie',
    'goblin',
    'skeleton',
    'imp',
    'muddy',
    'big_demon',
    'zombie',
    'orc_warrior',
    'chest',
    'demon',
    'ogre'
]
animation_types = ['idle', 'run']
for char in char_types:
    # load images
    animation_list = []
    for animation in animation_types:
        # reset temporary list of images
        temp_list = []
        action_dir = path.join(char_dir, char, animation)
        for img in listdir(action_dir):
            char_img = pygame.image.load(path.join(action_dir, img)).convert_alpha()
            if char == 'player':
                char_img = scale_img(char_img, PLAYER_SCALE)
            else:
                char_img = scale_img(char_img, SCALE)
            temp_list.append(char_img)
        animation_list.append(temp_list)
    char_animations.append(animation_list)

# load death animation
death_animation = []
for i in range(6):
    img = scale_img(pygame.image.load(path.join(img_dir, 'effects', f'death-{i}.png')).convert_alpha(), ITEM_SCALE)
    death_animation.append(img)

# load fountains animations
# blue
blue_fountain_base = []
for i in range(3):
    img = pygame.image.load(path.join(animated_tiles_dir, f'fountain_base_{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    blue_fountain_base.append(img)

blue_fountain_mid = []
for i in range(3):
    img = pygame.image.load(path.join(animated_tiles_dir, f'fountain_mid_{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    blue_fountain_mid.append(img)


# red
red_fountain_base = []
for i in range(3):
    img = pygame.image.load(path.join(animated_tiles_dir, f'fountain_base_red_{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    red_fountain_base.append(img)

red_fountain_mid = []
for i in range(3):
    img = pygame.image.load(path.join(animated_tiles_dir, f'fountain_mid_red_{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    red_fountain_mid.append(img)

# load torch animation
torch_animation = []
for i in range(4):
    img = scale_img(pygame.image.load(path.join(animated_tiles_dir, f'torch_{i}.png')).convert_alpha(), WEAPON_SCALE)
    torch_animation.append(img)

# load trap animation
trap_animation = []
for i in range(4):
    img = pygame.image.load(path.join(img_dir, 'trap', f'{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    trap_animation.append(img)

# load candles images
# candle a
candle_a_animation = []
for i in range(4):
    img = scale_img(pygame.image.load(path.join(animated_tiles_dir, f'candleA_{i}.png')).convert_alpha(), WEAPON_SCALE)
    candle_a_animation.append(img)

# candle b
candle_b_animation = []
for i in range(4):
    img = scale_img(pygame.image.load(path.join(animated_tiles_dir, f'candleB_{i}.png')).convert_alpha(), WEAPON_SCALE)
    candle_b_animation.append(img)

# load water and waterfall images
# waterfall_a
waterfall_a_animation = []
for i in range(3):
    img = pygame.image.load(path.join(animated_tiles_dir, f'waterfall_a{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img.set_alpha(180)
    waterfall_a_animation.append(img)

# waterfall_b
waterfall_b_animation = []
for i in range(3):
    img = pygame.image.load(path.join(animated_tiles_dir, f'waterfall_b{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img.set_alpha(180)
    waterfall_b_animation.append(img)

# water_a
water_a_animation = []
for i in range(4):
    img = pygame.image.load(path.join(animated_tiles_dir, f'water_a{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img.set_alpha(200)
    water_a_animation.append(img)

# water_b
water_b_animation = []
for i in range(4):
    img = pygame.image.load(path.join(animated_tiles_dir, f'water_b{i}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img.set_alpha(200)
    water_b_animation.append(img)

# fly crystal
crystal_animation = []
for i in range(4):
    img = pygame.image.load(path.join(animated_tiles_dir, f'crystal_{i}.png')).convert_alpha()
    crystal_animation.append(img)

# fly rock
rock_animation = []
for i in range(4):
    img = pygame.image.load(path.join(animated_tiles_dir, f'rock_{i}.png')).convert_alpha()
    rock_animation.append(img)

# load tilemap layers images
lower_tile_list = []
decor_tile_list = []
upper_tile_list = []

# lower tilemap
for x in range(LOWER_TILE_TYPES):
    tile_image = pygame.image.load(path.join(lower_tile_dir, f'{x}.png')).convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
    lower_tile_list.append(tile_image)

# decor tilemap
for x in range(DECOR_TILE_TYPES):
    tile_image = pygame.image.load(path.join(decor_tile_dir, f'{x}.png')).convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
    decor_tile_list.append(tile_image)

# upper tilemap
for x in range(UPPER_TILE_TYPES):
    tile_image = pygame.image.load(path.join(upper_tile_dir, f'{x}.png')).convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
    upper_tile_list.append(tile_image)
