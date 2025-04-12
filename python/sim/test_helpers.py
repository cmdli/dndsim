import sim.character


def sample_character():
    character = sim.character.Character()
    character.init(level=5, stats=[12, 12, 12, 12, 12, 12])
    return character
