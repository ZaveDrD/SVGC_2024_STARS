import BASE_GAME_FILES.scripts.AbilitySystems as AbilitySystem


abilities = []


def initialise_abilities(game):
    ability_data = [
        AbilitySystem.Ability('Grab Planet', AbilitySystem.AbilityFunctions.GrabPlanetAbility, 'Pinch', game, 0, unlockLevel=3),
        AbilitySystem.Ability('Summon Planet Ability', AbilitySystem.AbilityFunctions.SummonPlanetAbility, 'Summon Planet', game, 1, unlockLevel=8),
        AbilitySystem.Ability('Move Ability', AbilitySystem.AbilityFunctions.MoveAbility, 'Point', game, 0, unlockLevel=2),
        AbilitySystem.Ability('Time Control Ability', AbilitySystem.AbilityFunctions.TimeControlAbility, 'Time Control', game, 0, unlockLevel=1),
        AbilitySystem.Ability('Zoom In Ability', AbilitySystem.AbilityFunctions.ZoomInAbility, 'Zoom In', game, 0, unlockLevel=2),
        AbilitySystem.Ability('Zoom Out Ability', AbilitySystem.AbilityFunctions.ZoomOutAbility, 'Zoom Out', game, 0, unlockLevel=2),
        AbilitySystem.Ability('Summon Star Ability', AbilitySystem.AbilityFunctions.SummonStarAbility, 'Summon Star', game, 1, unlockLevel=11),
        AbilitySystem.Ability('Summon Black Hole Ability', AbilitySystem.AbilityFunctions.SummonBlackHoleAbility, 'Summon Black Hole', game, 1, unlockLevel=13),
        AbilitySystem.Ability('Enlarge Ability', AbilitySystem.AbilityFunctions.EnlargeAbility, 'Enlarge', game, 0, unlockLevel=14),
        AbilitySystem.Ability('Shrink Ability', AbilitySystem.AbilityFunctions.ShrinkAbility, 'Shrink', game, 0, unlockLevel=17),
        AbilitySystem.Ability('Reset Ability', AbilitySystem.AbilityFunctions.ResetAbility, 'Reset', game, 0, unlockLevel=0),
    ]
    return ability_data
