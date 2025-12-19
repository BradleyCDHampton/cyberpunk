
from collections import defaultdict, Counter
import numpy as np
from cyberpunk.dice import roll_dice, output_dice_tensor
from cyberpunk.netrunner import Netrunner

def output_check_success_odds(possibilities, DV=0, msgs=None):
    '''Output the odds that a check will suceed'''

    if msgs is None:
        msgs = []

    msgs = [f"DV: {DV}"] + msgs

    chance, chance_with_ties = calculate_check_odds(possibilities, DV)

    print(", ".join(msgs))
    #print(f"Passes: {passes}\tFailures:{failures}\t Ties: {ties}")
    print(f"Chance of Success: {chance:.2%}")
    print(f"Chance of Success w/ Ties: {chance_with_ties:.2%}")


def calculate_check_odds(possibilities:np.ndarray, DV:int=0):

    passes = np.count_nonzero(possibilities > DV)
    ties = np.count_nonzero(possibilities == 0)
    failures = np.count_nonzero(possibilities < DV)

    chance = passes / (passes+failures+ties)
    chance_with_ties = (passes+ties)/(passes+failures+ties)

    return chance, chance_with_ties

def roll_against_opponent_and_DV(DV:int, rolls:list):
    
    possibilities = np.array(0)

    for roll in rolls:
        possibilities = np.add.outer(possibilities, roll)

    output_dice_tensor(possibilities)
    output_check_success_odds(possibilities, DV)


def calculate_DV_pass(DV:int, dice:list, modifiers:list):
    rolls = roll_dice(dice, modifiers)

    output_dice_tensor(rolls)
    output_check_success_odds(rolls, DV)


def takedown_odds(attacks:list, DEF=-1, REZ=-1, netrunner=None):

    existing_probabilities = defaultdict(float)
    existing_probabilities[0] = 1.0

    for attack in attacks:
        if netrunner is not None and type(netrunner) == Netrunner:
            #attack = np.add.outer(attack, netrunner.net_defend()*-1)
            REZ = netrunner.hp
        elif type(DEF) == np.ndarray:
            DEF[DEF<0] = 0
            attack = np.add.outer(attack, DEF*-1)
        elif type(DEF) == int:
            attack -= DEF
        else:
            print("couldn't determine how to calc...")

        attack = attack.flatten()
        attack[attack < 0] = 0

        attack_matrix_size = len(attack)

        # Store the attack values in a new default dict
        damage_counts = Counter(attack)
        curr_probabilities = defaultdict(float)

        # Generate probabilities of recieving each damage value
        for dmg, times in damage_counts.items():
            curr_probabilities[dmg] = times/attack_matrix_size

        # Joint probability calculation
        joint_probabilities = defaultdict(float)
        for existing, probability_of_existing in existing_probabilities.items():
            for current, probability_of_current in curr_probabilities.items():
                joint_probabilities[existing + current] += (probability_of_existing * probability_of_current)

        existing_probabilities = joint_probabilities

    cumulative_odds = 0.0

    thresholds = [.99, .95, .9, .75, .66, .5, .33, .25, .1, .05, .01]
    for roll, odds in sorted(existing_probabilities.items(), reverse=True):
        cumulative_odds += odds
        
        if roll == REZ:
            print(f"DMG: {roll:^3}  Odds: {cumulative_odds:.2%}")
            while cumulative_odds >= thresholds[-1]:
                thresholds.pop()
        elif thresholds and cumulative_odds >= thresholds[-1]:
            thresholds.pop()
            print(f"DMG: {roll:^3}  Odds: {cumulative_odds:.2%}")
        
    print(f"Sum of probabilities = {sum(existing_probabilities.values())}")

