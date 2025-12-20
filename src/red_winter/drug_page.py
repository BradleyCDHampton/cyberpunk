import tkinter as tk
import json
from .modifier import Modifier

class DrugPage(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        #[("Archery", 1), ("Brawling",-2)]

        self.drugs = []
        self.addictions = []

        with open(r"data/modifiers.json", 'r') as modifier_file:
            data: dict = json.load(modifier_file)

            for modifier_name, contents in data.items():

                modifier_list: list[tuple[str,int]] = []
                ignore_list: list[str] = []

                if 'affects' in contents.keys():
                    for affect, magnitude in contents['affects'].items():
                        modifier_list.append((affect, magnitude))
                if 'ignores' in contents.keys():
                    for ignored in contents['ignores']:
                        ignore_list.append(ignored)

                modifier = Modifier(modifier_name, modifier_list, ignore_list)

                if contents['type'] == 'Drug':
                    self.drugs.append(modifier)
                elif contents['type'] == 'Addiction':
                    self.addictions.append(modifier)

        self.effects: dict[Modifier, tk.BooleanVar] = {}

        for drug_modifier in self.drugs:
            modifier_name = drug_modifier.modifier_list[-1]

            checkbox_parity = tk.BooleanVar(self, False, modifier_name)
            checkbox_ui  = tk.Checkbutton(self, text=modifier_name,
                                          variable=checkbox_parity,
                                          width=30, anchor='w')
            self.effects[drug_modifier] = checkbox_parity
            checkbox_ui.pack()

        for addiction_modifier in self.addictions:
            pass
            #TODO
    
    def get_active_effects(self) -> Modifier:
        """Returns: The combined Modifier of all effects that are checked"""

        combined_modifier: Modifier = Modifier()

        for effect, parity in self.effects.items():
            if parity.get() == True:
                combined_modifier = combined_modifier + effect
        
        return combined_modifier

        
                       
            