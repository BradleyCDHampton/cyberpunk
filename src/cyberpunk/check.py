
import numpy as np

class Check:
    """
        A skill check for a TTRPG, specifically with the rules of Cyberpunk Red in mind.

            dv:int The DV for the skill check, that must be beaten
            rolls:list A list of tensors, that represent all possible values that can come from a die.
            ties_count:bool Indicates whether a roll result equal to the DV counts as passing
    """

    def __init__(self, rolls:list, dv:int=0, ties_count:bool=False):
        
        self._dv = dv
        self._rolls = rolls
        self._ties_count = ties_count

        # Computed/cached as needed, not needed at this time.
        self._n = None
        self._success_chance = None
        self._roll_results = None

        self._accuracy = 1.0 #TODO
        
    @property
    def success_chance(self) -> float:
        '''Returns the percentage chance that the skill check will pass.'''
        if self._success_chance is None:
            pass_chance = 0.0
            for roll_result, odds in zip(*self.roll_results):
                if roll_result >= self.roll_needed_to_beat():
                    pass_chance += odds
            self._success_chance = pass_chance
        
        return self._success_chance
    
    @property
    def dv(self) -> int:
        return self._dv
    
    @dv.setter
    def dv(self, new_value:int) -> None:
        self._dv = new_value
        self._clear_rolls()

    @property
    def ties_count(self) -> bool:
        return self._ties_count
    
    @ties_count.setter
    def ties_count(self, new_value:bool) -> None:
        self._ties_count = new_value
        self._clear_rolls()

    @property
    def rolls(self) -> list[np.ndarray]:
        return self._rolls

    @rolls.setter
    def rolls(self, new_value) -> None:
        '''...'''
        self._rolls = new_value
        self._clear_rolls()

    @property
    def roll_results(self) -> tuple[np.ndarray, np.ndarray]:
        '''...'''
        if self._roll_results is None:
            self.compute_rolls()
        assert isinstance(self._roll_results, tuple)
        return self._roll_results
    
    @roll_results.setter
    def roll_results(self, new_value):
        self._roll_results = new_value
        self._success_chance = None
    
    @property
    def size(self) -> int:
        '''Returns the number of unique possible rolls for this particular check.'''
        if self._rolls is None:
            self.compute_rolls()
        assert isinstance(self._n, int)
        return self._n

    def _clear_rolls(self) -> None:
        '''Clears the cache for success_chance and roll_results.'''
        self._success_chance = None
        self._roll_results = None
        self._n = None

    def roll_needed_to_beat(self) -> int:
        '''Returns the value that is effectively needed to pass the Check, by adding 1 if ties fail.'''
        if self.ties_count:
            return self.dv
        return self.dv+1

    def compute_rolls(self) -> None:
        '''...'''
        possibilities = np.array(0)

        for roll in self.rolls:
            possibilities = np.add.outer(possibilities, roll)

        n = possibilities.size

        dmg, counts = np.unique(possibilities, return_counts=True)
        odds = counts / n

        self._roll_results = (dmg, odds)
        self._n = n

    def apply_accuracy(self, hit_chance:float):
        'Returns a version of roll_results, accounting a chance to hit.'

        miss_chance = 1.0 - hit_chance

        dmg, odds = self.roll_results
        odds *= hit_chance

        #if dmg[0] != 0

        odds[0] += miss_chance

        self.roll_results = (dmg, odds)
    
    def full_stats(self, key_values=None, use_thresholds=True, thresholds=None) -> str:
        """
        
        
        """
        key_values = key_values or []
        thresholds = thresholds or [.01, .05, .1, .25, .33, .5, .66, .75, .9, .95, .99]

        output = []
        output.append(f"DV  : {self.dv}")
        output.append(f"FAIL  {100.0 - 100*self.success_chance:.2f}%")

        running_odds = 1.0
        for roll_result, odds in zip(*self.roll_results):

            meets_threshold = (not use_thresholds) or (thresholds and running_odds <= thresholds[-1])
            beats_dv = roll_result >= self.roll_needed_to_beat()

            if (roll_result in key_values or (beats_dv and meets_threshold)):
                output.append(f"{roll_result:>4}  {100*running_odds:.2f}%")
            
            while thresholds and running_odds <= thresholds[-1]:
                thresholds.pop()

            running_odds -= odds
            if not thresholds:
                break

        return "\n".join(output)    

    def simple_stats(self) -> str:
        return (
            f"DV  : {self.dv}\n"
            f"PASS: {100*self.success_chance:.2f}% | "
            f"FAIL: {100*(1.0-self.success_chance):.2f}%\n"
        )

    def __str__(self):
        return self.simple_stats()


