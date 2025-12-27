from .modifier import Modifier

def damage_roll(app, roll:str, weapon:str, other_modifiers=None) -> None:
    """
    Docstring for damage_roll
    
    :param app: The application taht this will be associated with
    :param roll: The roll associated with the attack
    :param weapon: The thing the attack is being made with
    :param other_modifiers: Any modifiers that might be associated with the damage
    """

    other_modifiers = other_modifiers or [] # If None, empty list

    damage_modifier: Modifier = Modifier()
    for modifier in other_modifiers:
        damage_modifier += modifier

    magnitudes, reasons = damage_modifier.get_affect("Damage")

    if len(reasons) > 0:
        reasons = ' (' + reasons + ')'

    discord_command = f"!r {roll}{magnitudes} Damage w/ {weapon}{reasons}"

    app.update_clipboard(discord_command)