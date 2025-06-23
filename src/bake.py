from PIL import Image
import pygame

from src.elements.Entity import TILESIZE

WIDTH = 4000
HEIGHT = 4000

ZOOM = 0.4

images_cached = {}
levels_cached = {}

def image_cached(image_path, size):
    global images_cached

    try:
        return [images_cached[image_path + "#" + size], True]
    except:
        try:
            return [images_cached[image_path], False]
        except:
            return [False, False]

def level_cached(level):
    global levels_cached

    try:
        return levels_cached[level]
    except:
        return False

def bake_textures(level_data, level_name):
    global images_cached
    global levels_cached

    level = level_cached(level_name)
    if level:
        return level

    images = []
    for entity in level_data:
        if entity.anchored:
            if entity.sprite_name:
                image_size_x = int(entity.size.getX() * TILESIZE)
                image_size_y = int(entity.size.getY() * TILESIZE)
                cached_image = image_cached(entity.sprite_name, str(image_size_x) + "x" + str(image_size_y))
                if not cached_image[0]:
                    img = Image.open(entity.sprite_name).convert("RGBA")
                    images_cached[entity.sprite_name] = img
                else:
                    img = cached_image[0]
                if image_size_x == 0 or image_size_y == 0 or image_size_x < 0 or image_size_y < 0: continue
                if not cached_image[1]:
                    img = img.resize((int(image_size_x * ZOOM), int(image_size_y * ZOOM)), resample=Image.NEAREST)
                    images_cached[entity.sprite_name + "#" + str(image_size_x) + "x" + str(image_size_y)] = img
                images.append((img, entity.position.getX(), entity.position.getY() + entity.size.getY()))

    baked_image = Image.new('RGBA', (WIDTH, HEIGHT))

    for img in images:
        baked_image.alpha_composite(img[0], (int(img[1] * TILESIZE * ZOOM + WIDTH / 4), HEIGHT - int(img[2] * TILESIZE * ZOOM) - int(HEIGHT / 2)))

    #baked_image.show()

    mode = baked_image.mode
    size = baked_image.size
    data = baked_image.tobytes()

    surface = pygame.image.fromstring(data, size, mode).convert_alpha()

    levels_cached[level_name] = surface
    return surface
