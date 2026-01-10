import tkinter as tk

class NavigationBar(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.refresh()

    def refresh(self):
        i = 0
        for page_name, frame in self.parent.pages.items():
            tk.Button(self, text=page_name,
                      bg="#7d0a76", fg='#ffffff',
                      command=lambda f=frame: self.switch_tab_to(f)).grid(row=0, column=i)
            i += 1

    def switch_tab_to(self, new_tab):
        for tab in self.parent.pages.values():
            tab.pack_forget()
        new_tab.pack()