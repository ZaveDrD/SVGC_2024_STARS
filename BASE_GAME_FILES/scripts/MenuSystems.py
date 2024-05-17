import math
import pygame

import BASE_GAME_FILES.scripts.Actor as A


#  Func:
#   -> Each 'Menu' consists of individual 'elements'
#   -> Elements include:
#       - Buttons
#       - Panels
#       - Text
#       - whatever else later on (ie. sliders, toggles, etc...)


class UI_Element:
    #  Requires:
    #   -> screen_pos (px) : list[float], len = 2
    #   -> color (RGB), list[int], len = 3    #
    #   -> opacity (0-255), int

    def __init__(self, pos: list[float], color: list[int], opacity: int = 255, outlineThickness: int = 0):
        self.x = pos[0]
        self.y = pos[1]
        self.opacity = opacity
        self.color = color
        self.outlineThickness = outlineThickness
        self.show = False
        self.button = False

    def display(self):
        pass

    def is_clicked(self) -> bool:
        pass


class Rect_Panel(UI_Element):
    def __init__(self, pos: list[float], size: list[float], color: list[int], opacity: int = 255,
                 outlineThickness: int = 0, roundness: list[int] = [1, 1, 1, 1]):
        super().__init__(pos, color, opacity, outlineThickness)
        self.width = size[0]
        self.height = size[1]
        self.roundness = roundness

        self.bounds = pygame.Rect(self.x, self.y, self.width, self.height)
        self.points = [[self.x, self.y], [self.x+self.width, self.y+self.height]]

    def display(self):
        if not self.show: pass
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
        print(f"{ x = }, { y = }, { inRect = }")
        return pygame.mouse.get_pressed()[0] and inRect


class Geometric_Panel(UI_Element):
    def __init__(self, points: list[list[int]], pos: list[float], color: list[int], opacity: int = 255,
                 outlineThickness: int = 0):
        super().__init__(pos, color, opacity, outlineThickness)
        self.points = points
        self.col = None

    def display(self):
        if not self.show: pass
        self.col = pygame.draw.polygon(A.game_specs.display, self.color, self.points, width=self.outlineThickness)

    def is_clicked(self) -> bool:
        return False  # IDK how to do this yet


class Circular_Panel(UI_Element):
    def __init__(self, radius: int, pos: list[float], color: list[int], opacity: int = 255, outlineThickness: int = 0,
                 corners: list[bool] = [True, True, True, True]):
        super().__init__(pos, color, opacity, outlineThickness)
        self.radius = radius
        self.corners = corners

    def display(self):
        if not self.show: pass
        pygame.draw.circle(A.game_specs.display, self.color, [self.x, self.y], self.radius, width=self.outlineThickness,
                           draw_top_left=self.corners[0], draw_top_right=self.corners[1],
                           draw_bottom_right=self.corners[2], draw_bottom_left=self.corners[3])

    def is_clicked(self) -> bool:
        x1, y1 = pygame.mouse.get_pos()
        x2, y2 = self.x, self.y
        dist = math.hypot(x1 - x2, y1 - y2)

        return pygame.mouse.get_pressed()[0] and dist <= self.radius


class Button:
    def __init__(self, function, buttonObj: UI_Element):
        self.pressed = False
        self.function = function
        self.buttonObj = buttonObj
        self.button = True

    def press(self):
        self.function()

    def checkForInputs(self):
        if self.buttonObj.is_clicked() and not self.pressed:
            print("PRESSED")
            self.press()
            self.pressed = pygame.mouse.get_pressed()[0]


class Rect_Button(Rect_Panel, Button):
    def __init__(self, size: list[float], pos: list[float], color: list[int], function):
        Rect_Panel.__init__(self, size, pos, color)
        Button.__init__(self, function, self)


class Geometric_Button(Geometric_Panel, Button):
    def __init__(self, points: list[list[int]], pos: list[float], color: list[int], function):
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
