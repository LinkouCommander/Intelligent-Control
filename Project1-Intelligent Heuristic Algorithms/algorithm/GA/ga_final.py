import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import test

class GA():
    def __init__(self, population, upperboundary, lowerboundary, dimension, functionvalue, crossover_rate=0.5, mutation_rate=0.5, cp=0.95, mp=0.1):
        self.population = population
        self.upperboundary = upperboundary
        self.lowerboundary = lowerboundary
        self.dimension = dimension
        self.functionvalue = functionvalue
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.cp = cp
        self.mp = mp

        self.num_crossover = int(self.population * self.crossover_rate)
        self.num_mutation = int(self.population * self.mutation_rate)
        self.num_chromosome = self.population

        self.best_chromosome = np.zeros(self.dimension)

    def initialize(self):
        if (self.num_crossover % 2) == 1:   #確認num_crossover是否為偶數
            self.num_crossover -= 1
            # self.num_chromosome -= 1
        
        self.chromosome = np.zeros((self.num_chromosome, self.dimension))
        self.selected_chromosomes = np.zeros((self.num_crossover, self.dimension))

        #隨機產生chromosomes in range(lowerbound, upperbound)
        for i in range(self.population):
            for j in range(self.dimension):
                self.chromosome[i][j] = random.random(
                ) * (self.upperboundary-self.lowerboundary) + self.lowerboundary

        #挑選初代遺傳的parent
        self.fitness_function(self.chromosome)
        self.best_fitness = np.min(self.fitness)
        self.best_chromosome = self.chromosome[np.argmin(self.fitness)]
        # print(self.best_chromosome,self.best_fitness)
        # 挑選下一代的成員

    #計算fitness
    def fitness_function(self, gene):
        self.fitness = np.zeros(gene.shape[0])
        for i in range(gene.shape[0]):
            self.fitness[i] = self.functionvalue(gene[i])

    def select(self):
        self.fitness_function(self.chromosome)
        fit_arg = np.argsort(self.fitness)
        self.chromosome = self.chromosome[fit_arg]
        self.selected_chromosomes = self.chromosome[:self.num_crossover]

    def crossover(self):
        if self.cp > random.random():
            L = random.sample(range(0, self.dimension+1), 2)
            L_s = random.sample(range(0, self.num_crossover), self.num_crossover)
            #以三段進行基因交換
            for i in range(int(self.num_crossover/2)):
                #child 1
                self.chromosome[self.population-2*i-1][0:L[0]] = self.selected_chromosomes[L_s[2*i]][0:L[0]]
                self.chromosome[self.population-2*i-1][L[0]:L[1]] = self.selected_chromosomes[L_s[2*i+1]][L[0]:L[1]]
                self.chromosome[self.population-2*i-1][L[1]:] = self.selected_chromosomes[L_s[2*i]][L[1]:]
                #child 2
                self.chromosome[self.population-(2*i+2)][0:L[0]] = self.selected_chromosomes[L_s[2*i+1]][0:L[0]]
                self.chromosome[self.population-(2*i+2)][L[0]:L[1]] = self.selected_chromosomes[L_s[2*i]][L[0]:L[1]]
                self.chromosome[self.population-(2*i+2)][L[1]:] = self.selected_chromosomes[L_s[2*i+1]][L[1]:]
            
    #隨機對某個基因產生亂數
    def mutation(self):
        if self.mp > random.random():
            Lp = random.sample(range(0, self.dimension+1), 2)  #選定突變基因位置
            L = random.sample(range(self.num_crossover, self.num_chromosome), self.num_mutation)   #選定突變chromosome
            for i in range(self.num_mutation):
                # l = random.randrange(self.dimension)
                self.chromosome[L[i]][Lp[0]:Lp[1]] = random.random() * (self.upperboundary-self.lowerboundary) + self.lowerboundary


    #更新最佳值
    def update(self):
        self.mean_fitness = np.mean(self.fitness)
        if self.best_fitness > np.min(self.fitness):
            self.best_fitness = np.min(self.fitness)
            self.best_chromosome = self.chromosome[0]

def run(al):
    run = 50
    iteration = 2500
    answer_bsf=np.zeros((run))
    answer_mf=np.zeros((run,50))
    for j in range(run):
        ans = al
        ans.initialize()
        for i in range(iteration):
            ans.select()
            ans.crossover()
            ans.mutation()
            ans.update()
        answer_bsf[j] = ans.best_fitness
        answer_mf[j] = ans.fitness
    # print(answer_bsf)
    print("avg b-s-f : ",np.mean(answer_bsf))
    print("avg m-f : ", np.mean(answer_mf))
    print("med b-s-f : ",np.percentile(answer_bsf,50))
    print("std b-s-f : ",np.std(answer_bsf))
    print("\n")

run(GA(50, -10, 10, 30, test.F2))
run(GA(50, -100, 100, 30, test.F3))
run(GA(50, -600, 600, 30, test.F11))
run(GA(50, -50, 50, 30, test.F12))
run(GA(50, -50, 50, 30, test.F13))
run(GA(50, -65, 65, 2, test.F14))
run(GA(50, -5, 5, 4, test.F15))