from re import T
import pandas as pd
import numpy as np

data = pd.read_csv("../pokemon_data.csv")

sort_best = data.sort_values(by='Total',ascending=False)
best_standard = sort_best[(sort_best['Legendary'] == False) & (~sort_best['Name'].str.contains("Mega"))]

#print(best_standard[['Name', 'Total']][best_standard['Total'] >= 600])

def options(retrieval):
    print("\nType 's' for stats, 't' for type effectiveness, or 'b' to go back:")
    choice = input()
    if choice == 's':
        print("\nStat Total: " + retrieval.get(["Total"]).to_string(header=False, index=False))
        print()
        print("HP: "  + retrieval.get(["HP"]).to_string(header=False, index=False))
        print("Attack: "  + retrieval.get(["Attack"]).to_string(header=False, index=False))
        print("Defense: "  + retrieval.get(["Defense"]).to_string(header=False, index=False))
        print("Sp. Attack: "  + retrieval.get(["Sp. Atk"]).to_string(header=False, index=False))
        print("Sp. Defense: "  + retrieval.get(["Sp. Def"]).to_string(header=False, index=False))
        print("Speed: "  + retrieval.get(["Speed"]).to_string(header=False, index=False))
        print()
    elif choice == 't':
        print("\nTypes")
    elif choice != 'b':
        print("\nNot a valid choice")
        options(retrieval)
        

def command_loop():
    while True:
        print("Enter the name of a Pokemon or '0' to quit: ")
        pokemon = input().lower()
        if pokemon == '0':
            break
        retrieval = data[data['Name'].str.lower() == pokemon]
        if retrieval.empty:
            print("\nNot a valid Pokemon\n")
            continue
        options(retrieval)
        

command_loop()