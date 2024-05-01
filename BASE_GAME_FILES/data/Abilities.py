import BASE_GAME_FILES.scripts.AbilitySystems as AbilitySystem

abilities = []


def initialise_abilities(game):
    ability_data = [
        AbilitySystem.Ability('Grab Planet', AbilitySystem.AbilityFunctions.GrabPlanetAbility, 'Pinch', game, 0, unlockLevel=0),
        AbilitySystem.Ability('Summon Small Planet', AbilitySystem.AbilityFunctions.SummonPlanetAbility, 'Summon Small Planet', game, 2, unlockLevel=0)
    ]
    return ability_data
