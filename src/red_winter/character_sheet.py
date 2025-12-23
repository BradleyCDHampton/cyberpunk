
from PyPDF2 import PdfReader
from collections import defaultdict
import re
import pandas as pd

maps = { "DLV" : "Drive Land Vehicle",
             "PAV" : "Pilot Air Vehicle",
             "PSV" : "Pilot Sea Vehicle",
             "RTD" : "Resist Torture/Drugs",
             "PhotoFilm" : "Photography/Film",
             "PDSculpt" : "Paint/Draw/Sculpt",
             "LVTech" : "Land Vehicle Tech",
             "SVTech" : "Sea Vehicle Tech",
             "AVTech" : "Air Vehicle Tech",
             "ESTech" : "Electronics/Security Tech",
             "Martial" : "Martial Arts",
             "Wilderness" : "Wilderness Survival",
             "Melee": "Melee Weapon",
             "Conceal" : "Conceal/Reveal Object",
             "Contortion" : "Contortionist",
             "WardrobeStyle" : "Wardrobe & Style",
             "ElecSec" : "Electronics/Security Tech",
             "WeaponsTech" : "Weaponstech"}

def load_character_sheet(character_sheet_link:str) -> dict:
        """
            Parses the entries of a linked character sheet, and
            organizes its contents into a dictionary.

            :param character_sheet_link: The path to the character sheet to load

            Returns:
                The dictionary
        """
        character_sheet = PdfReader(character_sheet_link)
        test_fields = character_sheet.get_form_text_fields()
        #print(test_fields.keys())

        player_defined_fields:list[str] = []
        character_sheet_data = defaultdict(dict)

        for category in ['Skills','Weapons','Gear','Cyberware','Totals']:
            character_sheet_data[category] = defaultdict(dict)
        for category in ['Weapons','Gear','Cyberware']:
            character_sheet_data[category] = defaultdict(lambda: defaultdict(dict))

        for field, value in test_fields.items(): # All 

            # Category 1: Top-Left Box, PG. 1
            if (field.startswith("Role") or
                field in ['Notes', 'Text Field176'] ):
                
                if field == 'Text Field176': # stores character name
                    character_sheet_data["Handle"] = value

                character_sheet_data["Role"][field] = value

            # Category 2: STATs
            elif (field in ['INT','REF','DEX','TECH','COOL',
                        'WILL','LUCK-c','LUCK','MOVE','BODY',
                        'EMP MAX','EMP Curr', 'BODY-chargen']): 
                
                character_sheet_data["Stats"][field] = value

            # Category 3: Derived STATs
            elif (field in ['HPcurr', 'HPMax', 'SW_Value',
                            'DeathSave', 'HumanityCurr', 'HumanityMax']):

                character_sheet_data["Derived Stats"][field] = value

            # Category 4: All Skill LVL/MOD/BASEs
            elif (field.startswith("LVL") or 
                field.startswith("MOD") or
                field.startswith("BASE")):

                words:list[str] = field.split(" ")
                parameter, skill_name = words[0], " ".join(words[1:])

                # Alt 1: A skill has a known mapping that it should be renamed to.  
                if skill_name in maps.keys():
                    skill_name = maps[skill_name]

                # Alt 2: A "custom" skill, filled by player.
                elif ('LocalExpert' in field or 'Science' in field or
                        'PlayInstrument' in field or 'Lang' in field):
                    
                    variant_1 = "Txt_"+skill_name
                    variant_2 = "Txt "+skill_name

                    if variant_1 in test_fields:
                        skill_name = test_fields[variant_1]
                    elif variant_2 in test_fields:
                        skill_name = test_fields[variant_2]
                    else:
                        skill_name = test_fields[skill_name]
                else: # Could potentially need to separate words
                    skill_name = skill_name.split()[-1]
                    pattern = re.compile(r"[A-Z][a-z]*")
                    variant_1 = re.findall(pattern, skill_name)
                    skill_name = " ".join(variant_1)
        
                if not (skill_name == None or skill_name == ''): # Guards against empty custom skills
                    character_sheet_data["Skills"][skill_name][parameter] = value
                    
            # Category 5: Armor SP and Condition:
            elif ( field.startswith("SP") or 
                field.startswith("HPS")):
                
                if not field.endswith("Txt"): # Hard-coded, shouldn't load
                    pass

            # Category 6: All fields related to Weapons on PG. 1
            elif field.startswith("WeaponTxt"):
                
                num:int = int(field[9:])
                index = num-1 if num < 35 else num

                header:str = ''
                
                match (index % 5):
                    case 0:
                        header = "Name"      
                    case 1:
                        header = "DMG"  
                    case 2:
                        header = "Ammo"   
                    case 3:
                        header = "ROF" 
                    case 4:
                        header = "Notes"

                character_sheet_data["Weapons"][index//5][header] = value

            # Category 7: IP
            elif field in ['IpMax','IpCurr']:

                character_sheet_data[field] = value

            # Category 8: Gear
            elif field.startswith("Gear"):
                
                text = ''.join(re.findall(r'\S', field))
                digits = int(''.join(re.findall(r'\d', field)))
                
                character_sheet_data["Gear"][digits][text[4:8]] = value

            # Category 9: Ammo
            elif field in ["Ammunition"]:
                character_sheet_data[field] = value

            # Category 10: Cash
            elif field in ["Cash", "cash20"]: # Cash seems unused?
                if field == "cash20":
                    character_sheet_data["Cash"]["Amount"] = value
                else: #field == "Cash"
                    character_sheet_data["Cash"]["Notes"] = value

            # Category 11: Cyberware & Additional Notes
            elif field.startswith("TextField") or field.startswith("Text Field"):
                digits = int(''.join(re.findall(r'\d', field)))

                thresholds = [5, 11, 17, 25, 33, 47, 59, 65, 71, 85, 99, 114, 127] 
                slots = ["Cyberaudio Suite", "Right Cybereye", "Left Cybereye",
                        "Right Cyberarm", "Left Cyberarm",
                        "Neuroport", "Neural Link", "Right Cyberleg", "Left Cyberleg",
                        "Internal", "External", "Fashionware", "Borgware"]
                
                for slot, threshold in zip(slots, thresholds):
                    if digits <= threshold:

                        column = "Name" if digits % 2 == 0 else "Data"

                        # e.g. character_sheet/Cyberware/Neuroport/1/Name == "Biomonitor" 
                        character_sheet_data["Cyberware"][slot][digits//2][column] = value
                        break

                if digits > 127: # should be: 128-133; one of the big note pages PG. 4-6
                    character_sheet_data["Additional Notes"][field] = value

            # Category 12: Lifepath
            elif ("Friends" in field or
                "TragicLove" in field or
                "Enemies" in field or field == "Ex-friendo1" or # both refer to enemies
                field in ["Cultural Origins", "Personality", "Clothing Style", "HairStyle",
                            "ValueMost", "FeelingAboutPeople", "ValuedPerson","ValuedPossession",
                            "FamilyBackground", "ChildhoodEnvironment", "Family Crisis", "Life Goals",
                            "RoleSpecificLifepath"]):
                
                if field == "Ex-friendo1":
                    field = "Enemies1" # more consistent naming
                character_sheet_data["Lifepath"][field] = value
            
            # Category 13: HEAT
            elif field in ['Alias', 'RepEvents','Rep-Heat']:
                character_sheet_data["Heat"][field] = value

            # Category 14: Conditions
            elif field == 'Txt_Crit':
                character_sheet_data['Critical Injuries'] = value
            elif field == 'Txt_Addiction':
                character_sheet_data['Addictions'] = value

            # Category 15: Lifestyle
            elif (field in ['Housing', 'Rent', 'Lifestyle', 'Fashion']):
                character_sheet_data['Lifestyle'] = value

            # Category 16: Damage Taken
            elif (field in ['DMG Taken','BulletBrawl Head', 'MeleeMartial Body',
                            'MeleeMartial Head', 'BulletBrawl Body']):
                pass # Can't currently think of any meaningful reason to load this data

            # Category 17: Skill Totals
            elif field in ['TotalStats','skillsTotal','normSkills','doubleSkills']:
                character_sheet_data['Totals'][field] = value

            # Category 18: Names of "custom" skills (redundant)
            elif ('LocalExpert' in field or 
                'Science' in field or
                'PlayInstrument' in field or
                'Lang' in field):
                
                player_defined_fields.append(field)

            # Uncategorized: print as debug
            else:
                print(f"{field} \t\t {value}")

        # SKILLs/STATS
        stat_associations = pd.read_csv(r"data/skills.csv")
        assert(len(stat_associations) > 10)

        print(player_defined_fields)
        for skill_name in character_sheet_data['Skills'].keys():

            #print(skill_name)
            stat_group = determine_stat_group(skill_name, stat_associations)

            # Alt Path: The skill is player-defined (fill-in-blanks)
            if stat_group == "UNK": 
                for field in player_defined_fields:
                    if test_fields[field] == skill_name:
                        canon_skill_name = field[4:-1] if field.startswith("Txt") else field[:-1]
                        #print(f"Canon: {canon_skill_name}")
                        stat_group = determine_stat_group(canon_skill_name, stat_associations)

            character_sheet_data['Skills'][skill_name]["STAT"] = stat_group
        
        return dict(character_sheet_data)


def determine_stat_group(skill_name: str, df: pd.DataFrame) -> str:
    """
    :param skill_name: The name of the skill to lookup
    :param df: the data set of skills and their mappings to stats
    
    Returns:
        The stat that is associated with the given skill_name.
    """
    bucket = "UNK"
    if skill_name in list(df["SkillName"]):
        bucket = df.loc[df["SkillName"] == skill_name, "AlignedStat"].iloc[0]
        bucket = bucket.strip()
    else:
        print(f"{skill_name} was not found :()")
    return bucket
    