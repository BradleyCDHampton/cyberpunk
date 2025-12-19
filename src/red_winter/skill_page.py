
import tkinter as tk
import pandas as pd
from tkinter import font
import regex as re
from .utils import basic_skill_check
from collections import defaultdict

class SkillPage(tk.Frame):
    """
        Page for the Skill Checks
        click the button for the skill check to copy the discord command to the clipboard
    """
    def __init__(self, parent, *args, **kwargs):
    
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.pack()

        self.parent = parent

        skills = self.parent.character_sheet["Skills"]
        organizer: defaultdict[str, list[str]] = defaultdict(list[str])

        for skill_name in skills.keys():
            organizer[skills[skill_name]["STAT"]].append(skill_name)

        cols=4
        i = 0
        for stat, skills in organizer.items():
            if len(skills) == 0: # If there are no skills under that stat
                continue
            tk.Label(self, text=stat).grid(row=i//cols, column=0, columnspan=cols, sticky="ew")
            i += cols
            
            light_font = font.Font(family='Segoe UI', size=9)
            # Generate buttons for each of the stat's skills
            for skill_name in skills:
                value = self.parent.character_sheet["Skills"][skill_name]["BASE"]
                tk.Button(self, text=skill_name + f" ({value})", font=light_font,
                          command=lambda v=value, s=skill_name: basic_skill_check(v, s),
                          bg='#B45617', fg="#0A0228").grid(row=i//cols, column=i%cols, sticky="ew")
                i+=1
            i = (i + cols - 1)//cols * cols 