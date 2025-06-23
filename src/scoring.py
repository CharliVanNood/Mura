import os
import pygame
import random

SCORE = "score.txt"


# Dit laadt de huidige score uit een bestand.
def loading_score():
    if os.path.exists(SCORE):
        with open(SCORE, "r") as file:
            return int(file.read())
    return 50 # Standaardscore als bestand nog niet bestaat

# Dit slaat een gegeven score op in het scorebestand.
def save_score(score):
    with open(SCORE, "w") as file:
        file.write(str(score))
# Dit verhoogt  de huidige score met 10, slaat de nieuwe score op en geeft deze terug.
def increase_score(amount=10):
    score = loading_score()
    new_score = score + amount
    save_score(new_score)
    return new_score

# Dit verlaagt de score met 10 als de speler doodgaat, tenzij de score al 0 is,
# dan wordt de score 20. De score wordt opgeslagen en deze wordt teruggeven.
def death_score(window, player):
    if not player.alive:
        score = loading_score()
        if score == 0:
            new_score = 20
        else:
            new_score = max(0, score - 10)
        save_score(new_score)
        return new_score
