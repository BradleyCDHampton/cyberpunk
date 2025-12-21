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

        #[("Archery", 1), ("Brawling",-2)]

        cyberware = self.parent.character_sheet["Cyberware"]

        for slot_name, contents in cyberware.items():
            cyberware_frame = tk.LabelFrame(self, text=slot_name,
                                            bg="#000000", fg='#ffffff',
                                            relief='solid', borderwidth='1px')

            has_installations: bool = False
            for slot in contents.values():
                if 'Name' not in slot.keys() or slot['Name'] is None:
                    continue
                has_installations = True
                y = tk.Label(cyberware_frame, text=slot['Name'], width=25, bg="#91f6e3")
                y.pack(side='top')
            if has_installations:
                cyberware_frame.pack(side='left')




        
                       
            