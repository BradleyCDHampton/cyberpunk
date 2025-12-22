import tkinter as tk

from .main_app import MainApplication

#######################################################################################################

character_sheet_link = r"data/Solo_Crux.pdf"

#######################################################################################################

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root, character_sheet_link).pack(side="top", fill="both", expand=True)
    root.title("Red WINTER App")
    root.mainloop()

"""



Flaws:
    * Certain Drugs/effects cannot lower MOVE to 0 or a STAT above 8

    *   potential solution: add "rules" to JSON to communicate this info e.g. "if MOVE above 8, ignore'
    *   ...sequencing of that

    * Things like Wheelhaus apply additional debuffs depending on the situation
        potential solution... have more buttons.
    * Consider: make a Check data structure that looks at all the Modifiers+base stats & enforce rules about min/maxes w/ optimal sequencing

TODO:
    * make weapons follow the same modifier system
    * do a check for weapons that can do aimed shots/autofire/etc.

"""

# Critical Injuries
# Drugs no Addiction
# Drugs w/ Addition



# Weapon-Mods... do this later?

# some field for additional modifiers
