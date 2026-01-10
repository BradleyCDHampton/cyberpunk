import tkinter as tk
import pandas as pd

from .combat_awareness import CombatAwarenessPage
from ..modifier import Modifier
from ..rolls import damage_roll

colors = ["#A0D0E2", "#BDADE6", "#9F5BFF", "#EA7D3A", "#B3CE1B"]

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

        # Create fill-in Modifiers
        modifier_fields: list[str] = ["Luck", "Situational"]
        self.modifier_data: dict[str, tk.Entry] = self.create_modifier_fields(modifier_fields)

        weapons = self.parent.character_sheet["Weapons"]

        # Create Entries for each Weapon
        i: int = 0
        for weapon in weapons.values():
            self.create_weapon_entry(weapon, i)
            i += 1
    

    def create_weapon_entry(self, weapon: dict, color:int=0) -> None:
        """
        Generates a tkinter Frame containing UI to roll for accuracy/damage
        for a weapon, providing a button for each firing mode #TODO
        
        :param weapon: The weapon, and all its data
        :param color: Indicates the color to render the frame
        """
        if not (weapon["Name"] is None or weapon["Name"] == ""):
            
            # Alternative Firing Modes
            aimed_shot_available: bool = True #TODO, make logic to check for this
            autofire_available: bool = False #TODO
            suppressive_fire_available: bool = False #TODO
            shotgun_shell_available: bool = False #TODO

            weapon_frame = tk.LabelFrame(self, text=weapon['Name'], width=40, bg='#000000', fg='#ffffff', relief='solid')

            # Single Shot (always available?)
            self.create_attack_entry(weapon_frame, "Single Shot", weapon, color)

            if aimed_shot_available:
                aimed_shot_penalty = Modifier("Aimed Shot", [("Aimed Shot", -8)])
                self.create_attack_entry(weapon_frame, "Aimed Shot", weapon, color, rate_of_fire=1, attack_modifiers=[aimed_shot_penalty], attack_checks=["Aimed Shot"])
            if autofire_available:
                pass #TODO 
            if suppressive_fire_available:
                pass #TODO
            if shotgun_shell_available:
                pass #TODO

            tk.Label(weapon_frame, width=40, text=weapon["Notes"], anchor='w', bg=colors[color]).pack(fill='x')
            weapon_frame.pack()
            
    def create_attack_entry(self, weapon_frame:tk.LabelFrame, attack_label:str, weapon: dict, color:int=0, damage=None, rate_of_fire=None, attack_modifiers=None, attack_checks=None) -> None:
        """
        Creates a row in a weapon_frame, providing information about a particular way to attack, and buttons
        to press to generate/copy the commands for an attack or damage roll.
        
        :param weapon_frame: The frame where the attack entry will be put inside
        :param attack_label: How the attack is described (e.g. Single Shot, Aimed Shot, Autofire)
        :param weapon: The dictionary containing information about the weapon that is used
        :param color: Indicates the color to render the background the labels
        :param damage: Optional: overrides the standard damage roll to be used. If not defined, uses weapon['DMG']
        :param rate_of_fire: override for the ROF to be used. If not defined, uses weapon['ROF']
        :param attack_modifiers: Any additional modifiers that might apply to the attack check
        :param attack_checks: Any additional modifier affects that might apply to the attack (e.g. Aimed Shot)
        """
        damage = damage or weapon['DMG']
        damage = str(damage)

        rate_of_fire = rate_of_fire or weapon['ROF']
        rate_of_fire = str(rate_of_fire)
        
        attack_modifiers = attack_modifiers or []
        attack_checks = attack_checks or []

        attack_frame = tk.Frame(weapon_frame, width=50, bg=colors[color])

        tk.Button(attack_frame, width=25, text=attack_label, anchor='w',
                                        fg='#000000', bg="#47B35D",
                                        command=lambda weapon=weapon, other_checks=attack_checks, other_modifiers=attack_modifiers, action=attack_label: self.weapon_attack_check(weapon, other_checks, other_modifiers, action)).pack(side='left')
        tk.Button(attack_frame, width=5, text=damage,
                                        fg='#000000', bg="#47B35D",
                                        command=lambda dmg=damage, weapon=weapon["Name"], : damage_roll(self.parent, dmg, weapon, [self.parent.pages["Combat Awareness"].get_modifier()])).pack(side='left')
        tk.Label(attack_frame, width=5, text=f"ROF: {rate_of_fire}", bg=colors[color]).pack(side='left')
        tk.Label(attack_frame, width=5, text=weapon["Ammo"], bg=colors[color]).pack(side='left')

        attack_frame.pack()


    def get_accuracy_modifier(self) -> Modifier:
        """
        Generates a modifier that encapsulates all of the ways an attack check can be modified.
        
        Returns:
            A Modifier object that contains the data from the Precision Strike, Luck, and
            Situational Modifier fields.

            If there is an error parsing these fields (mal-formed), then an empty Modifier
            is returned instead.
        """
        result: Modifier = Modifier()
        
        try:
            for modifier_name in ["Luck", "Situational"]:
                value = self.modifier_data[modifier_name].get()
                if not (value is None or value == ''):
                    result += Modifier(modifier_name, [("All Actions", int(value))])
        except:
            print("Error parsing accuracy Modifier")
            result = Modifier()

        return result

    """    def get_damage_modifier(self) -> Modifier:
        
        Generates a Modifier for how much bonus damage that will happen on
        an attack's successful hit

        Returns:
            The Modifier that affects the damage that will be rolled
            (probably just Spot Weakness)

        result = Modifier()
        try:
            value = self.modifier_data["Spot Weakness"].get()
            if not (value is None or value == ''):
                result += Modifier("Spot Weakness", [("All Actions", int(value))])
        except:
            print("Error parsing accuracy Modifier")
            result = Modifier()

        return result"""
        
    def create_modifier_fields(self, modifier_fields: list[str]) -> dict[str, tk.Entry]:
        """
        Creates the set of fields where a user can input their modifiers that cannot be determined 
        at initialization (fluctuates during play)

        :param modifier_fields: The names of the fields, and also what the text label will be
        
        Returns:
            A dictionary of the names of each field, mapped to its entry box.
        """
        result: dict = {}
        for modifier_name in modifier_fields:

            modifier_frame = tk.Frame(self, width=40)

            tk.Label(modifier_frame, text=modifier_name, width=20, anchor='w').pack(side='left')
            result[modifier_name] = tk.Entry(modifier_frame, width=10)
            result[modifier_name].pack(side='left')

            modifier_frame.pack()

        return result


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
        combat_awareness_modifier = self.parent.pages["Combat Awareness"].get_modifier()

        modifier: Modifier = Modifier()

        if other_modifiers is None:
            other_modifiers = []
        modifier_list = [drug_modifier, injury_modifier, cyberware_modifier, combat_awareness_modifier, self.get_accuracy_modifier()] + other_modifiers
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

        relevant = [skill_name, stat_name, "All Actions","Attack"] + other_checks # Attacks... weaponmodifier

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