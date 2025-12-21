import tkinter as tk
import pandas as pd

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

        tk.Label(self, width=25, text=f"Weapon", anchor='w', bg='#000000', fg='#ffffff' ).grid(row=0, column=0)
        tk.Label(self, width=5, text=f"DMG",  bg='#000000', fg='#ffffff').grid(row=0, column=1)
        tk.Label(self, width=5, text=f"Ammo",  bg='#000000', fg='#ffffff').grid(row=0, column=2)
        tk.Label(self, width=5, text=f"ROF",  bg='#000000', fg='#ffffff').grid(row=0, column=3)
        tk.Label(self, width=25, text=f"Notes",  bg='#000000', fg='#ffffff', anchor='w').grid(row=0, column=4)

        weapons = self.parent.character_sheet["Weapons"]

        i: int = 1
        for weapon in weapons.values():
            #print(weapon)
            if weapon["Name"] is None or weapon["Name"] == "":
                continue

            tk.Button(self, width=25, text=weapon["Name"], anchor='w',
                                            fg='#000000', bg="#47B35D",
                                            command=lambda weapon=weapon["Name"]: self.weapon_attack_check(weapon)).grid(row=i, column=0)
            tk.Button(self, width=5, text=weapon["DMG"],
                                            fg='#000000', bg="#47B35D",
                                            command=lambda dmg=weapon["DMG"], weapon=weapon["Name"]: self.damage_roll(dmg, weapon)).grid(row=i, column=1)
            tk.Label(self, width=5, text=weapon["ROF"]).grid(row=i, column=2)
            tk.Label(self, width=5, text=weapon["Ammo"]).grid(row=i, column=3)
            tk.Label(self, width=25, text=weapon["Notes"]).grid(row=i, column=4)
            i += 1

    
    def damage_roll(self, roll:str, weapon:str, modifiers=None):
        
        #TODO Weapons might have an intrinsic +1
        #TODO Combat awareness

        #Modifier --> Whatever Skill, Ranged, All Actions, Attack 

        if modifiers == None:
            modifiers = []
        modifiers = "".join(modifiers)

        discord_command = f"!r {roll+modifiers} Damage w/ {weapon}"
        self.parent.update_clipboard(discord_command)


    def weapon_attack_check(self, weapon_name) -> None:
        """
        Copies the Discord command for a particular weapon attack check to the clipboard
        
        :param weapon_name: The weapon we are performing an attack check with
        """

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
        drug_modifier = self.parent.pages["Drugs"].get_active_effects()
        injury_modifier = self.parent.pages["Injuries"].get_active_effects()

        modifier = drug_modifier + injury_modifier

        magnitude_list: list[str] = []
        reason_list: list[str] = []

        relevant = [skill_name, stat_name, "All Actions"] # Attacks... weaponmodifier

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


        discord_command = f"!r 1d10+{base}{magnitudes} Attack w/ {weapon_name}{reasons}"
        self.parent.update_clipboard(discord_command)