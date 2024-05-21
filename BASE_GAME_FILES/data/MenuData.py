import BASE_GAME_FILES.scripts.MenuSystems as M_SYS
from BASE_GAME_FILES.scripts.Utils import Colour
import BASE_GAME_FILES.scripts.Actor as A


def i_am_clicked():
    print("I AM CLICKED")

#  ADD MENUS HERE

TestMenu = M_SYS.Menu([
    M_SYS.Toggle([200, 20], [200, 200], Colour(100, 100, 100), Colour(255, 255, 255))
    # M_SYS.Slider((200, 20), (200, 200), Colour(100, 100, 100), Colour(255, 255, 255), [0, 1000], 20)
])
