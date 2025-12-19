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


# Critical Injuries
# Drugs no Addiction
# Drugs w/ Addition



# Weapon-Mods... do this later?

# some field for additional modifiers
