import tkinter as tk
import pandas as pd

from ..modifier import Modifier

colors = ["#A0D0E2", "#BDADE6", "#9F5BFF", "#EA7D3A", "#B3CE1B"]


class NetrunningPage(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        weapons = self.parent.character_sheet["Weapons"]

        black_ice_bestiary = pd.read_csv(r"data\black_ice.csv")
        curr: list[dict] = black_ice_bestiary.to_dict(orient='records')

        # Create Entries for each Weapon
        i: int = 0
        for black_ice in curr:
            self.create_weapon_entry(black_ice, i)
            i += 1
    

    # Non-Black Ice

    # Black Ice

    def create_weapon_entry(self, black_ice: dict, color:int=0) -> None:
        """
        Generates a tkinter Frame containing UI to roll for accuracy/damage
        for a weapon, providing a button for each firing mode #TODO
        
        :param weapon: The weapon, and all its data
        :param color: Indicates the color to render the frame
        """
        if not (black_ice["name"] is None or black_ice["name"] == ""):
            
            weapon_frame = tk.LabelFrame(self, text=f"{black_ice['name']}, {black_ice['class'][:10]}", width=40, bg='#000000', fg='#ffffff', relief='solid')

            # Single Shot Attack
            attack_frame = tk.Frame(weapon_frame, width=50, bg=colors[color])

            #Button for Perception
            tk.Button(attack_frame, width=25, text="Perception", anchor='w',
                                            fg='#000000', bg="#47B35D",
                                            command=lambda black_ice=black_ice: self.net_check(black_ice)).pack(side='left')
            #Button for Speed
            #Button for Attack
            #Button for Defense

            #Button for Damage

            #curr_rez
            #max_rez

            tk.Label(attack_frame, width=5, text=black_ice["rez"], bg=colors[color%5]).pack(side='left')
            #effect

            
            """tk.Button(attack_frame, width=5, text=black_ice["Speed"],
                                            fg='#000000', bg="#47B35D",
                                            command=lambda dmg=black_ice["DMG"], weapon=black_ice["Name"]: self.damage_roll(dmg, weapon)).pack(side='left')"""
            




            attack_frame.pack()

            weapon_frame.pack()
            
    
    def get_accuracy_modifier(self) -> Modifier:
        """
        Generates a modifier that encapsulates all of the ways an attack check can be modified.
        
        Returns:
            A Modifier object that contains the data from the Precision Strike, Luck, and
            Situational Modifier fields.

            If there is an error parsing these fields (mal-formed), then an empty Modifier
            is returned instead.
        """
        """        result: Modifier = Modifier()
                
                try:
                    for modifier_name in ["Precision Strike","Luck", "Situational"]:
                        value = self.modifier_data[modifier_name].get()
                        if not (value is None or value == ''):
                            result += Modifier(modifier_name, [("All Actions", int(value))])
                except:
                    print("Error parsing accuracy Modifier")
                    result = Modifier()

                return result"""

    def get_damage_modifier(self) -> Modifier:
        """
        Generates a Modifier for how much bonus damage that will happen on
        an attack's successful hit

        Returns:
            The Modifier that affects the damage that will be rolled
            (probably just Spot Weakness)
        """
        result = Modifier()
        try:
            value = self.modifier_data["Spot Weakness"].get()
            if not (value is None or value == ''):
                result += Modifier("Spot Weakness", [("All Actions", int(value))])
        except:
            print("Error parsing accuracy Modifier")
            result = Modifier()

        return result
        
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

    def damage_roll(self, roll:str, black_ice:str):
        
        #TODO Weapons might have an intrinsic +1
        #TODO Combat awareness

        #Modifier --> Whatever Skill, Ranged, All Actions, Attack 

        damage_modifier: Modifier = self.get_damage_modifier()
        magnitudes, reasons = damage_modifier.get_affect("All Actions")

        if len(reasons) > 0:
            reasons = ' (' + reasons + ')'

        discord_command = f"!r {roll}{magnitudes} Damage w/ {black_ice}{reasons}"

        self.parent.update_clipboard(discord_command)


    #TODO generalize for AIMED shots
    def net_check(self, program: dict, other_checks=None, other_modifiers=None, action:str="Attack") -> None:
        """
        Copies the Discord command for a particular weapon attack check to the clipboard
        
        :param weapon_name: The weapon we are performing an attack check with
        """
        program_name: str = program["Name"]

        # Same logic from before

        modifier: Modifier = Modifier()

        if other_modifiers is None:
            other_modifiers = []
        modifier_list = [] + other_modifiers
        for current in modifier_list:
            modifier += current

        magnitude_list: list[str] = []
        reason_list: list[str] = []

        if other_checks is None:
            other_checks = []

        relevant = ["All Actions"] + other_checks # Attacks... weaponmodifier

        for affect in relevant:
            curr_mag, curr_reason = modifier.get_affect(affect)
            magnitude_list.append(curr_mag)
            reason_list.append(curr_reason)

        magnitudes: str = "".join(magnitude_list)

        reason_list = [r for r in reason_list if r != ""]
        reasons: str = ",".join(reason_list)        
        
        if len(reasons) > 0:
            reasons = ' (' + reasons + ')'

        discord_command = f"!r 1d10+{magnitudes} {action} w/ {program_name}{reasons}"
        self.parent.update_clipboard(discord_command)