from re import T
import pandas as pd
import numpy as np

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

#Handles user input
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

        print_all(retrieval)

#Prints full analysis
def print_all(retrieval):
    print()
    print(retrieve(retrieval, "Name") + " (Gen " + str(retrieve(retrieval, "Generation")) + ")")
    print("Type: " + retrieve(retrieval, "Type 1"), end='')
    if not pd.isna(retrieval["Type 2"]).bool():
        print("/" + retrieve(retrieval, "Type 2"), end='')

    print("\n\nType Effectiveness")
    total_effect = effectiveness(retrieval)
    to_print = (4, 2, 0.5, 0.25, 0)
    for multiplier in to_print:
        print_effectiveness(total_effect, multiplier)

    print("\nStats")
    print_stats(retrieval)

#Retrieves data about a specific Pokemon
def retrieve(retrieval, parameter):
    return retrieval.iloc[0][parameter]

#Prints effectiveness
def print_effectiveness(total_effect, multiplier):
    if len(total_effect[multiplier]) > 0:
        print(str(multiplier) + "x Effective: ", end='')
        index = 0
        for type in total_effect[multiplier]:
            print(type, end='')
            index += 1
            if index < len(total_effect[multiplier]):
                print(", ", end='')
        print()

#Prints stats
def print_stats(retrieval):
    print("Stat Total: " + str(retrieve(retrieval, "Total")))
    print("HP: "  + str(retrieve(retrieval, "HP")))
    print("Attack: "  + str(retrieve(retrieval, "Attack")))
    print("Defense: "  + str(retrieve(retrieval, "Defense")))
    print("Sp. Attack: "  + str(retrieve(retrieval, "Sp. Atk")))
    print("Sp. Defense: "  + str(retrieve(retrieval, "Sp. Def")))
    print("Speed: "  + str(retrieve(retrieval, "Speed")))
    print()

#Returns each type in a dictionary categorized by effectiveness
def effectiveness(retrieval):
    types = {'Grass': 1, 'Fire': 1, 'Water': 1, 'Poison': 1, 'Flying': 1, 'Dragon': 1, 'Bug': 1, 'Normal': 1, 'Electric': 1, 'Ground': 1, 'Fairy': 1, 'Fighting': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Ice': 1, 'Ghost': 1, 'Dark': 1}
    types = calculate_effect(retrieve(retrieval, "Type 1"), types)
    if not pd.isna(retrieval["Type 2"]).bool():
        types = calculate_effect(retrieve(retrieval, "Type 2"), types)
    
    total_effect = {4: set(), 2: set(), 1: set(), 0.5: set(), 0.25: set(), 0: set()}
    for effect in types:
        total_effect[types[effect]].add(effect)

    return total_effect

#Edits and returns a given dictionary of types based on each type's effectiveness
def calculate_effect(retrieval_type, types):
    for effect in SUPEREFFECTIVE[retrieval_type]:
        types[effect] *= 2
    for effect in NONEFFECTIVE[retrieval_type]:
        types[effect] /= 2
    if retrieval_type in INEFFECTIVE:
        for effect in INEFFECTIVE[retrieval_type]:
            types[effect] *= 0

    return types


command_loop()