import BASE_GAME_FILES.scripts.MenuSystems as M_SYS
from BASE_GAME_FILES.scripts.Utils import Colour


def i_am_clicked():
    print("I AM CLICKED")


#  ADD MENUS HERE

MissionFailedScreen = M_SYS.Menu([
    M_SYS.Image([0, 0], "GameArt/FAIL_SCREEN_HANDTRACKED.png", scale=0.33),

])

MissionSuccessScreen = M_SYS.Menu([
    M_SYS.Image([0, 0], "GameArt/SUCCESS_SCREEN_HANDTRACKED.png", scale=0.33),
])


TestMenu = M_SYS.Menu([
    M_SYS.Slider((200, 20), (0, 0), Colour(100, 100, 100), Colour(255, 255, 255), (0, 1000), 20),
    M_SYS.Toggle([50, 20], [0, 30], Colour(100, 100, 100), Colour(255, 255, 255))
])

Stars_Idle = M_SYS.Menu([
    M_SYS.Image([0, -25], "GameArt/Helper.png"),
    M_SYS.Image([0, -25], "GameArt/StarMan-Idle.png")
])

MaxAbilitiesPlanet = M_SYS.Menu([
    M_SYS.Text([650, 10], "Planet: ", 30, Colour(255, 255, 255)),
])

MaxAbilitiesStar = M_SYS.Menu([
    M_SYS.Text([650, 40], "Star: ", 30, Colour(255, 255, 255)),
])

MaxAbilitiesBlackHole = M_SYS.Menu([
    M_SYS.Text([650, 70], "Black Hole: ", 30, Colour(255, 255, 255)),
])

Stars_Talking_1 = M_SYS.Menu([
    M_SYS.Image([0, -25], "GameArt/Helper.png"),
    M_SYS.Image([0, -25], "GameArt/StarMan-Talking.png"),
])

DialogueBox = M_SYS.Menu([
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-12.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-11.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-10.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-9.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-8.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-7.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-6.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-5.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-4.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-3.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-2.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-1.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-13.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-18.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-24.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-16.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-14.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-23.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-21.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-19.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-22.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-15.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-20.png"),
    M_SYS.Image([30, -25], "GameArt/Dialogue/Dialogue_Box-17.png"),
])

ShowingRaptor_Idle = M_SYS.Menu([
    M_SYS.Image([0, -25], "GameArt/Helper.png"),
    M_SYS.Image([0, -25], "GameArt/Raptor-Idle.png")
])

ShowingRaptor_Talking = M_SYS.Menu([
    M_SYS.Image([0, -25], "GameArt/Helper.png"),
    M_SYS.Image([0, -25], "GameArt/Raptor-Talking.png")
])

ShowingBig_Idle = M_SYS.Menu([
    M_SYS.Image([0, -25], "GameArt/Helper.png"),
    M_SYS.Image([0, -25], "GameArt/Big-Idle.png")
])

ShowingBig_Talking = M_SYS.Menu([
    M_SYS.Image([0, -25], "GameArt/Helper.png"),
    M_SYS.Image([0, -25], "GameArt/Big-Talking.png")
])
