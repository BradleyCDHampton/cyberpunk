
import tkinter as tk
import pandas as pd
from tkinter import font
import regex as re
from .utils import basic_skill_check

class SkillPage(tk.Frame):
    """
        Page for the Skill Checks
        click the button for the skill check to copy the discord command to the clipboard
    """
    def __init__(self, parent, *args, **kwargs):
    
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.pack()

        self.parent = parent

        x = self.parent.character_sheet_data["Skills"]

        fields = self.parent.fields

        skill_df = pd.read_csv(r"data\skills.csv")
        mappings = pd.read_csv(r"data\mappings.csv")

        organizer = {"INT" : [], "REF" : [], "DEX" : [], "TECH" : [],
                     "COOL" : [], "WILL" : [], "EMP" : [], "UNK" : []}

        for field_name, value in x.keys():
            skill_name:str = field_name

            # Case 1: Particular Skill has a defined mapping.
            if field_name in list(mappings["Field"]):
                skill_name = mappings.loc[mappings["Field"] == skill_name, "Canon"].iloc[0]
                bucket = self.determine_bucket(skill_name, skill_df)

            # Case 2: It is a fill-in-the-blank "named" skill
            elif ("BASE" in field_name and field_name[-1].isnumeric() and int(value) > 0):

                variant_1 = "Txt_"+field_name[5:]
                variant_2 = field_name[5:]

                bucket = self.determine_bucket(field_name[5:-1], skill_df)

                if variant_1 in fields and fields[variant_1] is not None:
                    skill_name = fields[variant_1]
                elif variant_2 in fields and fields[variant_2] is not None:
                    skill_name = fields[variant_2]
                else:
                    continue

            # Case 3: It is an "ordinary" skill, with a fixed name.
            elif "BASE" in field_name and not field_name[-1].isnumeric():
                skill_name = field_name.split()[-1]
                pattern = re.compile(r"[A-Z][a-z]*")
                variant_1 = re.findall(pattern, skill_name)
                skill_name = " ".join(variant_1)

                bucket = self.determine_bucket(skill_name, skill_df)
            else:
                continue
            organizer[bucket].append((skill_name, value))

        cols=4
        i = 0
        for stat, skills in organizer.items():
            if len(skills) == 0: # If there are no skills under that stat
                continue
            tk.Label(self, text=stat).grid(row=i//cols, column=0, columnspan=cols, sticky="ew")
            i += cols
            
            light_font = font.Font(family='Segoe UI', size=9)
            # Generate buttons for each of the stat's skills
            for (skill_name, value) in skills:
                tk.Button(self, text=skill_name + f" ({value})", font=light_font,
                          command=lambda v=value, s=skill_name: basic_skill_check(v, s),
                          bg='#B45617', fg="#0A0228").grid(row=i//cols, column=i%cols, sticky="ew")
                i+=1
            i = (i + cols - 1)//cols * cols 

    
    def determine_bucket(self, skill_name: str, df: pd.DataFrame) -> str:
        bucket = "UNK"
        if skill_name in list(df["SkillName"]):
            bucket = df.loc[df["SkillName"] == skill_name, "AlignedStat"].iloc[0]
            bucket = bucket.strip()
        else:
            print(f"{skill_name} was not found :()")
        return bucket