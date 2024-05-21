import BASE_GAME_FILES.scripts.MenuSystems as M_SYS
from BASE_GAME_FILES.scripts.Utils import Colour
import BASE_GAME_FILES.scripts.Actor as A


def i_am_clicked():
    print("I AM CLICKED")

#  ADD MENUS HERE
TestMenu = M_SYS.Menu([
    M_SYS.Slider((100, 20), (200, 200), Colour('#ffffff'), Colour("#990099"), [0, 100], 20)
])
