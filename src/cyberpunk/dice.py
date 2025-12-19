import numpy as np

def roll_dice(dice:list, modifiers:list):
    """
    Computes a tensor of all possible dice roll results, including a modifier.

        dice: a list of dice, where the magnitude is the number of faces (e.g. a d10)
              the sign indicates whether it can crit (negative dice crit)
        modifier: a list of all modifiers that may impact the roll
    """
    possibilities = np.array(0)
    
    for die in dice:
        can_crit = False
        if die < 0:
            can_crit = True
            die = abs(die)

        base = np.arange(start=1,stop=die+1)
        roll = base.copy() 

        if can_crit:
            fumble_mask = (base == 1).astype(int)
            critical_mask = (base == die).astype(int)
            mask = critical_mask - fumble_mask
            mask = mask[:, np.newaxis] 
            criticals = mask[:, np.newaxis] * base
            criticals = criticals.reshape(criticals.shape[0], criticals.shape[2])
            criticals = np.transpose(criticals)
            roll = roll+criticals

        possibilities = np.add.outer(roll, possibilities)
    possibilities += sum(modifiers)
    
    return possibilities

def output_dice_tensor(rolls):
    '''Outputs a matrix of all possible rolls, or the shape of the tensor if more than 2d.'''

    if len(rolls.shape) <= 2:
        print("Possible Rolls:")
        print(rolls)
    else:
        print(f"rolls.shape: {rolls.shape}")