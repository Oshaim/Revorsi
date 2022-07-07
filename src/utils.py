import os
import pathlib
import arcade

def get_root_dir():
    return pathlib.Path(__file__).parent.parent

def load_resource(path):
    pass

def load_image(filename):
    return arcade.load_texture(os.path.join(get_root_dir(), f'resources/pictures/{filename}'))

    