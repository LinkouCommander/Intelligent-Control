import random
import sys
import test
import statistics
import numpy as np



class PSO():
    def __init__(self,population,upperboundary,lowerboundary,dimension,functionvalue,self_weight=2,social_weight=2):
        self.population=population
        self.upperboundary=upperboundary
        self.lowerboundary=lowerboundary
        self.dimension=dimension
        self.functionvalue=functionvalue
        self.self_weight=self_weight
        self.social_weight=social_weight
        self.group_best_value=sys.float_info.max

    def initialize(self):
        self.individual_solution=[]
        self.individual_best_solution=[]
        self.individual_best_value=[]
        self.group_best_solution=[]

        min_value=sys.float_info.max
        place=0
        for i in range(self.population):#隨機產生particle的position and velocity
            temp_solution=[]
            for j in range(self.dimension):
                temp=random.random()*(self.upperboundary-self.lowerboundary)+self.lowerboundary
                temp_solution.append(temp)
            self.individual_solution.append(temp_solution)

            temp_value=self.functionvalue(temp_solution)
            self.individual_best_solution.append(temp_solution)
            self.individual_best_value.append(temp_value)
            if temp_value<min_value:
                min_value=temp_value
                place=i
        #設定group best value和group best solution
        self.group_best_value=min_value
        self.group_best_solution=self.individual_solution[place].copy()

    def move(self):
        for i in range(len(self.individual_solution)):
            for j in range(self.dimension):
                #計算velocity
                val=self.self_weight*random.random()*(self.individual_best_solution[i][j]-self.individual_solution[i][j])+\
                    self.social_weight*random.random()*(self.group_best_solution[j]-self.individual_solution[i][j])
                #更新new position
                self.individual_solution[i][j]=val+self.individual_solution[i][j]*(0.5+random.random()/2)
                #注意position的search range
                self.individual_solution[i][j]=min(self.individual_solution[i][j],self.upperboundary)
                self.individual_solution[i][j]=max(self.individual_solution[i][j],self.lowerboundary)


    def update_data(self):
        for i in range(len(self.individual_solution)):
            #newval是fitness function出來的值
            newval=self.functionvalue(self.individual_solution[i])
            #如果newval比individual best value小,就把它更新成newval
            if newval<self.individual_best_value[i]:
                self.individual_best_solution[i]=self.individual_solution[i]
                self.individual_best_value[i]=newval
                #如果還比group best value小,就把它更新成newval
                if newval<self.group_best_value:
                    self.group_best_solution=self.individual_solution[i]
                    self.group_best_value=newval
       


def run(al):
    runs=50
    iteration=500
    answer_absf=[]#average best_so_far
    answer_amf=[]#average mean fitness function
    for j in range(runs):
        ans=al
        ans.initialize()
        for i in range(iteration):
            ans.move()
            ans.update_data()
        answer_absf.append(ans.group_best_value)
        answer_amf.append(ans.individual_best_value)

    temp=0
    for i in range(runs):
        for j in range(50):
            temp+=answer_amf[i][j]
    temp/=50*runs
    
    print("avg b-s-f : ",statistics.mean(answer_absf))
    print("avg m-f : ", temp)
    print("med b-s-f : ",statistics.median(answer_absf))
    np.array(answer_absf)
    print("std b-s-f : ",np.std(answer_absf))
    print("\n")



run(PSO(50,10,-10,30,test.F2))
run(PSO(50,100,-100,30,test.F3))
run(PSO(50,600,-600,30,test.F11))
run(PSO(50,50,-50,30,test.F12))
run(PSO(50,50,-50,30,test.F13))
run(PSO(50,65,-65,2,test.F14))
run(PSO(50,5,-5,4,test.F15))
