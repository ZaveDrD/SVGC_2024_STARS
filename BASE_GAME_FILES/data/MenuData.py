import BASE_GAME_FILES.scripts.MenuSystems as M_SYS
from BASE_GAME_FILES.scripts.Utils import Colour


def i_am_clicked():
    print("I AM CLICKED")

#  ADD MENUS HERE


TestMenu = M_SYS.Menu([
    M_SYS.Toggle([100, 50], [200, 200], (Colour((255, 0, 0)), Colour((0, 255, 0))), (Colour((0, 0, 255)), Colour((0, 0, 255))), True),
])
