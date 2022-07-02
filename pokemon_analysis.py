from re import T
import pandas as pd
import numpy as np
import math

data = pd.read_csv("pokemon_data.csv")

SUPEREFFECTIVE = {'Grass': set(['Fire', 'Ice', 'Poison', 'Flying', 'Bug']),
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

NONEFFECTIVE =   {'Grass': set(['Water', 'Electric', 'Grass', 'Ground']),
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

INEFFECTIVE =    {'Flying': set(['Ground']),
                  'Normal': set(['Ghost']),
                  'Ground': set(['Electric']),
                  'Fairy': set(['Dragon']),
                  'Steel': set(['Poison']),
                  'Ghost': set(['Normal', 'Fighting']),
                  'Dark': set(['Psychic'])
}

class Pokemon:
    def __init__(self, retrieval, level = 0):
        self.retrieval = retrieval
        self.level = level

        self.name = retrieve(retrieval, "Name")
        self.gen = str(retrieve(retrieval, "Generation"))

        if level == 0:
            self.attack = retrieve(retrieval, "Attack")
            self.defense = retrieve(retrieval, "Defense")
            self.spatk = retrieve(retrieval, "Sp. Atk")
            self.spdef = retrieve(retrieval, "Sp. Def")
            self.speed = retrieve(retrieval, "Speed")
            self.hp = retrieve(retrieval, "HP")
        else:
            self.attack = math.floor(0.01 * 2 * retrieve(retrieval, "Attack") * level) + 5
            self.defense = math.floor(0.01 * 2 * retrieve(retrieval, "Defense") * level) + 5
            self.spatk = math.floor(0.01 * 2 * retrieve(retrieval, "Sp. Atk") * level) + 5
            self.spdef = math.floor(0.01 * 2 * retrieve(retrieval, "Sp. Def") * level) + 5
            self.speed = math.floor(0.01 * 2 * retrieve(retrieval, "Speed") * level) + 5
            self.hp = math.floor(0.01 * 2 * retrieve(retrieval, "HP") * level) + level + 10
        self.total = self.attack + self.defense + self.spatk + self.spdef + self.speed + self.hp
        
        self.type1 = retrieve(retrieval, "Type 1")
        self.type2 = ''
        if not pd.isna(retrieval["Type 2"]).bool():
            self.type2 = retrieve(retrieval, "Type 2")
        self.types = self.effectiveness()
    
    # Returns each type in a dictionary categorized by effectiveness against this Pokemon
    def effectiveness(self):
        types = {'Grass': 1, 'Fire': 1, 'Water': 1, 'Poison': 1, 'Flying': 1, 'Dragon': 1, 'Bug': 1, 'Normal': 1, 'Electric': 1, 'Ground': 1, 'Fairy': 1, 'Fighting': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Ice': 1, 'Ghost': 1, 'Dark': 1}
        types = self.calculate_effect(self.type1, types)
        if self.type2 != '':
            types = self.calculate_effect(self.type2, types)
        
        total_effect = {4: set(), 2: set(), 1: set(), 0.5: set(), 0.25: set(), 0: set()}
        for effect in types:
            total_effect[types[effect]].add(effect)

        return total_effect
    
    # Edits and returns a given dictionary of types based on each type's effectiveness against this Pokemon
    def calculate_effect(self, retrieval_type, types):
        for effect in SUPEREFFECTIVE[retrieval_type]:
            types[effect] *= 2
        for effect in NONEFFECTIVE[retrieval_type]:
            types[effect] /= 2
        if retrieval_type in INEFFECTIVE:
            for effect in INEFFECTIVE[retrieval_type]:
                types[effect] *= 0

        return types
    
    # Prints full analysis
    def print_all(self):
        print()
        print(self.name + " (Gen " + self.gen + ")")
        print("Type: " + self.type1, end='')
        if self.type2 != '':
            print("/" + self.type2, end='')

        print("\n\nType Effectiveness")
        total_effect = self.types
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
        print("Stat Total: " + str(self.total))
        print("HP: "  + str(self.hp))
        print("Attack: "  + str(self.attack))
        print("Defense: "  + str(self.defense))
        print("Sp. Attack: "  + str(self.spatk))
        print("Sp. Defense: "  + str(self.spdef))
        print("Speed: "  + str(self.speed))
        print()
    

# Handles user input
def command_loop():
    while True:
        print("Enter the name of a Pokemon or 'q' to quit: ")
        pokemon = input().lower()
        if pokemon == 'q':
            break

        retrieval = data[data['Name'].str.lower() == pokemon]
        if retrieval.empty:
            print("\nNot a valid Pokemon\n")
            continue

        p1 = Pokemon(retrieval)
        p1.print_all()

# Retrieves data about a specific Pokemon
def retrieve(retrieval, parameter):
    return retrieval.iloc[0][parameter]


command_loop()