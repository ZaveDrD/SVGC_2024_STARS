import BASE_GAME_FILES.scripts.MenuSystems as M_SYS


def i_am_clicked():
    print("I AM CLICKED")

#  ADD MENUS HERE


TestMenu = M_SYS.Menu([
    M_SYS.Rect_Button([25, 25], [100, 100], [255, 0, 0], i_am_clicked)
])
