from itertools import *

def remove(string,char):
    return ''.join(letter for letter in string if letter!=char)

def hash_sequence(genome,k):
    n_dict = {}
    for i in range(len(genome) - k + 1):
        if genome[i:i+k] in n_dict:
            n_dict[genome[i:i+k]].append(i)
        else:
            n_dict[genome[i:i+k]] = [i]
    return n_dict


def intersects(genome1,genome2,k):
    if len(genome1) < len(genome2):
        chk_dict = hash_sequence(genome1, k)
        for i in range(len(genome2) - k + 1):
            if genome2[i:i+k] in chk_dict:
                return genome2[i:i+k]
        return None
    else:
        chk_dict = hash_sequence(genome2, k)
        for i in range(len(genome1) - k + 1):
            if genome1[i:i+k] in chk_dict:
                return genome1[i:i+k]
        return None
        
from Legionella import legionella
from Brucella import brucella
from Shigella_sonnei import shigella
from Helicobacter_pylori import helicobacter

def gimel():
    genomes = [("Legionella", remove(legionella, '\n')),
               ("Brurcella", remove(brucella, '\n')),
               ("Shigella", remove(shigella, '\n')),
               ("Helicobacter", remove(helicobacter, '\n'))]
    res = {}
    for tup in combinations(genomes, 2):
        left = 0
        right = 150
        while right-left != 1:
            if intersects(tup[0][1], tup[1][1], (left+right)//2) == None:
                right = (left+right)//2
            else:
                left = (left+right)//2
        res[(tup[0][0], tup[1][0])] = (left, intersects(tup[0][1], tup[1][1]
                                                        , left))
    return res
            
    
