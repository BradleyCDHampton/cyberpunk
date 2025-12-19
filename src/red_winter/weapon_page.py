import tkinter as tk
from .utils import damage_roll, weapon_roll

class WeaponPage(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        fields = self.parent.fields

        x:list = [None] * 39

        tk.Label(self, width=25, text=f"Weapon", anchor='w', bg='#000000', fg='#ffffff' ).grid(row=0, column=0)
        tk.Label(self, width=5, text=f"DMG",  bg='#000000', fg='#ffffff').grid(row=0, column=1)
        tk.Label(self, width=5, text=f"Ammo",  bg='#000000', fg='#ffffff').grid(row=0, column=2)
        tk.Label(self, width=5, text=f"ROF",  bg='#000000', fg='#ffffff').grid(row=0, column=3)
        tk.Label(self, width=25, text=f"Notes",  bg='#000000', fg='#ffffff', anchor='w').grid(row=0, column=4)

        for field, value in fields.items():

            if value is None or len(value) == 0:
                continue

            if 'WeaponTxt' in field:
                
                num:int = int(field[9:])
                index = num-1 if num < 35 else num

                match (index % 5):
                    case 0:
                        msg = "weapon"
                        x[num-1] = tk.Button(self, width=25, text=f"{value}", anchor='w',
                                             fg='#000000', bg="#47B35D",
                                             command=lambda weapon=value: weapon_roll(weapon))
                    case 1:
                        msg = "DMG"
                        weapon = str(fields[f"WeaponTxt{num-1}"])
                        x[num-1] = tk.Button(self, width=5, text=f"{value}",
                                             fg='#000000', bg="#47B35D",
                                             command=lambda dmg=str(value), weapon=weapon: damage_roll(dmg, weapon))
                    case 2:
                        msg = "Ammo"
                        x[num-1] = tk.Label(self, width=5, text=f"{value}")
                    case 3:
                        msg = "ROF"
                        x[num-1] = tk.Label(self, width=5, text=f"{value}")
                    case 4:
                        msg = "NOTES"
                        x[num-1] = tk.Label(self, width=25, text=f"{value}", anchor='w')
                                     
                x[num-1].grid(row=1+(index)//5, column=index%5)
            