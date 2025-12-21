import tkinter as tk
import json
from ..modifier import Modifier

from collections import defaultdict


class CyberwarePage(tk.Frame):
    """
    A Page that allows you to assign/config all things related
    to Drugs and Addictions
    
    :var Returns: Description
    :vartype Returns: The
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.effects = self.load_cyberware(r"data/cyberware.json")    
        self.modifier: Modifier = Modifier()

        cyberware = self.parent.character_sheet["Cyberware"]

        for slot_name, contents in cyberware.items():
            cyberware_frame = tk.LabelFrame(self, text=slot_name,
                                            bg="#000000", fg='#ffffff',
                                            relief='solid', borderwidth='1px')

            has_installations: bool = False
            for slot in contents.values():
                if 'Name' not in slot.keys() or slot['Name'] is None or slot['Name'] == '':
                    continue
                self.modifier += self.cyberware_modifier(slot['Name'])
                has_installations = True
                y = tk.Label(cyberware_frame, text=slot['Name'], width=25, bg="#91f6e3")
                y.pack(side='top')

            if has_installations:
                cyberware_frame.pack(side='left')


    def cyberware_modifier(self, cyberware_name) -> Modifier:
        """
        Checks the list of all cyberware, and creates a Modifier out of the known effects.
        
        :param cyberware_name: The name of the Cyberware to lookup
        
        Returns:
            A Modifier corresponding to the cyberware_name if found, otherwise
            an empty Modifier
        """
      
        if cyberware_name in self.effects.keys():

            print(f"Found {cyberware_name} in keys!")

            cyberware: dict = self.effects[cyberware_name]

            effect_list: list[tuple[str,int]] = []
            ignore_list: list[str] = []

            if 'affects' in cyberware.keys():
                for affect, magnitude in cyberware['affects'].items():
                    effect_list.append((affect, magnitude))
            if 'ignores' in cyberware.keys():
                for ignored in cyberware['ignores']:
                    ignore_list.append(ignored)

            return Modifier(cyberware_name, effect_list, ignore_list)
        
        return Modifier()

    def load_cyberware(self, cyberware_json_path) -> dict:

        with open(cyberware_json_path, 'r') as modifier_file:
            data: dict = json.load(modifier_file)
            return data

        
            





        
                       
            