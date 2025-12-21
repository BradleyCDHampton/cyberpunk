import tkinter as tk
from tkinter import font
from collections import defaultdict

##############################################################################################

colors = {
    "COOL" : "#50AED1",
    "REF" : "#40B338",
    "EMP" : "#C948E2",
    "INT" : "#9F5BFF",
    "DEX" : "#EA7D3A",
    "TECH" : "#B3CE1B",
}

##############################################################################################

class SkillPage(tk.Frame):
    """
        Page for the Skill Checks
        click the button for the skill check to copy the discord command to the clipboard
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.parent = parent

        skills = self.parent.character_sheet["Skills"]
        organizer: defaultdict[str, list[str]] = defaultdict(list[str])

        # Three Columns of Frames each skill Frame will reside in
        sections: list[tk.Frame] = []
        for i in range(3):
            sections.append(tk.Frame(self))
            
            sections[i].pack(side='left')

        for skill_name in skills.keys():
            organizer[skills[skill_name]["STAT"]].append(skill_name)

        stat_frames: dict[str, tk.Frame] = {}

        for stat, skills in organizer.items():
            if len(skills) == 0: # If there are no skills under that stat
                continue

            # Figure out which of the three main columns a stat should go into.
            stat_parent: tk.Frame
            if stat in ["REF","TECH"]:
                stat_parent = sections[0]
            elif stat in ["WILL","EMP","DEX","COOL"]:
                stat_parent = sections[1]
            else:
                stat_parent = sections[2]
               
            stat_frames[stat] = tk.Frame(stat_parent)
            tk.Label(
                stat_frames[stat], text=stat,
                width=25, height=1, bg="#000000", fg="#ffffff"
                ).grid(row=0, column=0, columnspan=2, sticky="ew",
            )

            light_font = font.Font(family='Segoe UI', size=9)
            bold_font = font.Font(family='Segoe UI', size=9, weight='bold')
            # Generate buttons for each of the stat's skills
            i:int = 2

            # Set the Color for the Buttons to the Global Configuration
            if stat in colors.keys():
                color = colors[stat]
            else:
                color = "#B45617"

            for skill_name in skills:
                value = self.parent.character_sheet["Skills"][skill_name]["BASE"]
            
                # Bold font if the BASE is 10 or higher
                my_font = light_font if int(value) < 10 else bold_font

                tk.Button(stat_frames[stat], text=skill_name + f" ({value})", font=my_font,
                          width=25, height=1,
                          command=lambda s=skill_name: self.parent.basic_skill_check(s),
                          bg=color, fg="#0A0228").grid(row=i//2, column=i%2, sticky="ew")
                i+=1
            stat_frames[stat].pack()

        