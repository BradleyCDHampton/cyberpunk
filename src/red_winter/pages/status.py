import tkinter as tk
from ..modifier import Modifier
from typing import TypedDict


class StatusPage(tk.Frame):
    """
    Manages the UI elements for Combat Awareness
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.create_entry("Current HP", self.parent.character_sheet['Derived Stats'], 'HPcurr')
        self.create_entry("SP Head", self.parent.character_sheet['Armor'], 'SPHead')
        self.create_entry("SP Head", self.parent.character_sheet['Armor'], 'SPBody')


    def create_entry(self, label:str, dictionary:dict, status_key:str) -> None:
        """
        Docstring for create_entry
        
        :param label: Description
        :param dictionary: Description
        :param status_key: Description
        """
        frame = tk.Frame(self, width=50)

        initial_value = dictionary[status_key]
        tk.Label(frame, text=label, width=20).pack(side='left')

        def on_change(*args):
            dictionary[status_key] = var.get()

        var = tk.IntVar(value=int(initial_value))
        var.trace_add("write", on_change)

        current_hp_entry = tk.Entry(frame, textvariable=var)
        current_hp_entry.pack(side='left')

        frame.pack()




    
