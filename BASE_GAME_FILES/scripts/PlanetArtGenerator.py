import os.path
import random
from PyNoise.noisemodule import *
from PyNoise.noiseutil import *
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from BASE_GAME_FILES.scripts.Utils import save_warped_img, BASE_IMG_PATH

# Planet Type :
#   Stars
#   Meteors
#   Planet
#   Black Hole

_width, _height = 256, 256  # px size of the square planet (non-warped)

object_color_palettes = {
    "Planet": [
        [Color(0, 0, 0.5), Color(0, .2, 0)],
        [Color(.4, 0, 0), Color(0, 0, .3)]
    ],
    "Meteor": [
        [Color(.45, .06, .06), Color(.4, .22, .05)],
        [Color(.4, .3, .16), Color(.4, .26, .13)]
    ],
    "Star": [
             [Color(1, .21, .09), Color(1, .65, .05), Color(1, .87, .07)],
             [Color(1, .7, .09), Color(1, .4, .1), Color(1, .23, .23)],
             [Color(1, .05, .05), Color(.5, 0, 0), Color(1, .7, .09)],
             [Color(0.53, 1.00, 0.97), Color(0.27, 1.00, 1.00), Color(0.18, 0.45, 1.00)],
             [Color(0.74, 0.22, 1.00), Color(.5, 0.19, 0.8), Color(0.38, 0.15, 1.00)],
             [None, None, None]
    ],
    "Black_Hole": [
        [Color(0, 0, 0), Color(.8, .5, .1)]
    ],
}


def render_obj(_render, filename, gradient, src):
    _map = noise_map_plane_gpu(_width, _height, lower_x=1, upper_x=6, lower_z=2, upper_z=6, source=src)
    _render.render(_width, _height, _map, filename, gradient)
    save_warped_img(filename, img_path=BASE_IMG_PATH)


def generate_rand_gradient(palette, color_change_interval: list[float] = [0, 0.1],
                           gradient_point_range: list[int] = [2, 5]):
    gradient = GradientColor()
    gradient.gradient_points.clear()

    numPointsPos, numPointsNeg = random.randint(min(gradient_point_range), max(gradient_point_range)), random.randint(
        min(gradient_point_range), max(gradient_point_range))

    palette = palette[random.randint(0, len(palette) - 1)]

    neg_current_color = palette[0]
    pos_current_color = palette[1]

    for i in range(numPointsNeg):
        neg_current_color = Color(
            neg_current_color.r + random.uniform(min(color_change_interval), max(color_change_interval)),
            neg_current_color.g + random.uniform(min(color_change_interval), max(color_change_interval)),
            neg_current_color.b + random.uniform(min(color_change_interval), max(color_change_interval)))

        gradient.add_gradient_point(-1 / (i + 1), neg_current_color)

    for i in range(numPointsPos):
        pos_current_color = Color(
            pos_current_color.r + random.uniform(min(color_change_interval), max(color_change_interval)),
            pos_current_color.g + random.uniform(min(color_change_interval), max(color_change_interval)),
            pos_current_color.b + random.uniform(min(color_change_interval), max(color_change_interval)))

        gradient.add_gradient_point(1 / (i + 1), pos_current_color)

    return gradient


def gen_circular_gradient(filename, colors: list[tuple[float, float, float]]):
    # define color map
    cmap = LinearSegmentedColormap.from_list("my_cmap", colors)

    # create color map
    X, Y = np.meshgrid(np.linspace(-1, 1, _width), np.linspace(-1, 1, _height))
    R = np.sqrt(X ** 2 + Y ** 2)

    # plot color map
    fig = plt.figure(figsize=(_width+75, _height+77), frameon=False, dpi=1)
    plt.pcolormesh(X, Y, R, cmap=cmap)
    plt.axis('off')
    plt.savefig(os.path.join(BASE_IMG_PATH, filename + ".png"), bbox_inches='tight', pad_inches=0)


def gen_planet(filename: str, octaves: list[int] = [3, 4], persistence: list[float] = [.2, .3],
               lacunarity: list[int] = [1, 2], frequency: list[int] = [1, 2]):
    octaves = random.randint(min(octaves), max(octaves))
    persistence = random.uniform(min(persistence), max(persistence))
    lacunarity = random.randint(min(lacunarity), max(lacunarity))
    frequency = random.randint(min(frequency), max(frequency))

    seed = random.randint(0, 2048)

    perlin = Perlin(frequency, lacunarity, octaves, persistence, seed)
    rmf = RidgedMulti(frequency, lacunarity, octaves=octaves, seed=seed)
    terrain_pick = Perlin(frequency=frequency, persistence=persistence)
    final = Select(source0=perlin, source1=rmf, source2=terrain_pick, edge_falloff=0.125)

    render = RenderImage(light_enabled=True, light_brightness=2, light_contrast=2, directory=BASE_IMG_PATH)
    gradient = generate_rand_gradient(object_color_palettes['Planet'])
    render_obj(render, filename + '.png', gradient, final)


def gen_meteor(filename: str, octaves: list[int] = [3, 4], persistence: list[float] = [.2, .3],
               lacunarity: list[int] = [1, 2], frequency: list[int] = [1, 2]):
    octaves = random.randint(min(octaves), max(octaves))
    persistence = random.uniform(min(persistence), max(persistence))
    lacunarity = random.randint(min(lacunarity), max(lacunarity))
    frequency = random.randint(min(frequency), max(frequency))

    seed = random.randint(0, 2048)

    voronoi = Voronoi(frequency=2, enable_distance=True, seed=seed, displacement=0)
    ridges = RidgedMulti(seed=seed, lacunarity=lacunarity, frequency=frequency, octaves=octaves)
    terrain_pick = Perlin(frequency=frequency, persistence=persistence)
    final = Select(source0=voronoi, source1=ridges, source2=terrain_pick, edge_falloff=0.05)

    render = RenderImage(light_enabled=True, light_brightness=2, light_contrast=2, directory=BASE_IMG_PATH)
    gradient = generate_rand_gradient(object_color_palettes['Meteor'])
    render_obj(render, filename + '.png', gradient, final)


def gen_black_hole(filename: str):
    colors = [(0, 0, 0), (0, 0, 0), (.8, .6, .1), (.8, .6, .1)]
    gen_circular_gradient(filename, colors)
    save_warped_img(filename + ".png", img_path=BASE_IMG_PATH)


def gen_clouds(filename: str, frequency: list[int] = [1, 2]):
    frequency = random.randint(min(frequency), max(frequency))
    seed = random.randint(0, 2048)

    billow = Billow(seed=seed, frequency=frequency, lacunarity=2)

    render = RenderImage(light_enabled=True, light_brightness=2, light_contrast=2, directory=BASE_IMG_PATH)
    gradient = grayscale_gradient()
    render_obj(render, filename + '.png', gradient, billow)


def gen_star(filename: str, octaves: list[int] = [6, 7], persistence: list[float] = [.2, .3],
             lacunarity: list[int] = [3, 5], frequency: list[int] = [3, 5]):
    octaves = random.randint(min(octaves), max(octaves))
    persistence = random.uniform(min(persistence), max(persistence))
    lacunarity = random.randint(min(lacunarity), max(lacunarity))
    frequency = random.randint(min(frequency), max(frequency))

    seed = random.randint(0, 2048)

    perlin = Perlin(frequency, lacunarity, octaves, persistence, seed)

    grad_points = object_color_palettes['Star'][random.randint(0, len(object_color_palettes['Star']) - 1)]

    if grad_points[0] is not None:
        gradient = GradientColor()
        gradient.gradient_points.clear()
        gradient.add_gradient_point(-1, grad_points[0])
        gradient.add_gradient_point(0, grad_points[1])
        gradient.add_gradient_point(1, grad_points[2])

        render = RenderImage(light_enabled=True, light_brightness=2, light_contrast=2, directory=BASE_IMG_PATH)
        render_obj(render, filename + '.png', gradient, perlin)
    else:
        gen_circular_gradient(filename, [(1., 1., 1.), (1., 1., 1.), (0.53, 1.00, 0.97), (0, 0, 0)])
        save_warped_img(filename + ".png", img_path=BASE_IMG_PATH)


def Generate_Art(num_planets: int, num_meteors: int, num_stars: int, num_black_holes: int):
    for i in range(num_planets):
        gen_planet('planet_procedural_art_' + str(i))

    for i in range(num_meteors):
        gen_meteor('meteor_procedural_art_' + str(i))

    for i in range(num_stars):
        gen_star('star_procedural_art_' + str(i))

    for i in range(num_black_holes):
        gen_black_hole('black_hole_procedural_art_' + str(i))

