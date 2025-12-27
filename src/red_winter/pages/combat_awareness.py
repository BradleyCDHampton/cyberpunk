import tkinter as tk
from ..modifier import Modifier
from typing import TypedDict

class ModifierWidgets(TypedDict):
    Name: tk.Label
    Downtick: tk.Button
    Uptick: tk.Button
    Points: tk.Label
    Notes: tk.Label

class CombatAwareness():

    def __init__(self):

        self.combat_awareness_max_points:int = 4
        self.combat_awareness_available_points:int  = 4

        self.combat_awareness_abilities: dict[str, tuple[str,int,int]] = {
            #ability_name, (affects, cost_per_level, max_level)
            "Damage Deflection" : ('',2,5),
            'Fumble Recovery' : ('',4,1),
            'Initiative Reaction' : ('Initiative',1,10),
            'Precision Attack' : ('Attack',3,3),
            'Spot Weakness' : ('Damage',1,10),
            'Threat Detection' : ('Perception',1,10)
        }

        self.ability_points: dict[str, int] = {}
        for ability in self.combat_awareness_abilities.keys():
            self.ability_points[ability] = 0


    def update_points(self, ability_name:str, delta:int) -> None:
        """
        Docstring for update_points
        
        :param ability_name: Description
        :param delta: Description
        """
        _, cost, max = self.combat_awareness_abilities[ability_name]
        current_points = self.ability_points[ability_name]

        if (0 <= delta + current_points <= max and
            delta*cost <= self.combat_awareness_available_points):
            
            self.combat_awareness_available_points -= (delta*cost)
            self.ability_points[ability_name] += delta

        #print(f"{self.combat_awareness_available_points} Available.")

    def get_modifier(self) -> Modifier:
        """
        Docstring for get_modifier
        
        Returns:
            Modifier
        """
        result = Modifier()

        for ability_name in self.combat_awareness_abilities.keys():
            affects: str = self.combat_awareness_abilities[ability_name][0]
            points: int = self.ability_points[ability_name]
            if affects != '' and points > 0:
                result += Modifier(ability_name, [(affects, points)])

        return result


class CombatAwarenessPage(tk.Frame, CombatAwareness):
    """
    Manages the UI elements for Combat Awareness
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        CombatAwareness.__init__(self)
        self.parent = parent

        self.combat_awareness_max_points = int(self.parent.character_sheet["Role"]["RoleRank"])
        self.combat_awareness_available_points = self.combat_awareness_max_points

        self.available_points_ui = tk.Label(self, width=60)
        self.available_points_ui.pack()

        my_frame = tk.Frame(self, width=50, bg='black')
        tk.Label(my_frame, text="Ability", bg='black', fg='white', width=20).pack(side='left')
        tk.Label(my_frame, text="Points", bg='black', fg='white', width=10).pack(side='left')
        tk.Label(my_frame, text="Effect", bg='black', fg='white', width=30).pack(side='left')
        
        my_frame.pack()

        self.modifier_ui: dict[str, ModifierWidgets] = self.create_modifier_fields(self.combat_awareness_abilities)   

        self.refresh_ui()
        
    def refresh_ui(self):
        """
        Refreshes the UI to display the current values.
        
        :param self: Description
        """
        self.available_points_ui.configure(text=f"Available Combat Awareness Points: {self.combat_awareness_available_points}/{self.combat_awareness_max_points}")
        #update combat awareness

        for ability_name, ability_widgets in self.modifier_ui.items():
            points:int = self.ability_points[ability_name]
            ability_widgets["Points"].configure(text=str(points))
            
            note = '' if points == 0 else f'+{points} to {self.combat_awareness_abilities[ability_name][0]}'
            ability_widgets["Notes"].configure(text=note)

    def update_points(self, ability_name:str, delta:int) -> None:
        """
        Docstring for update_points

        :param ability_name: Description
        :param delta: Description
        """
        super().update_points(ability_name, delta)
        self.refresh_ui()

    def create_modifier_fields(self, modifier_fields: dict[str, tuple[str,int,int]]) -> dict[str, ModifierWidgets]:
        """
        Creates the set of fields where a user can input their modifiers that cannot be determined 
        at initialization (fluctuates during play)

        :param modifier_fields: The names of the fields, and also what the text label will be
        
        Returns:
            A dictionary of the names of each field, mapped to its entry box.
        """
        result: dict[str, ModifierWidgets] = {}

        for modifier_name, (_,cost,max) in modifier_fields.items():
            modifier_frame = tk.Frame(self, width=60)

            entry: ModifierWidgets = {
                "Name" : tk.Label(modifier_frame, text=modifier_name, width=20, anchor='w'),
                "Downtick" : tk.Button(modifier_frame, text="-", width=3, anchor='w',bg="#ea92e1",
                      command=lambda modifier_name=modifier_name: self.update_points(modifier_name, -1)),
                "Uptick" : tk.Button(modifier_frame, text="+", width=3, anchor='w',bg="#91dfc6",
                      command=lambda modifier_name=modifier_name: self.update_points(modifier_name, 1)),
                "Points" : tk.Label(modifier_frame, text=0, width=4),
                "Notes" : tk.Label(modifier_frame, text=0, width=30, anchor='w')
            }

            # Render
            entry["Name"].pack(side='left')
            entry["Downtick"].pack(side='left')
            entry["Points"].pack(side='left')
            entry["Uptick"].pack(side='left')
            entry["Notes"].pack(side='left')

            result[modifier_name] = entry

            modifier_frame.pack()

        return result
    
