from __future__ import annotations
import pygame
import BASE_GAME_FILES.scripts.Actor as A

BASE_IMG_PATH = ""


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey(A.COLOUR_KEY)
    return img


def ConvToPixelScale(sim_scale: int) -> int:
    return sim_scale / (A.SIM_SCALE / A.player_zoom)


def ConvToSimScale(px_scale: int) -> int:
    return px_scale * (A.SIM_SCALE / A.player_zoom)


def ScaleCoordinateToScreenSize(px: list[float]) -> tuple:
    ratioX = A.game_specs.display.get_size()[0] / A.game_specs.screen.get_size()[0]
    ratioY = A.game_specs.display.get_size()[1] / A.game_specs.screen.get_size()[1]
    return px[0] * ratioX, px[1] * ratioY


class Colour(tuple):
    def __init__(self, colour: str | tuple[int, int, int]):
        """
        An implementation of Colour allowing RGB and Hex
        Args:
            colour: (str | tuple) The colour to use, either in rgb form as an iterable or hex form
                                    as a string
        """
        self.__colour: str | None = None
        self.set(colour)
        print(f"{colour = }, {self.hex = }, {self[2] = }")

    def set(self, colour: str | tuple[int, int, int]) -> None:
        """
        Sets the value of the colour
        Args:
            colour: (str | tuple) The colour to use, either in rgb form as an iterable or hex form
                                    as a string
        Returns: Nothing
        """
        if isinstance(colour, str):
            if colour[0] == '#' and len(colour) == 7 and colour[1:].isdigit():
                self.__colour = colour
            else:
                colours = {
                    'white': '#ffffff',
                    'black': '#000000',
                    'red': '#ff0000',
                    'green': '#00ff00',
                    'blue': '#0000ff',
                    'yellow': '#ffff00',
                    'aqua': '#00ffff',
                    'purple': '#ff00ff',
                }
                if colour.lower() in colours:
                    self.__colour = colours[colour]
                else:
                    raise ValueError(f"Invalid Colour, \"{colour}\"")
        elif isinstance(colour, list) or isinstance(colour, tuple):
            print("ARRAY")
            self.__colour = self.rgbToHex(colour)

    def grayScale(self) -> Colour:
        """
        Converts the colour to grayscale
        Returns: (Colour) The converted colour

        """
        brightness = sum(self.rgb) // 3
        return Colour((brightness,)*3)

    @staticmethod
    def rgbToHex(rgb: tuple[int]) -> str:
        """
        Converts a colour from RGB form to hex form
        Args:
            rgb: (int, int, int) The colour in RGB form
        Returns: (str) The colour in hex

        """
        red = hex(rgb[0]).replace('x', '')
        if len(red) == 1:
            red = '0' + red
        elif len(red) == 3:
            red = red[1:]
        green = hex(rgb[1]).replace('x', '')
        if len(green) == 1:
            green = '0' + green
        elif len(green) == 3:
            green = green[1:]
        blue = hex(rgb[2]).replace('x', '')
        if len(blue) == 1:
            print(blue, len(blue))
            blue = '0' + blue
        elif len(blue) == 3:
            blue = blue[1:]
        return '#' + red + green + blue

    @staticmethod
    def hexToRgb(hex: str) -> tuple[int, int, int]:
        """
        Converts a colour from hex to RGB
        Args:
            hex: (str) The colour in hex
        Returns: (int, int, int) The colour in RGB form

        """
        red = int(hex[1:3], 16)
        green = int(hex[3:5], 16)
        blue = int(hex[5:7], 16)

        return (red, green, blue)

    @property
    def red(self) -> int:
        return int(self.__colour[1:3], 16)

    @property
    def green(self) -> int:
        return int(self.__colour[3:5], 16)

    @property
    def blue(self) -> int:
        return int(self.__colour[5:7], 16)

    @property
    def hex(self) -> str:
        """The colour in hex"""
        return self.__colour

    @property
    def rgb(self) -> tuple[int, int, int]:
        """The colour in RGB"""
        return self.hexToRgb(self.__colour)

    def __getitem__(self, item) -> int:
        return self.rgb[item]

    def __setitem__(self, key: int, value: int) -> None:
        rgb: list[int, int, int] = list(self.rgb)
        rgb[key] = value
        self.__colour = self.rgbToHex(tuple(rgb))

    def __str__(self) -> str:
        return self.hex
