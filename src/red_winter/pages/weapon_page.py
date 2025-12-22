import tkinter as tk
import pandas as pd

from ..modifier import Modifier

#MAP WEAPON TYPES TO SKILLS
skills_for_weapons = {
    'Medium Pistol' : 'Handgun',
    'Heavy Pistol' : 'Handgun',
    'Very Heavy Pistol' : 'Handgun',
    'SMG' : 'Handgun',
    'Heavy SMG' : 'Handgun',
    'Shotgun': 'Shoulder Arms',
    'Assault Rifle' : 'Shoulder Arms',
    'Sniper Rifle' : 'Shoulder Arms',
    'Bow' : 'Archery',
    'Grenade Launcher' : 'Heavy Weapons',
    'Rocket Launcher' 'Heavy Weapons'
    'Light Melee' : 'Melee Weapon',
    'Medium Melee' : 'Melee Weapon',
    'Heavy Melee' : 'Melee Weapon',
    'Very Heavy Melee' : 'Melee Weapon',
    'Thrown Weapon' : 'Melee Weapon',
    'Crossbow' : 'Archery'
}

class WeaponPage(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent



        """tk.Label(self, width=25, text=f"Weapon", anchor='w', bg='#000000', fg='#ffffff' ).grid(row=0, column=0)
        tk.Label(self, width=5, text=f"DMG",  bg='#000000', fg='#ffffff').grid(row=0, column=1)
        tk.Label(self, width=5, text=f"Ammo",  bg='#000000', fg='#ffffff').grid(row=0, column=2)
        tk.Label(self, width=5, text=f"ROF",  bg='#000000', fg='#ffffff').grid(row=0, column=3)
        tk.Label(self, width=25, text=f"Notes",  bg='#000000', fg='#ffffff', anchor='w').grid(row=0, column=4)"""

        weapons = self.parent.character_sheet["Weapons"]

        i: int = 1
        for weapon in weapons.values():
            self.create_weapon_entry(weapon)
    
    def create_weapon_entry(self, weapon: dict):
        print(weapon)

        if not (weapon["Name"] is None or weapon["Name"] == ""):
            

            aimed_shot_available: bool = True # TODO, make logic to check for this

            # Single Shot



            weapon_frame = tk.LabelFrame(self, text=weapon['Name'], width=40)


            # Single Shot Attack
            attack_frame = tk.Frame(weapon_frame, width=40)

            tk.Button(attack_frame, width=25, text="Single Shot", anchor='w',
                                            fg='#000000', bg="#47B35D",
                                            command=lambda weapon=weapon: self.weapon_attack_check(weapon)).pack(side='left')
            tk.Button(attack_frame, width=5, text=weapon["DMG"],
                                            fg='#000000', bg="#47B35D",
                                            command=lambda dmg=weapon["DMG"], weapon=weapon["Name"]: self.damage_roll(dmg, weapon)).pack(side='left')
            tk.Label(attack_frame, width=5, text=f"ROF: {weapon["ROF"]}").pack(side='left')
            tk.Label(attack_frame, width=5, text=weapon["Ammo"]).pack(side='left')

            attack_frame.pack()

            if aimed_shot_available: # Aimed Shot
                aimed_attack_frame = tk.Frame(weapon_frame, width=40)

                aimed_shot_penalty = Modifier("Aimed Shot", [("Aimed Shot", -8)])

                tk.Button(aimed_attack_frame, width=25, text="Aimed Shot", anchor='w',
                                                fg='#000000', bg="#47B35D",
                                                command=lambda weapon=weapon, other_checks=["Aimed Shot"], other_modifiers=[aimed_shot_penalty], action="Aimed Shot": self.weapon_attack_check(weapon, other_checks, other_modifiers, action)).pack(side='left')
            
                tk.Button(aimed_attack_frame, width=5, text=weapon["DMG"],
                                                fg='#000000', bg="#47B35D",
                                                command=lambda dmg=weapon["DMG"], weapon=weapon["Name"]: self.damage_roll(dmg, weapon)).pack(side='left')
                tk.Label(aimed_attack_frame, width=5, text=f"ROF: 1").pack(side='left')
                tk.Label(aimed_attack_frame, width=5, text=weapon["Ammo"]).pack(side='left')
                aimed_attack_frame.pack()






            tk.Label(weapon_frame, width=40, text=weapon["Notes"], anchor='w').pack()
            weapon_frame.pack()
            


    def damage_roll(self, roll:str, weapon:str, modifiers=None):
        
        #TODO Weapons might have an intrinsic +1
        #TODO Combat awareness

        #Modifier --> Whatever Skill, Ranged, All Actions, Attack 

        if modifiers == None:
            modifiers = []
        modifiers = "".join(modifiers)

        discord_command = f"!r {roll+modifiers}+1 Damage w/ {weapon} (Combat Awareness)"

        #TODO Replace this Jury Rigging w/ proper management of Combat Awareness
        if self.parent.character_sheet["Handle"] != "Crux":
            discord_command = f"!r {roll+modifiers} Damage w/ {weapon}"

        self.parent.update_clipboard(discord_command)


    #TODO generalize for AIMED shots
    def weapon_attack_check(self, weapon: dict, other_checks=None, other_modifiers=None, action:str="Attack") -> None:
        """
        Copies the Discord command for a particular weapon attack check to the clipboard
        
        :param weapon_name: The weapon we are performing an attack check with
        """
        weapon_name: str = weapon["Name"]
        weapons_list = pd.read_csv(r"data\weapons.csv")

        for i in range(len(weapon_name)):
            weapons_list = weapons_list[ 
                weapons_list["name"].str.startswith(weapon_name[:i+1], na=False)
            ]
            if len(weapons_list) <= 1:
                break

        if len(weapons_list) == 0:
            print(f"can't find {weapon_name}")
            return

        skill_name = skills_for_weapons[weapons_list['type'].iloc[0]]

        # Same logic from before

        stat_name = self.parent.character_sheet["Skills"][skill_name]["STAT"]
        drug_modifier: Modifier = self.parent.pages["Drugs"].get_active_effects()
        injury_modifier: Modifier = self.parent.pages["Injuries"].get_active_effects()
        cyberware_modifier: Modifier = self.parent.pages["Cyberware"].get_active_effects()

        modifier: Modifier = Modifier()

        if other_modifiers is None:
            other_modifiers = []
        modifier_list = [drug_modifier, injury_modifier, cyberware_modifier] + other_modifiers
        for current in modifier_list:
            modifier += current

        #TODO make this nicer, this is a jury rig for rn
        if "EQ" in weapon['Notes']:
            modifier += Modifier("EQ", [("All Actions", 1)])
        if "Smartlink" in weapon['Notes']:
            modifier += Modifier("Smartlink", [("All Actions", 1)])

        magnitude_list: list[str] = []
        reason_list: list[str] = []

        if other_checks is None:
            other_checks = []

        relevant = [skill_name, stat_name, "All Actions"] + other_checks # Attacks... weaponmodifier

        for affect in relevant:
            curr_mag, curr_reason = modifier.get_affect(affect)
            magnitude_list.append(curr_mag)
            reason_list.append(curr_reason)

        magnitudes: str = "".join(magnitude_list)

        reason_list = [r for r in reason_list if r != ""]
        reasons: str = ",".join(reason_list)        
        
        base = self.parent.character_sheet["Skills"][skill_name]["BASE"]

        if len(reasons) > 0:
            reasons = ' (' + reasons + ')'


        discord_command = f"!r 1d10+{base}{magnitudes} {action} w/ {weapon_name}{reasons}"
        self.parent.update_clipboard(discord_command)