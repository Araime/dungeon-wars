from animated_tile import AnimatedTile
from character import Character
from enemy import Enemy
from settings import TILE_SIZE, ROWS, COLS
from images import (
    decor_tile_list,
    lower_tile_list,
    upper_tile_list,
    item_images,
    blue_fountain_base,
    red_fountain_base,
    torch_animation,
    blue_fountain_mid,
    red_fountain_mid,
    candle_a_animation,
    candle_b_animation,
    waterfall_a_animation,
    waterfall_b_animation,
    water_a_animation,
    water_b_animation,
    rock_animation,
    crystal_animation
)
from items import Item
from trap import Trap


class World:

    def __init__(self):
        self.lower_layer_map_tiles = []
        self.decor_layer_map_tiles = []
        self.upper_layer_map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.enemy_list = []
        self.trap_list = []
        self.a_decor_tiles_list = []
        self.a_upper_tiles_list = []

    def process_data(self, lower_layer_data, decor_layer_data, upper_layer_data):
        self.level_length = len(lower_layer_data)

        # create matrix
        matrix = []
        for row in range(ROWS):
            r = [-1] * COLS
            matrix.append(r)

        # create collision matrix
        for y, row in enumerate(lower_layer_data):
            for x, tile in enumerate(row):
                if -1 <= tile <= 7:
                    matrix[y][x] = 1
                elif 50 <= tile <= 66:
                    matrix[y][x] = 1
                else:
                    matrix[y][x] = 0

        # iterate through each value in lower layer level data file
        for y, row in enumerate(lower_layer_data):
            for x, tile in enumerate(row):
                image = lower_tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                if 8 <= tile <= 46:
                    self.obstacle_tiles.append(tile_data)
                elif tile == 47:
                    a_tile = AnimatedTile(image_x, image_y, blue_fountain_base, 130)
                    self.a_decor_tiles_list.append(a_tile)
                    self.obstacle_tiles.append(tile_data)
                elif tile == 48:
                    a_tile = AnimatedTile(image_x, image_y, red_fountain_base, 130)
                    self.a_decor_tiles_list.append(a_tile)
                    self.obstacle_tiles.append(tile_data)
                elif tile == 49:
                    self.exit_tile = tile_data
                elif tile == 50:
                    trap = Trap(image_x, image_y)
                    self.trap_list.append(trap)
                elif tile == 51:
                    gem = Item(image_x, image_y, 0, item_images[0])
                    self.item_list.append(gem)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 52:
                    cherry = Item(image_x, image_y, 1, item_images[1])
                    self.item_list.append(cherry)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 53:
                    crystal = Item(image_x, image_y, 2, item_images[2])
                    self.item_list.append(crystal)
                    tile_data[0] = lower_tile_list[0]
                # create player
                elif tile == 54:
                    player = Character(image_x, image_y, 100, 10, 0)
                    self.player = player
                    tile_data[0] = lower_tile_list[0]
                elif tile == 55:
                    enemy = Enemy(image_x, image_y, 80, 5, 1, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 56:
                    enemy = Enemy(image_x, image_y, 100, 6, 2, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 57:
                    enemy = Enemy(image_x, image_y, 130, 7, 3, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 58:
                    enemy = Enemy(image_x, image_y, 150, 10, 4, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 59:
                    enemy = Enemy(image_x, image_y, 200, 9, 5, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 60:
                    enemy = Enemy(image_x, image_y, 600, 15, 6, True)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 61:
                    trap = Trap(image_x, image_y, True)
                    self.trap_list.append(trap)
                elif tile == 62:
                    enemy = Enemy(image_x, image_y, 120, 7, 7, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 63:
                    enemy = Enemy(image_x, image_y, 150, 8, 8, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 64:
                    enemy = Enemy(image_x, image_y, 200, 10, 9, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 65:
                    enemy = Enemy(image_x, image_y, 250, 14, 10, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]
                elif tile == 66:
                    enemy = Enemy(image_x, image_y, 1000, 20, 11, False)
                    self.enemy_list.append(enemy)
                    tile_data[0] = lower_tile_list[0]

                # add image data in lower tiles list
                if tile >= 0:
                    if tile != 50 and tile != 61:
                        self.lower_layer_map_tiles.append(tile_data)

        # iterate through each value in decor layer level data file
        for y, row in enumerate(decor_layer_data):
            for x, tile in enumerate(row):
                image = decor_tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                if tile == 0:
                    a_tile = AnimatedTile(image_x, image_y, torch_animation, 100)
                    self.a_decor_tiles_list.append(a_tile)
                if tile == 3:
                    a_tile = AnimatedTile(image_x, image_y, candle_a_animation, 100)
                    self.a_decor_tiles_list.append(a_tile)
                if tile == 4:
                    a_tile = AnimatedTile(image_x, image_y, candle_b_animation, 100)
                    self.a_decor_tiles_list.append(a_tile)
                if tile == 5:
                    a_tile = AnimatedTile(image_x, image_y, waterfall_a_animation, 130)
                    self.a_decor_tiles_list.append(a_tile)
                if tile == 6:
                    a_tile = AnimatedTile(image_x, image_y, waterfall_b_animation, 130)
                    self.a_decor_tiles_list.append(a_tile)
                if tile == 7:
                    a_tile = AnimatedTile(image_x, image_y, water_a_animation, 150)
                    self.a_decor_tiles_list.append(a_tile)
                if tile == 8:
                    a_tile = AnimatedTile(image_x, image_y, water_b_animation, 150)
                    self.a_decor_tiles_list.append(a_tile)
                if tile == 9:
                    a_tile = AnimatedTile(image_x, image_y, crystal_animation, 150)
                    self.a_decor_tiles_list.append(a_tile)
                if tile == 10:
                    a_tile = AnimatedTile(image_x, image_y, rock_animation, 150)
                    self.a_decor_tiles_list.append(a_tile)

                # add image data in decor tiles list
                if tile == 1 or tile == 2:
                    self.decor_layer_map_tiles.append(tile_data)

        # iterate through each value in upper layer level data file
        for y, row in enumerate(upper_layer_data):
            for x, tile in enumerate(row):
                image = upper_tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                if tile == 0:
                    a_tile = AnimatedTile(image_x, image_y, blue_fountain_mid, 130)
                    self.a_upper_tiles_list.append(a_tile)
                elif tile == 1:
                    a_tile = AnimatedTile(image_x, image_y, red_fountain_mid, 130)
                    self.a_upper_tiles_list.append(a_tile)
                if tile == 4:
                    a_tile = AnimatedTile(image_x, image_y, waterfall_a_animation, 130)
                    self.a_upper_tiles_list.append(a_tile)
                if tile == 5:
                    a_tile = AnimatedTile(image_x, image_y, waterfall_b_animation, 130)
                    self.a_upper_tiles_list.append(a_tile)

                # add image data in upper tiles list
                if tile >= 2:
                    if tile != 4 and tile != 5:
                        self.upper_layer_map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.lower_layer_map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

        for tile in self.decor_layer_map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def update_upper(self, screen_scroll):
        for tile in self.upper_layer_map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.lower_layer_map_tiles:
            surface.blit(tile[0], tile[1])

        for tile in self.decor_layer_map_tiles:
            surface.blit(tile[0], tile[1])

    def draw_upper(self, surface):
        for tile in self.upper_layer_map_tiles:
            surface.blit(tile[0], tile[1])
