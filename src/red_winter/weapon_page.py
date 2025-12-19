import tkinter as tk

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
            print(weapon)
            if weapon["Name"] is None or weapon["Name"] == "":
                continue

            tk.Button(self, width=25, text=weapon["Name"], anchor='w',
                                            fg='#000000', bg="#47B35D",
                                            command=lambda weapon=weapon["Name"]: self.parent.weapon_roll(weapon)).grid(row=i, column=0)
            tk.Button(self, width=5, text=weapon["DMG"],
                                            fg='#000000', bg="#47B35D",
                                            command=lambda dmg=weapon["DMG"], weapon=weapon["Name"]: self.parent.damage_roll(dmg, weapon)).grid(row=i, column=1)
            tk.Label(self, width=5, text=weapon["ROF"]).grid(row=i, column=2)
            tk.Label(self, width=5, text=weapon["Ammo"]).grid(row=i, column=3)
            tk.Label(self, width=25, text=weapon["Notes"]).grid(row=i, column=4)
            i += 1
        
                       
            