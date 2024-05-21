import math
import pygame
from BASE_GAME_FILES.scripts.Utils import Colour
import BASE_GAME_FILES.scripts.Actor as A
from typing import Callable


#  Func:
#   -> Each 'Menu' consists of individual 'elements'
#   -> Elements include:
#       - Buttons
#       - Panels
#       - Text
#       - whatever else later on (ie. sliders, toggles, etc...)


class UI_Element:
    button = False

    #  Requires:
    #   -> screen_pos (px) : list[float], len = 2
    #   -> color (RGB), list[int], len = 3    #
    #   -> opacity (0-255), int

    def __init__(self, pos: list[float], color: Colour, opacity: int = 255, outlineThickness: int = 0):
        self.x = pos[0]
        self.y = pos[1]
        self.opacity = opacity
        self.color = color
        self.outlineThickness = outlineThickness
        self.show = False

    def display(self):
        pass

    def is_clicked(self) -> bool:
        pass


class Rect_Panel(UI_Element):
    def __init__(self, pos: list[float], size: list[float], color: Colour, opacity: int = 255,
                 outlineThickness: int = 0, roundness: list[int] = [1, 1, 1, 1]):
        super().__init__(pos, color, opacity, outlineThickness)
        self.width = size[0]
        self.height = size[1]
        self.roundness = roundness

        self.bounds = pygame.Rect(self.x, self.y, self.width, self.height)
        self.points = [[self.x, self.y], [self.x+self.width, self.y+self.height]]

    def display(self):
        if not self.show: return
        self.bounds = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(A.game_specs.display, self.color,
                         self.bounds, width=self.outlineThickness,
                         border_top_left_radius=self.roundness[0], border_top_right_radius=self.roundness[1],
                         border_bottom_right_radius=self.roundness[2],
                         border_bottom_left_radius=self.roundness[3])

    def is_clicked(self) -> bool:
        x, y = A.mouse.get_pos()
        inRect = False
        if self.points[0][0] <= x <= self.points[1][0] and self.points[0][1] <= y <= self.points[1][1]:
            inRect = True
        #print(f"{ x = }, { y = }, { inRect = }")
        return pygame.mouse.get_pressed()[0] and inRect


class Geometric_Panel(UI_Element):
    def __init__(self, points: list[list[int]], pos: list[float], color: Colour, opacity: int = 255,
                 outlineThickness: int = 0):
        super().__init__(pos, color, opacity, outlineThickness)
        self.points = points
        self.col = None

    def display(self):
        if not self.show: return
        self.col = pygame.draw.polygon(A.game_specs.display, self.color, self.points, width=self.outlineThickness)

    def is_clicked(self) -> bool:
        return False  # IDK how to do this yet


class Circular_Panel(UI_Element):
    def __init__(self, radius: int, pos: list[float], color: Colour, opacity: int = 255, outlineThickness: int = 0,
                 corners: list[bool] = [True, True, True, True]):
        UI_Element.__init__(self, pos, color, opacity, outlineThickness)
        self.radius = radius
        self.corners = corners

    def display(self):
        if not self.show: return
        pygame.draw.circle(A.game_specs.display, self.color, [self.x, self.y], self.radius, width=self.outlineThickness,
                           draw_top_left=self.corners[0], draw_top_right=self.corners[1],
                           draw_bottom_right=self.corners[2], draw_bottom_left=self.corners[3])


    def is_clicked(self) -> bool:
        print("IS CLICKED :)")
        x1, y1 = pygame.mouse.get_pos()
        x2, y2 = self.x, self.y
        dist = math.hypot(x1 - x2, y1 - y2)

        return pygame.mouse.get_pressed()[0] and dist <= self.radius


class Button:
    button = True

    def __init__(self, function: Callable[[], None], buttonObj: UI_Element, needPressed=True, *args):
        self.pressed = False
        self.needPressed = needPressed
        self.function = function
        self.buttonObj = buttonObj

    def press(self):
        self.function()

    def checkForInputs(self):
        if self.buttonObj.is_clicked() and not (self.needPressed and self.pressed):
            self.press()
        self.pressed = pygame.mouse.get_pressed()[0]


class Rect_Button(Rect_Panel, Button):
    def __init__(self, size: list[float], pos: list[float], color: Colour, function: Callable[[], None], *args, **kwargs):
        Rect_Panel.__init__(self, pos, size, color, *args, **kwargs)
        Button.__init__(self, function, self)


class Circular_Button(Circular_Panel, Button):
    def __init__(self, size, pos, color, function: Callable[[], None], *args, **kwargs):
        Circular_Panel.__init__(self, size, pos, color, *args, **kwargs)
        Button.__init__(self, function, self)


class Toggle(UI_Element):
    button = True

    def __init__(self, size: list[float], pos: list[float], toggleColour: Colour, bgColour: Colour,
                 default: bool = True, function: Callable[[], None] | None = None):
        """
        A toggle widget to get boolean input
        Args:
            size: (int, int) The size of the widget (x, y)
            pos: (int, int) The coordinate of the widget (x, y)
            toggleColour: (Colour, Colour) The colour of the toggle circle. The first element applies
                                            when the toggle is on, the second is when it is off
            bgColour: (Colour, Colour) The colour of the rectangle containing the widget. The first
                                        element applies when the toggle is on, the second when it is
                                        off
            default: (bool) Whether the toggle is selected at the start
            function: (Function) A function to run when the widget is clicked [optional]
        """

        super().__init__(pos, bgColour)
        self.size = size
        self.show = True
        self.pressed = False
        self.toggleColour = toggleColour
        self.bgColour = self.color

        self.__rect = Rect_Button(size, pos, toggleColour, function=self.clicked, roundness=[30, 30, 30, 30])
        self.__circle = Circular_Button(size[1]//3, (self.x+self.size[0]-self.size[0]//4, self.y+self.size[1]-self.size[1]//2), bgColour,
                                      function=self.clicked)
        self.isSet = default
        self.__rect.show = True
        self.__circle.show = True
        self.function = function or (lambda: None)
        self.buttonObj = self.__rect.buttonObj

    def clicked(self):
        self.isSet = not self.isSet
        posIfNotSet = (self.x+self.size[0]//4, self.y+self.size[1]//2)
        posIfSet = (self.x+self.size[0]-self.size[0]//4, self.y+self.size[1]-self.size[1]//2)

        if self.isSet:
            self.__circle.x = posIfSet[0]
            self.__circle.y = posIfSet[1]
        else:
            self.__circle.x = posIfNotSet[0]
            self.__circle.y = posIfNotSet[1]

        self.function()

    def display(self):
        if not self.show: return
        self.__circle.color = self.toggleColour[self.isSet]
        self.__rect.color = self.bgColour[self.isSet]
        self.__rect.display()
        self.__circle.display()

    def checkForInputs(self):
        return self.__rect.checkForInputs()


class Text(UI_Element):
    button = False
    def __init__(self, pos: tuple[int], text: str, size: int = 12, colour: Colour | None = None, font: str = "Arial", *,
                 bold: bool = False, italic: bool = False, position: str = "top-left"):
        self.text = text
        self.colour = colour or Colour((0, 0, 0))
        self.bold = bold
        self.italic = italic
        self.pos = pos
        self.size = size
        self.position = position
        self.font = font


    def display(self):
        surfaces = []
        totalHeight = 0
        maxWidth = 0
        font = A.pygame.font.SysFont(self.font, self.size, self.bold, self.italic)
        for line in self.text.split('\n'):
            textSurface = font.render(line, True, self.colour)
            surfaces.append(textSurface)
            totalHeight += textSurface.get_height()
            maxWidth = max(maxWidth, textSurface.get_width())
        combinedSurface = A.pygame.Surface((maxWidth, totalHeight), A.pygame.SRCALPHA)
        yOffset = 0
        for surface in surfaces:
            combinedSurface.blit(surface, (0, yOffset))
            yOffset += surface.get_height()

        textRect = combinedSurface.get_rect()

        if self.position == 'top-left':
            textRect.topleft = self.pos
        elif self.position == 'top-right':
            textRect.topright = self.pos
        elif self.position == 'center':
            textRect.center = self.pos
        elif self.position == 'mid-top':
            textRect.midtop = self.pos
        elif self.position == 'bottom-left':
            textRect.bottomleft = self.pos
        elif self.position == 'bottom-right':
            textRect.bottomright = self.pos
        elif self.position == 'mid-bottom':
            textRect.midbottom = self.pos
        elif self.position == 'mid-left':
            textRect.midleft = self.pos
        elif self.position == 'mid-right':
            textRect.midright = self.pos

        A.game_specs.display.blit(combinedSurface, textRect)


class Slider(UI_Element):
    button = True

    def __init__(self, size: tuple[int, int], pos: tuple[int, int], colour: Colour,
                 bgColour: Colour, range_: tuple[int, int], default: float, **textOptions) -> None:
        super().__init__(pos, colour)
        self.value = default
        self.__range = range_
        self.__sizeX = size[0]
        self.__xStart = pos[0]
        self.pos = pos
        self.size = size

        self.container = Rect_Button(self.size, pos, bgColour, self.updateX, roundness=[5, 5, 5, 5])
        self.min = Text((pos[0] + 5, pos[1]), str(range_[0]), min(size)//2, colour, **textOptions)
        self.max = Text((pos[0]+size[0]-min(size) - 5, pos[1]), str(range_[1]), min(size)//2, colour, **textOptions)
        self.slider = Rect_Button((min(size)*0.8, min(size)*1.1), (self.__posX(), pos[1]-1), self.color, self.updateX, roundness=[5, 5, 5, 5])

        self.container.needPressed = self.slider.needPressed = False

    def __posX(self):
        # Normalise the slider to the size of the container
        ratio = self.value / abs(self.__range[1] - self.__range[0])
        xCoord = ratio * self.__sizeX + self.__xStart
        return xCoord

    def display(self):
        if not self.show: return
        self.container.show = self.min.show = self.max.show = self.slider.show = True
        self.container.display()
        self.min.display()
        self.max.display()
        self.slider.x = self.__posX()
        self.slider.display()

    def updateX(self):
        mouseCoord = A.mouse.get_pos()
        # Confirm the mouse is within the rectangle
        print(self.size[0])
        if not (self.pos[0] + self.slider.width / 2 <= mouseCoord[0] <= self.pos[0] + self.size[0] - self.slider.width / 2):
            # Is not within the x-range of the container
            return
        elif not (self.pos[1] + self.size[1] > mouseCoord[1] > self.pos[1]):
            # Is not within the y-range of the container
            return
        # Find the coordinate within the rectangle, then normalise to the range
        x = mouseCoord[0] - self.__xStart - self.slider.width / 2
        self.value = (x/self.__sizeX) * abs(self.__range[1] - self.__range[0]) + min(self.__range)

    def checkForInputs(self):
        self.container.checkForInputs()
        self.slider.checkForInputs()


class Geometric_Button(Geometric_Panel, Button):
    def __init__(self, points: list[list[int]], pos: list[float], color: Colour, function):
        Geometric_Panel.__init__(self, points, pos, color)
        Button.__init__(self, function, self)


class Menu:
    def __init__(self, elements: list[UI_Element]):
        self.elements = elements

    def open_menu(self):
        for UI in self.elements:
            UI.show = True

    def close_menu(self):
        for UI in self.elements:
            UI.show = False

    def updateMenu(self):
        for UI in self.elements:
            UI.display()
            if UI.button:
                UI.checkForInputs()
