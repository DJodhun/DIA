import random
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import copy
import itertools
import tkinter as tk
from tkinter import *

#%%
#1step is more accurate for the task at hand
def makeRandomPath1step(length):
    path = []
    choices = []
    coord1 = 1#np.random.randint(1, 10)
    coord2 = 1#np.random.randint(1, 10)
    startingPosition = (coord1, coord2)
    path.append(startingPosition)
    while len(path) != length:
        choice = np.random.randint(1,5)
        choices.append(choice)
        movement = np.random.randint(1,5)
        if choice == 1:
            coord1 = coord1 - 1
            if coord1 <= 0:
                coord1 = coord1 + 1
        if choice == 2:
            coord1 = coord1 + 1
            if coord1 >= 10:
                coord1 = coord1 - 1
        if choice == 3: 
            coord2 = coord2 - 1
            if coord2 <= 0:
                coord2 = coord2 + 1
        if choice == 4:
            coord2 = coord2 + 1
            if coord2 >= 10:
                coord2 = coord2 - 1
                
        newPosition = (coord1, coord2)
        path.append(newPosition)   
        
        
    return path, choices

#johnny, test = makeRandomPath1step(20)

def choicesToPath(choices):
    path = []
    coord1 = 1
    coord2 = 1
    startingPosition = (coord1, coord2)
    path.append(startingPosition)
    for i in range(len(choices)):
        if choices[i] == 1:
            coord1 = coord1 - 1
            if coord1 <= 0:
                coord1 = coord1 + 1
        if choices[i] == 2:
            coord1 = coord1 + 1
            if coord1 >= 10:
                coord1 = coord1 - 1
        if choices[i] == 3: 
            coord2 = coord2 - 1
            if coord2 <= 0:
                coord2 = coord2 + 1
        if choices[i] == 4:
            coord2 = coord2 + 1
            if coord2 >= 10:
                coord2 = coord2 - 1
                
        newPosition = (coord1, coord2)
        path.append(newPosition)   
        
        
    return path

#johnnytest2 = choicesToPath(test)
    
#%%
def mutate2(parent, numberOfMutations):
    parent1 = copy.deepcopy(parent)    
    parent = parent[0]
    for _ in range(numberOfMutations):
        index = np.random.randint(0, len(parent))
        mutation = random.randint(1, 9)
        parent[index] = mutation
    
    return parent

def crossOver(parent1, parent2):
    crossChild = []
    parent12 = copy.deepcopy(parent1)
    parent12contrib1 = list(parent12[0:10])
    parent12contrib2 = list(parent12[10:20])
    parent22 = copy.deepcopy(parent2)
    parent22contrib1 = list(parent22[0:10])
    parent22contrib2 = list(parent22[10:20])
    split = np.random.randint(1,3)
    if split == 1:
        crossChild.extend(list(parent12contrib1))
        crossChild.extend(list(parent22contrib2))
    if split == 2:
        crossChild.extend(list(parent12contrib2))
        crossChild.extend(list(parent22contrib1))
    return crossChild

def initialPopulation(numberInGeneration):
    population = []
    for i in range(numberInGeneration):
        path, choices = makeRandomPath1step(20)
        population.append(choices)
    
    return population

def popFitPairs3(initialpop):
    fitness22 = []
    success = []
    averages2 = []
    bests2 = []
    population1 = copy.deepcopy(initialpop)
    count = 0
    
    for i in range(len(initialpop)):
        count += 1
        fitness22.append(geneticMain(initialpop[i]))
        #fitnessnorm2 = [fitness22*success for fitness22, success in zip(fitness22, success)]
        # print(fitnessnorm22)
        averages2.append(sum(fitness22)/count)
        print("av ",sum(fitness22)/count)
        bests2.append(max(fitness22))
        print("max ",max(fitness22))
    
    pairs = list(zip(population1,fitness22))
    
    return pairs, fitness22, averages2, bests2
    
def tournament(popFitPairs, tournamentSize, popSiz): #popSiz = numberOfRuns -> popSiz should be half of numberOfRuns so that 2 parents make 1 child
    newPopulation = []
    bestGenes = []
    for _ in range(popSiz):
        tournament = random.sample(popFitPairs, tournamentSize) 
        parent1 = sorted(tournament, reverse = True, key=lambda x:x[1])[0]
        bestGenes.append(parent1)
        parent2 = sorted(tournament, reverse = True, key=lambda x:x[1])[1]
        crossChild = crossOver(parent1[0], parent2[0])
        newPopulation.append(crossChild)
        mutation = np.random.randint(1, 5)
        if mutation == 1:
            mutated = mutate2(parent1, 4)
            newPopulation.append(mutated)
        
        newPopulation1 = copy.deepcopy(newPopulation)
        
        
    bestGene = sorted(bestGenes, reverse = True, key=lambda x:x[1])[0]
    
    return parent1, parent2, newPopulation1, bestGene, bestGenes, tournament#, parent1, parent2, parent1ff, parent2ff, newPopulation, bestGene, bestGenes

success = []
initialpop = initialPopulation(20)
#pairs = popFitPairs3(initialpop)
#p1, p2, newPop, bestGene, bestGenes, tourney = tournament(pairs, 4, 20)
#childtest = mutate2(p1)

def runGA3(numberInGeneration, tournamentSize, popSiz, numberOfGenerations):
    totalfitness = []
    totalavs = []
    totalbests = []
    bestGenestotal = []
    count = 0
    avs2g = []
    bests2g = []
    poptot = []
    
    population1 = initialPopulation(20)
    poptot.append(population1)
    
    for i in range(numberOfGenerations):
        count += 1
        print("Generation: ", count)
        pairs, fitness, averages, bests = popFitPairs3(population1)
        # if pairs[i]*success[i] == 0:
        #     fitness[i] = 0
        totalfitness.append(fitness)
        totalavs.append(averages)
        avs2g.append(averages)
        bests2g.append(bests)
        totalbests.append(bests)
        parent1, parent2, population1, bestGene, bestGenes, tourney = tournament(pairs, tournamentSize, popSiz)
        population2 = copy.deepcopy(population1)
        poptot.append(population1)
        
    return totalfitness, totalavs, totalbests, parent1, parent2, poptot, bestGene, bestGenes, tourney

# def geneticMain(initialpop):
#     pass
