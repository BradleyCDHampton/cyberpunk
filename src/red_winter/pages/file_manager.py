import tkinter as tk
from tkinter import filedialog

from ..character_sheet import save_character_sheet

class FilePage(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        tk.Button(self,
                  text="Save",
                  command=self.save).pack()
        tk.Button(self, text="Load",
                  command=self.load).pack()

    def load(self): #TODO needs a try/catch 
        """
        Docstring for load_new
        
        :param self: Description
        """
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Pdfs", "*.pdf"), ]
        )
        if file_path:
            self.parent.character_sheet_link = file_path
            self.parent.refresh()

    def save(self):
        """
        Docstring for save
        
        :param self: Description
        """
        save_character_sheet(self.parent.character_sheet, self.parent.character_sheet_link)
        self.parent.clipboard_echo.config(text="File saved!")
        
        

