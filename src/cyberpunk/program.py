
from cyberpunk.dice import roll_dice
from collections import defaultdict
from enum import Enum
import re

class ProgramType(Enum):
    ANTI_PERSONNEL = "Anti-Personnel"
    ANTI_PROGRAM = "Anti-Program"
    BOOSTER = "Booster"
    DEFENDER = "Defender"
    UNKNOWN = "ERROR: Unknown"

class Program:
    def __init__(self, name:str):
        import pandas as pd
        program = pd.read_csv(r"data\programs.csv")
        black_ice = pd.read_csv(r"data\black_ice.csv")
        program = pd.concat([program, black_ice])

        program = program.loc[program['name']==name]
        
        self._name = name
        
        self._roll = int(program.attack.values[0])
        self._defense = int(program.defense.values[0])
        self._rez = int(program.rez.values[0])
        self._effect = str(program.effect.values[0])
        self._augment = self._apply_augments(str(program.augment.values[0]))

        self._program_type = self.parse_class(str(program["class"].values[0]))
        self._attack
        self._dice = program.dice.values[0]

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_value:str):
        self._name = new_value

    @property
    def roll(self):
        '''Generates all possible attacks from a Black Ice'''
        dice = str(self._dice).split("d")
        roll = [int(dice[1])] * int(dice[0])
    
        return roll_dice(dice=roll, modifiers=[self._roll])
    
    @roll.setter
    def roll(self, new_value):
        self._roll = new_value

    @property
    def attack(self):
        '''Generates all possible rolls from a Program'''
        return self._attack
    
    @attack.setter
    def attack(self, new_value):
        self._attack = new_value

    @property
    def defense(self):
        return self._defense
    
    @defense.setter
    def defense(self, new_value):
        self._defense = new_value
    
    @property
    def hp(self):
        return self._rez
    
    @hp.setter
    def hp(self, new_value):
        self._rez = new_value

    @property
    def rez(self):
        return self._rez
    
    @rez.setter
    def rez(self, new_value):
        self._rez = new_value

    @property
    def effect(self):
        return self._effect
    
    @effect.setter
    def effect(self, new_value):
        self._effect = new_value

    @property
    def dice(self):
        return self._dice
    
    @dice.setter
    def dice(self, new_value):
        self._dice = new_value

    @property
    def program_type(self):
        return self._program_type
    
    @program_type.setter
    def program_type(self, attacker_class:str):
        self._program_type = self.parse_class(attacker_class)

    @property
    def augments(self):
        return self._augments

    @augments.setter
    def augments(self, new_value:str):
        self._augments = self._apply_augments(new_value)

    def __str__(self):
        return (
            f"{self.name} - {self.program_type.value}, {self._roll} + {self.dice}\n"
            "ATK DEF REZ\n"
            f"{self._roll:^3} "
            f"{self.defense:^3} "
            f"{self.rez:^3}\n"
        )

    def _apply_augments(self, augments:str):
        my_augments = augments.split(" ")
        applied_augments = defaultdict(int)

        for augment in my_augments:
            stat = re.sub(r"\d", "", augment)
            value = int(re.sub(r"[a-zA-Z]", "", augment))
            applied_augments[stat] = value

        return applied_augments


    def parse_class(self, class_label:str):
        class_label = class_label.strip()
        if class_label.startswith("Anti-Personnel"):
            return ProgramType.ANTI_PERSONNEL
        elif class_label.startswith("Anti-Program"):
            return ProgramType.ANTI_PROGRAM
        elif class_label.startswith("Booster"):
            return ProgramType.BOOSTER
        elif class_label.startswith("Defender"):
            return ProgramType.DEFENDER
        else:
            print("Issue w/ class label")
            print(class_label)
            return ProgramType.UNKNOWN




    





