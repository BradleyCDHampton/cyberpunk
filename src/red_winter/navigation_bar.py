import tkinter as tk

class NavigationBar(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        def switch_tab_to(new_tab):
            for tab in self.parent.pages.values():
                tab.pack_forget()
            new_tab.pack()

        i = 0
        for page_name, frame in self.parent.pages.items():
            tk.Button(self, text=page_name,
                      command=lambda f=frame: switch_tab_to(f)).grid(row=0, column=i)
            i += 1