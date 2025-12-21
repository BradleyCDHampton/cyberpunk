import tkinter as tk
import json
from ..modifier import Modifier

class InjuryPage(tk.Frame):
    """
    A Page that allows you to assign/config all things related
    to Drugs and Addictions
    
    :var Returns: Description
    :vartype Returns: The
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        
        self.critical_injuries = []

        with open(r"data/modifiers.json", 'r') as modifier_file:
            data: dict = json.load(modifier_file)

            for modifier_name, contents in data.items():

                modifier_list: list[tuple[str,int]] = []
                ignore_list: list[str] = []

                if 'affects' in contents.keys():
                    for affect, magnitude in contents['affects'].items():
                        modifier_list.append((affect, magnitude))

                modifier = Modifier(modifier_name, modifier_list, ignore_list)

                if contents['type'] == 'Critical Injury':
                    self.critical_injuries.append(modifier)

        self.effects: dict[Modifier, tk.BooleanVar] = {}

        critical_injury_frame: tk.Frame = tk.Frame(self)
        
        for injury in self.critical_injuries:
            modifier_name = injury.modifier_list[-1]

            checkbox_parity = tk.BooleanVar(critical_injury_frame, False, modifier_name)
            checkbox_ui  = tk.Checkbutton(critical_injury_frame, text=modifier_name,
                                          variable=checkbox_parity,
                                          width=30, anchor='w')
            self.effects[injury] = checkbox_parity
            checkbox_ui.pack()

        critical_injury_frame.pack(side='left')

    
    def get_active_effects(self) -> Modifier:
        """Returns: The combined Modifier of all effects that are checked"""

        combined_modifier: Modifier = Modifier()

        for effect, parity in self.effects.items():
            if parity.get() == True:
                combined_modifier = combined_modifier + effect
        
        return combined_modifier

        
                       
            