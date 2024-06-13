import random
from pynoise.noisemodule import *
from pynoise.noiseutil import *

from BASE_GAME_FILES.scripts.Utils import save_warped_img

# Planet Type :
#   Stars
#   Meteors
#   Planet
#   Black Hole

_width, _height = 256, 256  # px size of the square planet (non-warped)
render = RenderImage(light_enabled=True, light_brightness=2, light_contrast=3)


def render_planet(render, filename, gradient, src):
    map = noise_map_plane_gpu(_width, _height, lower_x=1, upper_x=6, lower_z=2, upper_z=6, source=src)
    render.render(_width, _height, map, filename, gradient)
    save_warped_img(filename)


def generate_rand_gradient(init_color_max: float = .5, color_change_interval: float = 0.1, gradient_point_range: list[int] = [2, 5], starting_color: Color = None):
    gradient = GradientColor()
    numPointsPos, numPointsNeg = random.randint(min(gradient_point_range), max(gradient_point_range)), random.randint(min(gradient_point_range), max(gradient_point_range))

    if starting_color is not None:
        current_color = starting_color
    else:
        current_color = Color(random.uniform(0, init_color_max), random.uniform(0, init_color_max),
                          random.uniform(0, init_color_max))

    for i in range(numPointsNeg):
        gradient.add_gradient_point(-1 / (i + 1), Color(np.clip(current_color.r + random.uniform(-color_change_interval, color_change_interval), 0, 1),
                                                        np.clip(current_color.g + random.uniform(-color_change_interval, color_change_interval), 0, 1),
                                                        np.clip(current_color.b + random.uniform(-color_change_interval, color_change_interval), 0, 1)))

    if starting_color is None:
        current_color = Color(random.uniform(0, init_color_max), random.uniform(0, init_color_max),
                          random.uniform(0, init_color_max))

    for i in range(numPointsPos):
        gradient.add_gradient_point(1 / (i + 1), Color(np.clip(current_color.r + random.uniform(-color_change_interval, color_change_interval), 0, 1),
                                                       np.clip(current_color.g + random.uniform(-color_change_interval, color_change_interval), 0, 1),
                                                       np.clip(current_color.b + random.uniform(-color_change_interval, color_change_interval), 0, 1)))

    return gradient


def gen_planet(filename: str, octaves: list[int] = [3, 4], persistence: list[float] = [.2, .3], lacunarity: list[int] = [1, 2], frequency: list[int] = [1, 2]):
    octaves = random.randint(min(octaves), max(octaves))
    persistence = random.uniform(min(persistence), max(persistence))
    lacunarity = random.randint(min(lacunarity), max(lacunarity))
    frequency = random.randint(min(frequency), max(frequency))

    seed = random.randint(0, 2048)

    perlin = Perlin(frequency, lacunarity, octaves, persistence, seed)
    rmf = RidgedMulti(frequency, lacunarity, octaves=octaves, seed=seed)
    terrain_pick = Perlin(frequency=frequency, persistence=persistence)
    final = Select(source0=perlin, source1=rmf, source2=terrain_pick, edge_falloff=0.125)

    gradient = generate_rand_gradient(starting_color=Color(0, 0, .1))
    render_planet(render, filename+'.png', gradient, final)


def gen_clouds(filename: str, frequency: list[int] = [1, 2]):
    frequency = random.randint(min(frequency), max(frequency))
    seed = random.randint(0, 2048)

    billow = Billow(seed=seed, frequency=frequency, lacunarity=2)

    gradient = grayscale_gradient()
    render_planet(render, filename+'.png', gradient, billow)

gen_planet("blue_planet_test")
