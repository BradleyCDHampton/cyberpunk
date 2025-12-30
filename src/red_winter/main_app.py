
import tkinter as tk
from tkinter import filedialog
import clipboard

from .pages.skill_page import SkillPage
from .pages.weapon_page import WeaponPage
from .navigation_bar import NavigationBar
from .modifier import Modifier
from .pages.drug_page import DrugPage
from .pages.injury_page import InjuryPage
from .pages.cyberware_page import CyberwarePage
from .pages.combat_awareness import CombatAwarenessPage
from .file_manager import FilePage

from .character_sheet import load_character_sheet, save_character_sheet


class MainApplication(tk.Frame):

    def __init__(self, parent, character_sheet_link, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Initialize Character Sheet
        self.character_sheet_link = character_sheet_link
        self.character_sheet = load_character_sheet(self.character_sheet_link)
        save_character_sheet(self.character_sheet)

        self.pages = {}

        #self.pages["Load"] = tk.Button(self, text="Load")
        self.pages["Skills"] = SkillPage(self)
        self.pages["Weapons"] = WeaponPage(self)
        self.pages["Drugs"] = DrugPage(self)
        self.pages["Injuries"] = InjuryPage(self)
        self.pages["Cyberware"] = CyberwarePage(self)
        self.pages["Combat Awareness"] = CombatAwarenessPage(self)

        self.navigation = NavigationBar(self)
        self.clipboard_echo = tk.Label(self, text='')

        self.pages["Skills"].pack()

        tk.Button(self.navigation, text="Load", command=self.load_new).grid(row=0, column=6)
        self.navigation.pack(side='bottom')

    def load_new(self): #TODO needs a try/catch 
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Pdfs", "*.pdf"), ]
        )
        if file_path:
            for page in self.pages.values():
                page.pack_forget()
            self.navigation.pack_forget()

            self.character_sheet_link = file_path
            self.character_sheet = load_character_sheet(self.character_sheet_link)

            self.pages["Skills"] = SkillPage(self)
            self.pages["Weapons"] = WeaponPage(self)
            self.pages["Drugs"] = DrugPage(self)
            self.pages["Injuries"] = InjuryPage(self)
            self.navigation = NavigationBar(self)

            self.pages["Skills"].pack()
            self.navigation.pack(side='bottom')
            tk.Button(self.navigation, text="Load", command=self.load_new).grid(row=0, column=5)

    def update_clipboard(self, discord_command: str) -> None:
        """
        Writes a discord command to the clipboard, and shows the
        command that was copied to the clipboard at the bottom of the window.
        
        :param discord_command: The command to be copied/output
        """
        clipboard.copy(discord_command)
        self.clipboard_echo.config(text=discord_command)
        self.clipboard_echo.pack(side='bottom', after=self.navigation)

   
    def basic_skill_check(self, skill_name) -> None:
        """
        Copies the Discord command for a particular skill check to the clipboard.
        
        :param skill_name: The skill/action we are checking
        """
        stat_name = self.character_sheet["Skills"][skill_name]["STAT"]
        drug_modifier = self.pages["Drugs"].get_active_effects()
        injury_modifier = self.pages["Injuries"].get_active_effects()
        cyberware_modifier = self.pages["Cyberware"].get_active_effects()
        combat_awareness_modifier = self.pages["Combat Awareness"].get_modifier()

        modifier = drug_modifier + injury_modifier + cyberware_modifier + combat_awareness_modifier

        magnitude_list: list[str] = []
        reason_list: list[str] = []

        relevant = [skill_name, stat_name, "All Actions"]

        for affect in relevant:
            curr_mag, curr_reason = modifier.get_affect(affect)
            magnitude_list.append(curr_mag)
            reason_list.append(curr_reason)

        magnitudes: str = "".join(magnitude_list)

        reason_list = [r for r in reason_list if r != ""]
        reasons: str = ",".join(reason_list)        
        

        level: int = int(self.character_sheet["Skills"][skill_name]["BASE"])
        mod: str = self.character_sheet["Skills"][skill_name]["MOD"]
        if mod is not None and mod != '':
            level -= int(mod)

        if len(reasons) > 0:
            reasons = ' (' + reasons + ')'

        discord_command = f"!r 1d10+{level}{magnitudes} {skill_name}{reasons}"
        self.update_clipboard(discord_command)






        


   