from os import path

import pygame

pygame.mixer.init()

# define path variables
res_dir = path.join(path.dirname(__file__), 'resources')
snd_dir = path.join(res_dir, 'sounds')

# load sounds
magic_snd = pygame.mixer.Sound(path.join(snd_dir, 'magic1.wav'))
magic_snd.set_volume(0.3)
shot_snd = pygame.mixer.Sound(path.join(snd_dir, 'arrow_shot.mp3'))
shot_snd.set_volume(0.6)
hit_snd = pygame.mixer.Sound(path.join(snd_dir, 'arrow_hit.wav'))
hit_snd.set_volume(0.6)
player_hit_snd = pygame.mixer.Sound(path.join(snd_dir, 'hit_1.wav'))
player_hit_snd.set_volume(0.2)
death_snd = pygame.mixer.Sound(path.join(snd_dir, 'Explosion11.wav'))
death_snd.set_volume(0.3)
gem_snd = pygame.mixer.Sound(path.join(snd_dir, 'pickup.wav'))
gem_snd.set_volume(0.4)
heal_snd = pygame.mixer.Sound(path.join(snd_dir, 'heal.wav'))
heal_snd.set_volume(0.3)
boost_snd = pygame.mixer.Sound(path.join(snd_dir, 'blessing.ogg'))

pickup_sounds = [gem_snd, heal_snd, boost_snd]
