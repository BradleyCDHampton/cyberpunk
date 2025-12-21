import tkinter as tk
import json
from .modifier import Modifier

from collections import defaultdict


class DrugPage(tk.Frame):
    """
    A Page that allows you to assign/config all things related
    to Drugs and Addictions
    
    :var Returns: Description
    :vartype Returns: The
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        #[("Archery", 1), ("Brawling",-2)]

        drug_modifiers: defaultdict[str, dict[str, Modifier]] = defaultdict(dict)

        with open(r"data/modifiers.json", 'r') as modifier_file:
            data: dict = json.load(modifier_file)

            for modifier_name, contents in data.items():

                effect_list: list[tuple[str,int]] = []
                ignore_list: list[str] = []

                if 'affects' in contents.keys():
                    for affect, magnitude in contents['affects'].items():
                        effect_list.append((affect, magnitude))
                if 'ignores' in contents.keys():
                    for ignored in contents['ignores']:
                        ignore_list.append(ignored)

                modifier = Modifier(modifier_name, effect_list, ignore_list)
    
                if contents['type'] == 'Drug':
                    drug_modifiers[modifier_name]['Drug'] = modifier
                elif contents['type'] == 'Addiction':
                    drug_modifiers[modifier_name[11:]]['Addiction'] = modifier


        self.effects: dict[Modifier, tk.BooleanVar] = {}

        i: int = 0
        for drug_name, effects in sorted(drug_modifiers.items()):
            drug_frame = tk.LabelFrame(self, text=drug_name,
                                       bg="#000000", fg='#ffffff',
                                       relief='solid', borderwidth='1px')

            for effect_name, effect_modifier in effects.items():
                
                checkbox_parity = tk.BooleanVar(drug_frame, False, drug_name+effect_name)
                checkbox_ui  = tk.Checkbutton(drug_frame, text=effect_name,
                                            variable=checkbox_parity,
                                            bg="#DA8686",
                                            width=15, anchor='w')
                self.effects[effect_modifier] = checkbox_parity
                checkbox_ui.pack(side='left')

            drug_frame.grid(row=i%9, column=i//9)
            i += 1

    
    def get_active_effects(self) -> Modifier:
        """Returns: The combined Modifier of all effects that are checked"""

        combined_modifier: Modifier = Modifier()

        for effect, parity in self.effects.items():
            if parity.get() == True:
                combined_modifier = combined_modifier + effect
        
        return combined_modifier

        
                       
            