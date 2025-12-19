from PyPDF2 import PdfReader
import tkinter as tk
from collections import defaultdict
import re

from .skill_page import SkillPage
from .weapon_page import WeaponPage
from .navigation_bar import NavigationBar

from .utils import determine_stat_group

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

class MainApplication(tk.Frame):

    def __init__(self, parent, character_sheet_link, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Initialize Character Sheet
        self.character_sheet_link = character_sheet_link
        self.character_sheet = self.load_character_sheet(character_sheet_link)

        self.pages = {}

        self.pages["Skills"] = SkillPage(self)
        self.pages["Weapons"] = WeaponPage(self)

        self.navigation = NavigationBar(self)

        self.navigation.pack(side='bottom')



    def load_character_sheet(self, character_sheet_link:str) -> dict:
        """
            Parses the entries of a linked character sheet, and
            organizes its contents into a dictionary.
        """
        character_sheet = PdfReader(character_sheet_link)
        test_fields = character_sheet.get_form_text_fields()

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


            # Category 2: All Skill LVL/MOD/BASEs
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
        
                if not (skill_name == None or skill_name == ''): # Guards against empty custom skills
                    character_sheet_data["Skills"][skill_name][parameter] = value
                    
            # Category: Armor SP and Condition:
            elif ( field.startswith("SP") or 
                field.startswith("HPS")):
                
                if not field.endswith("Txt"): # Hard-coded, shouldn't load
                    pass

            # Category 4: All fields related to Weapons on PG. 1
            elif field.startswith("WeaponTxt"):
                pass
                #weapon_fields.append((field, value))

            # Category: IP
            elif field in ['IpMax','IpCurr']:

                character_sheet_data[field] = value

            # Category 5: Gear
            elif field.startswith("Gear"):
                
                text = ''.join(re.findall(r'\S', field))
                digits = int(''.join(re.findall(r'\d', field)))
                
                character_sheet_data["Gear"][digits][text[4:8]] = value

            # Category: Ammo
            elif field in ["Ammunition"]:
                character_sheet_data[field] = value

            # Category: Cash
            elif field in ["Cash", "cash20"]: # Cash seems unused?
                if field == "cash20":
                    character_sheet_data["Cash"]["Amount"] = value
                else: #field == "Cash"
                    character_sheet_data["Cash"]["Notes"] = value

            # Category 6: Cyberware & Additional Notes
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

            # Category 7: Lifepath
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
            
            # Category: HEAT
            elif field in ['Alias', 'RepEvents','Rep-Heat']:
                character_sheet_data["Heat"][field] = value

            # Category: Conditions
            elif field == 'Txt_Crit':
                character_sheet_data['Critical Injuries'] = value
            elif field == 'Txt_Addiction':
                character_sheet_data['Addictions'] = value

            # Category: Lifestyle
            elif (field in ['Housing', 'Rent', 'Lifestyle', 'Fashion']):
                character_sheet_data['Lifestyle'] = value

            # Category 8: Damage Taken
            elif (field in ['DMG Taken','BulletBrawl Head', 'MeleeMartial Body',
                            'MeleeMartial Head', 'BulletBrawl Body']):
                pass # Can't currently think of any meaningful reason to load this data

            # Category: Skill Totals
            elif field in ['TotalStats','skillsTotal','normSkills','doubleSkills']:
                character_sheet_data['Totals'][field] = value

            # Categories: Names of "custom" skills (redundant)
            elif ('LocalExpert' in field or 
                'Science' in field or
                'PlayInstrument' in field or
                'Lang' in field):
                
                continue # basically just don't print these as uncategorized

            # Uncategorized: print as debug
            else:
                print(f"{field} \t\t {value}")

        return dict(character_sheet_data)




        


   