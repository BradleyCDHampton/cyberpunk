
from collections import defaultdict
from copy import deepcopy
from typing import Self

class Modifier:
    """Represents a collection of affects for a single Modifier.

    Each Modifier stores effects as key-value pairs, where the key is the
    affected skill/stat/check and magnitude of the modification.

    Attributes:
        data (dict[str, int]): The internal dictionary storing modifiers.
    """

    def __init__(self, modifier_name="", modifier_list=None, ignore_list=None):
        """Creates a new Modifier object
        
        :param modifier_name: The name of the modifier
        :param modifier_list: Optional. If not provided, represents an empty modifier list. 
            If provided a list of tuples e.g. [("Archery", 1), ("Brawling",-2)]
            represents effects of the modifier
        """
        self.modifier_list: list[str] = [modifier_name]
        
        if ignore_list is None:
            ignore_list = []

        self.ignore_list = ignore_list
        self.data: defaultdict[str, list[tuple[str, int]]] = defaultdict(list)

        if modifier_list is not None:
            for affects, magnitude in modifier_list:
                self.data[affects].append((modifier_name, magnitude))

    
    def __add__(self, other_modifier: object) -> Self:
        """
        Adds two Modifiers together to create a new Modifier.

        :param other_modifier: 

        Returns:
            A new Modifier object, which is a key-by-key appendation of self and other
        """
        if isinstance(other_modifier, Modifier):
            assert(isinstance(other_modifier, Modifier))
            result: Modifier = deepcopy(self)

            for affects, magnitude in other_modifier.data.items():
                result.data[affects] += magnitude
                
            result.modifier_list += other_modifier.modifier_list
            result.ignore_list += other_modifier.ignore_list
            return result
        
        return NotImplemented
    

    def __str__(self) -> str:
        """Returns: a string with each affect: magnitude on separate lines."""
        mods = []

        for affect, magnitude in self.data.items():
            mods.append(f"{affect}: {magnitude}")

        return "\n".join(mods)
    

    def get_affect(self, affect: str) -> tuple[str, str]:
        """
        Generates the strings for a Modifier
        
        :param affect: The skill/stat/action that is being looked up.

        Returns:
            A tuple of two strings. The first being a string concatenation of all
            relevant modifiers. The second being a concatenation of the "reasons" for
            each modifier.

            If a particular affect is meant to be ignored by the modifier, it is not
            included in the calculation or output.
        """
        nums: list[str] = []
        reasons: list[str] = []

        for reason, num in self.data[affect]:
            if reason not in self.ignore_list:
                if num >= 0:
                    nums.append(f"+{num}")
                else:
                    nums.append(f"{num}")
                reasons.append(reason)
                
        return "".join(nums), ", ".join(reasons)    