import os
import random

from BASE_GAME_FILES.scripts.Utils import load_image, BASE_IMG_PATH
import BASE_GAME_FILES.scripts.PlanetArtGenerator as PAG
import BASE_GAME_FILES.scripts.Actor as A

asset_dict = {
}


def load_planets():
    PAG.Generate_Art(A.initial_art_generation['Planet'], A.initial_art_generation['Meteor'],
                     A.initial_art_generation['Star'], A.initial_art_generation['Black_Hole'])

    planet_assets = {
        'Planet': [load_image(i) for i in os.listdir(BASE_IMG_PATH) if
                   i.__contains__("spherized_planet_procedural_art")],
        'Meteor': [load_image(i) for i in os.listdir(BASE_IMG_PATH) if
                   i.__contains__("spherized_meteor_procedural_art")],
        'Star': [load_image(i) for i in os.listdir(BASE_IMG_PATH) if
                 i.__contains__("spherized_star_procedural_art")],
        'Black_Hole': [load_image(i) for i in os.listdir(BASE_IMG_PATH) if
                       i.__contains__("spherized_black_hole_procedural_art")]
    }

    asset_dict.update(planet_assets)


def rand_key(key: str):
    return asset_dict[key][random.randint(0, len(asset_dict[key]) - 1)]
