from cyberpunk.program import Program

class BlackIce(Program):
    def __init__(self, name:str):
        super().__init__(name)

        import pandas as pd
        black_ice = pd.read_csv(r"data\black_ice.csv")
        black_ice = black_ice.loc[black_ice['name']==name]

        self._perception = int(black_ice.perception.values[0])
        self._speed = int(black_ice.speed.values[0])

    @property
    def perception(self):
        return self._perception
    
    @perception.setter
    def perception(self, new_value):
        self._perception = new_value

    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, new_value):
        self._speed = new_value
    
    
    def __str__(self):
        
        return (
            f"{self.name} - {self.program_type.value}, {self._roll} + {self.dice}\n"
            "PER SPD ATK DEF REZ\n"
            f"{self.perception:^3} "
            f"{self.speed:^3} "
            f"{self._roll:^3} "
            f"{self.defense:^3} "
            f"{self.rez:^3}\n"
        )





    





