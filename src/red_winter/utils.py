import clipboard
from PyPDF2 import PdfReader
import pandas as pd

character_sheet_link = r"data\Solo_Crux.pdf"


def basic_skill_check(base_value, skill_name, modifiers=None):

    #TODO nab additional modifiers based on... conditions

    if modifiers == None:
        modifiers = []
    modifiers = "".join(modifiers)

    discord_command = f"!r 1d10+{str(base_value)}{modifiers} {skill_name}"
    clipboard.copy(discord_command)

def damage_roll(roll:str, weapon:str, modifiers=None):

    #TODO Handle things like a chain of mods +1-1-8

    if modifiers == None:
        modifiers = []
    modifiers = "".join(modifiers)

    discord_command = f"!r {roll+modifiers} Damage w/ {weapon}"
    clipboard.copy(discord_command)

def weapon_roll(weapon:str, modifiers=None):

    weapons_list = pd.read_csv(r"data\weapons.csv")

    for i in range(len(weapon)):
        weapons_list = weapons_list[ 
            weapons_list["name"].str.startswith(weapon[:i+1], na=False)
        ]
        #print(weapons_list)
        if len(weapons_list) <= 1:
            break

    if len(weapons_list) == 0:
        print(f"can't find {weapon}")
        return

    #MAP WEAPON TYPES TO SKILLS

    skills_for_weapons = {
        'Medium Pistol' : 'Handgun',
        'Heavy Pistol' : 'Handgun',
        'Very Heavy Pistol' : 'Handgun',
        'SMG' : 'Handgun',
        'Heavy SMG' : 'Handgun',
        'Shotgun': 'ShoulderArms',
        'Assault Rifle' : 'ShoulderArms',
        'Sniper Rifle' : 'ShoulderArms',
        'Bow' : 'Archery',
        'Grenade Launcher' : 'HeavyWeapons',
        'Rocket Launcher' 'HeavyWeapons'
        'Light Melee' : 'Melee',
        'Medium Melee' : 'Melee',
        'Heavy Melee' : 'Melee',
        'Very Heavy Melee' : 'Melee',
        'Thrown Weapon' : 'Melee',
        'Crossbow' : 'Archery'
    }

    skill_name = skills_for_weapons[weapons_list['type'].iloc[0]]
    character_sheet = PdfReader(character_sheet_link)
    fields = character_sheet.get_form_text_fields()

    base = fields[f"BASE {skill_name}"]

    #Modifier List
    if modifiers == None:
        modifiers = []
    if "(EQ)" in weapon: # Excellent Quality -> +1
        modifiers.append("+1")

    modifiers = "".join(modifiers)

    discord_command = f"!r 1d10+{base}{modifiers} Attack w/ {weapon}"
    clipboard.copy(discord_command)


def determine_stat_group(skill_name: str, df: pd.DataFrame) -> str:
    bucket = "UNK"
    if skill_name in list(df["SkillName"]):
        bucket = df.loc[df["SkillName"] == skill_name, "AlignedStat"].iloc[0]
        bucket = bucket.strip()
    else:
        pass
        print(f"{skill_name} was not found :()")
    return bucket