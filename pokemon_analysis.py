from calendar import c
from re import T
import pandas as pd
import numpy as np
import math

data = pd.read_csv("pokemon_data.csv")

SUPEREFFECTIVE = {
'Grass': set(['Fire', 'Ice', 'Poison', 'Flying', 'Bug']),
'Fire': set(['Water', 'Ground', 'Rock']),
'Water': set(['Electric', 'Grass']),
'Poison': set(['Ground', 'Psychic']),
'Flying': set(['Electric', 'Ice', 'Rock']),
'Dragon': set(['Ice', 'Dragon', 'Fairy']),
'Bug': set(['Fire', 'Flying', 'Rock']),
'Normal': set(['Fighting']),
'Electric': set(['Ground']),
'Ground': set(['Water', 'Grass', 'Ice']),
'Fairy': set(['Poison', 'Steel']),
'Fighting': set(['Flying', 'Psychic', 'Fairy']),
'Psychic': set(['Bug', 'Ghost', 'Dark']),
'Rock': set(['Water', 'Grass', 'Fighting', 'Ground', 'Steel']),
'Steel': set(['Fire', 'Fighting', 'Ground']),
'Ice': set(['Fire', 'Fighting', 'Rock', 'Steel']),
'Ghost': set(['Ghost', 'Dark']),
'Dark': set(['Fighting', 'Bug', 'Fairy'])
}

NONEFFECTIVE =   {
'Grass': set(['Water', 'Electric', 'Grass', 'Ground']),
'Fire': set(['Fire', 'Grass', 'Ice', 'Bug', 'Steel', 'Fairy']),
'Water': set(['Fire', 'Water', 'Ice', 'Steel']),
'Poison': set(['Grass', 'Fighting', 'Poison', 'Bug', 'Fairy']),
'Flying': set(['Grass', 'Fighting', 'Bug']),
'Dragon': set(['Fire', 'Water', 'Electric', 'Grass']),
'Bug': set(['Grass', 'Fighting', 'Ground']),
'Normal': set([]),
'Electric': set(['Electric', 'Flying', 'Steel']),
'Ground': set(['Poison', 'Rock']),
'Fairy': set(['Fighting', 'Bug', 'Dark']),
'Fighting': set(['Bug', 'Dark', 'Rock']),
'Psychic': set(['Fighting', 'Psychic']),
'Rock': set(['Normal', 'Fire', 'Poison', 'Flying']),
'Steel': set(['Normal', 'Grass', 'Ice', 'Flying', 'Psychic', 'Bug', 'Rock', 'Dragon', 'Steel', 'Fairy']),
'Ice': set(['Ice']),
'Ghost': set(['Poison', 'Bug']),
'Dark': set(['Ghost', 'Dark'])
}

INEFFECTIVE =    {
'Flying': set(['Ground']),
'Normal': set(['Ghost']),
'Ground': set(['Electric']),
'Fairy': set(['Dragon']),
'Steel': set(['Poison']),
'Ghost': set(['Normal', 'Fighting']),
'Dark': set(['Psychic'])
}

class Pokemon:
    # Constructs a Pokemon object
    # Inputs: a single row 'retrieval' from DataFrame data
    # and an optional 'level' integer
    def __init__(self, retrieval, level = 0):
        self.retrieval = retrieval
        self.level = level

        self.name = retrieve(retrieval, "Name")
        self.gen = str(retrieve(retrieval, "Generation"))

        self.attack = retrieve(retrieval, "Attack")
        self.defense = retrieve(retrieval, "Defense")
        self.spatk = retrieve(retrieval, "Sp. Atk")
        self.spdef = retrieve(retrieval, "Sp. Def")
        self.speed = retrieve(retrieval, "Speed")
        self.hp = retrieve(retrieval, "HP")
        if level != 0:
            self.attack = self.calc_stat(self.attack, level)
            self.defense = self.calc_stat(self.defense, level)
            self.spatk = self.calc_stat(self.spatk, level)
            self.spdef = self.calc_stat(self.spdef, level)
            self.speed = self.calc_stat(self.speed, level)
            self.hp = math.floor(0.01 * 2 * retrieve(retrieval, "HP") * level) + level + 10
        
        self.type1 = retrieve(retrieval, "Type 1")
        self.type2 = ''
        if not pd.isna(retrieval["Type 2"]).bool():
            self.type2 = retrieve(retrieval, "Type 2")
        self.total_effect = self.effectiveness()
    
    # Calculates a stat dependent upon a Pokemon's level
    def calc_stat(self, stat, level):
        return math.floor(0.01 * 2 * stat * level) + 5
    
    # Calculates a Pokemon's stat total
    def calculate_total(self):
        return int(round(self.attack + self.defense + self.spatk + self.spdef + self.speed + self.hp))
    
    # Returns each type in a dictionary categorized by effectiveness against
    # this Pokemon
    def effectiveness(self):
        types = {'Grass': 1, 'Fire': 1, 'Water': 1, 'Poison': 1, 'Flying': 1,
                 'Dragon': 1, 'Bug': 1, 'Normal': 1, 'Electric': 1, 'Ground': 1,
                 'Fairy': 1, 'Fighting': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1,
                 'Ice': 1, 'Ghost': 1, 'Dark': 1}
        types = self.calculate_effect(self.type1, types)
        if self.type2 != '':
            types = self.calculate_effect(self.type2, types)
        
        total_effect = {4: set(), 2: set(), 1: set(), 0.5: set(), 0.25: set(), 0: set()}
        for effect in types:
            total_effect[types[effect]].add(effect)

        return total_effect
    
    # Edits and returns a given dictionary of types based on each type's
    # effectiveness against this Pokemon
    def calculate_effect(self, retrieval_type, types):
        for effect in SUPEREFFECTIVE[retrieval_type]:
            types[effect] *= 2
        for effect in NONEFFECTIVE[retrieval_type]:
            types[effect] /= 2
        if retrieval_type in INEFFECTIVE:
            for effect in INEFFECTIVE[retrieval_type]:
                types[effect] *= 0

        return types
    
    # Prints full analysis for this Pokemon
    def print_all(self):
        print()
        print(self.name + " (Gen " + self.gen + ")")
        print("Type: " + self.type1, end='')
        if self.type2 != '':
            print("/" + self.type2, end='')

        print("\n\nType Effectiveness")
        total_effect = self.total_effect
        to_print = (4, 2, 0.5, 0.25, 0)
        for multiplier in to_print:
            self.print_effectiveness(total_effect, multiplier)

        print("\nStats")
        self.print_stats()
    
    # Prints effectiveness against this Pokemon
    def print_effectiveness(self, total_effect, multiplier):
        if len(total_effect[multiplier]) > 0:
            print(str(multiplier) + "x Effective: ", end='')
            index = 0
            for type in total_effect[multiplier]:
                print(type, end='')
                index += 1
                if index < len(total_effect[multiplier]):
                    print(", ", end='')
            print()
    
    # Prints this Pokemon's stats
    def print_stats(self):
        print("Stat Total: " + str(self.calculate_total()))
        print("HP: "  + str(self.hp))
        print("Attack: "  + str(self.attack))
        print("Defense: "  + str(self.defense))
        print("Sp. Attack: "  + str(self.spatk))
        print("Sp. Defense: "  + str(self.spdef))
        print("Speed: "  + str(self.speed))
        print()
    

# Handles user input in standard mode
def command_loop():
    while True:
        print("Enter the name of a Pokemon or 'c' for comparison mode or 'q' to quit: ")
        user_input = input().lower()
        if user_input == 'q':
            break
        if user_input == 'c':
            comparison_loop()
            break

        retrieval = data[data['Name'].str.lower() == user_input]
        if retrieval.empty:
            print("\nNot a valid Pokemon\n")
            continue

        p1 = Pokemon(retrieval)
        p1.print_all()

# Handles user input in comparison mode
def comparison_loop():
    while True:
        print("\nEnter the name of a Pokemon or 'q' to quit: ")
        user_input = input().lower()
        if user_input == 'q':
            break
        retrieval = data[data['Name'].str.lower() == user_input]
        if retrieval.empty:
            print("\nNot a valid Pokemon\n")
            continue

        p1 = Pokemon(retrieval, get_level())

        print("\nEnter the name of a 2nd Pokemon: ")
        user_input = input().lower()
        retrieval = data[data['Name'].str.lower() == user_input]
        if retrieval.empty:
            print("\nNot a valid Pokemon\n")
            continue

        p2 = Pokemon(retrieval, get_level())

        print("\nPokemon 1: " + p1.name)
        p1.print_stats()
        print("\nPokemon 2: " + p2.name)
        p2.print_stats()

        adjust_stats(p1, p2)

        print("The winner is:")
        if p1.calculate_total() > p2.calculate_total():
            print(p1.name)
            print("Score: " + str(p1.calculate_total()) + " - " + str(p2.calculate_total()))
        elif p2.calculate_total() > p1.calculate_total():
            print(p2.name)
            print("Score: " + str(p2.calculate_total()) + " - " + str(p1.calculate_total()))
        else:
            print("Tie!")
            print("Score: " + str(p2.calculate_total()) + " - " + str(p1.calculate_total()))
        
# Extracts a piece of data from a given row of a DataFrame
def retrieve(retrieval, parameter):
    return retrieval.iloc[0][parameter]

# Prompts the user to input a level and returns it
def get_level():
    print("\nEnter the Pokemon's level: ")
    level_input = input()
    try:
        int(level_input)
    except:
        print("Not a number. Try again.")
        return get_level()
    else:
        level_input = int(level_input)
        if level_input > 0 and level_input < 101:
            return level_input
        else:
            print("Not a valid level. Try again.")
            return get_level()

# Compares two given Pokemon and adjusts their stats accordingly
def adjust_stats(p1, p2):
    attack_adjust1(p1)
    attack_adjust1(p2)
    stab_adjust(p1, p2)
    stab_adjust(p2, p1)
    attack_adjust2(p1, p2)
    attack_adjust2(p2, p1)
    if p1.speed != p2.speed:
        speed_adjust(p1, p2) if p2.speed > p1.speed else speed_adjust(p2, p1)

# Returns the stab multiplier of the Pokemon 'winner'
def stab_multiplier(loser, winner):
    if winner.type1 in loser.total_effect[4]:
        return 4
    elif winner.type2 in loser.total_effect[4]:
        return 4
    elif winner.type1 in loser.total_effect[2]:
        return 2
    elif winner.type2 in loser.total_effect[2]:
        return 2
    else:
        return 1

# Gives attack stat advantage to the Pokemon 'winner' based on stab multiplier
def stab_adjust(loser, winner):
    if winner.attack > winner.spatk:
        winner.attack *= stab_multiplier(loser, winner)
    else:
        winner.spatk *= stab_multiplier(loser, winner)

# Gives hp stat disadvantage to the Pokemon 'loser'
def speed_adjust(loser, winner):
    if winner.attack > winner.spatk:
        loser.hp -= ((((2 * winner.level) / 5) + 2) * 50 * (winner.attack / loser.defense)) / 50 + 2
    else:
        loser.hp -= ((((2 * winner.level) / 5) + 2) * 50 * (winner.spatk / loser.spdef)) / 50 + 2

# Gives attack stat disadvantage if necessary
def attack_adjust1(loser):
    if (loser.attack - loser.spatk) >= 40:
        loser.spatk /= 2
    elif (loser.spatk - loser.attack) >= 40:
        loser.attack /= 2

# Adjusts HP based on attack stats as necessary
def attack_adjust2(loser, winner):
    if winner.attack > winner.spatk:
        loser.hp -= (winner.attack - loser.defense)
    else:
        loser.hp -= (winner.spatk - loser.spdef)

command_loop()