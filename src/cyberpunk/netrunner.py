from cyberpunk.dice import roll_dice
from cyberpunk.black_ice import BlackIce
from cyberpunk.check import Check
from cyberpunk.program import Program

class Netrunner:

    def __init__(self, name, hp:int=-1, interface:int=-1, programs=None):
        self._id = name
        
        try:
            import pandas as pd
            netrunners = pd.read_json(r"data\netrunners.json")

            if name in netrunners.name:
                self._hp = hp if hp > 0 else int(netrunners.hp.values[0])
                self._interface = interface if interface > 0 else int(netrunners.interface.values[0])
                self._programs = self._programs or self._validate_programs(programs)

        except:
            self._hp = hp if hp > 0 else 20
            self._interface = interface if interface > 0 else 4
            self._programs = self._programs or self._validate_programs(programs)
            
    @property
    def id(self):
        '''Returns the id of the netrunner'''
        return self._id
    
    @id.setter
    def id(self, id):
        '''Sets a new id value for a Netrunner'''
        self._id = id

    @property
    def hp(self):
        '''Returns the current hp value of a Netrunner'''
        return self._hp
    
    @hp.setter
    def hp(self, new_value):
        '''Sets the new hp value for a Netrunner'''
        self._hp = new_value

    @property
    def interface(self):
        '''Returns a 10x10 matrix containing all possible interface rolls.'''
        return roll_dice(dice=[-10], modifiers=[self._interface])

    @interface.setter
    def interface(self, new_value):
        '''New setter for an interface modifier'''
        self._interface = new_value

    def _net_contested_check(self, my_modifiers:list, encounter_modifiers:list):
        '''Creates a simple contested Check, where only a single d10 and modifiers are considered.'''
        my_roll = roll_dice(dice=[-10], modifiers=my_modifiers)
        encounter_roll = roll_dice(dice=[10], modifiers=encounter_modifiers) * -1

        my_check = Check(rolls=[my_roll, encounter_roll])
        return my_check
    
    def _validate_programs(self, programs):
        if programs is None:
            return []
        valid_programs = []

        import pandas as pd
        black_ice = pd.read_csv(r"data\black_ice.csv")
        programs = pd.read_csv(r"data\programs.csv")
        combined = pd.concat([black_ice, programs])

        for program in programs:
            if program in combined["name"].values:
                valid_programs.append(program)

        return valid_programs


    def compute_modifier(self, target_program:str, bonus:int) -> int:
        modifier = 0
        for program in self._programs:
            if program == target_program:
                modifier += bonus
        return modifier


    def net_outspeed(self, black_ice:BlackIce):
        '''Creates a Check to track the odds for a Netrunner to avoid a preemptive strike from Black ICE'''
        bonus_modifier = self.compute_modifier("Speedy Gonzales", 2)
        return self._net_contested_check([self.interface], [black_ice.speed, bonus_modifier])

    def net_slide(self, black_ice:BlackIce):
        '''Creates a Check to track the odds of a Netrunner Sliding from Black ICE'''
        return self._net_contested_check([self.interface], [black_ice.perception])

    def net_attack(self, black_ice:BlackIce, program=None):
        '''Returns a ndmatrix of probabilities for the damage that might be dealt'''

        damage:Check
        accuracy:Check

        if isinstance(program, Program):
            accuracy = self._net_contested_check([self.interface, program.attack], [black_ice.defense])
            damage = Check(rolls=[6]*program.dice)
        else:
            accuracy = self._net_contested_check([self.interface], [black_ice.defense])
            damage = Check(rolls=[6])
            
        damage.apply_accuracy(accuracy.success_chance)
        return damage
        
        
    def net_defend(self, program:Program):
        '''Creates a Check for the damage taken from the black ice'''

        bonus_modifier = self.compute_modifier("Armor", 4)

        accuracy = self._net_contested_check([program.attack], [self.interface])
        damage = Check(rolls=[6]*program.dice, dv=bonus_modifier)
        damage.apply_accuracy(accuracy.success_chance)
        return damage







        
        attack_roll = black_ice.roll

        my_modifiers = [self.interface, bonus_modifier]
        defense_roll = roll_dice(dice=[-10], modifiers=my_modifiers) * -1

        my_check = Check(rolls=[attack_roll, defense_roll])
        return my_check
    
    
    def pathfinder(self):
        pass
    
    
    def backdoor(self):
        pass

    def __str__(self):
        my_netrunner = { 
            "name": self.id,
            "hp": self.hp,
            "interface": self._interface,
            "programs": {}
        }
        return str(my_netrunner)
    
    def add_program(self, program_name:str):
        pass

    def remove_program(self, program_name:str):
        pass

    def save(self, id=None):
        '''Saves a netrunner if an id is specified'''

        id = id or self.id

        if id==None:
            print("No id for Netrunner, save failed.")
        else:
            import pandas as pd
            my_netrunner = { 
                "hp": self.hp,
                "interface": self._interface,
                "programs": []
            }
            try:
                netrunners = pd.read_json(r"data\netrunners.json")
                netrunners.loc[id] = my_netrunner
            except:
                print("No JSON found, generating new file...")
                netrunners = pd.DataFrame.from_dict({id : my_netrunner}, orient='index')

            netrunners.to_json(r"data\netrunners.json")

