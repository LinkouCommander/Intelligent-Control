import random
import sys
import copy

class Bee(object):
    def __init__(self, lower, upper, fun, funcon=None):
        self._random(lower, upper)

        if not funcon:
            self.valid = True
        else:
            self.valid = funcon(self.vector)

        if (fun != None):
            self.value = fun(self.vector)
        else:
            self.value = sys.float_info.max
        self._fitness()

        self.counter = 0

    def _random(self, lower, upper):

        self.vector = []
        for i in range(len(lower)):
            self.vector.append( lower[i] + random.random() * (upper[i] - lower[i]) )

    def _fitness(self):
        if (self.value >= 0):
            self.fitness = 1 / (1 + self.value)
        else:
            self.fitness = 1 + abs(self.value)

class BeeHive(object):
    def run(self):
        cost = {}; 
        cost["best"] = []; 
        cost["mean"] = []
        for itr in range(self.max_itrs):

            for index in range(self.size):
                self.send_employee(index)
            self.send_onlookers()
            self.send_scout()
            self.find_best()

            cost["best"].append( self.best )
            cost["mean"].append( sum( [ bee.value for bee in self.population ] ) / self.size )

            if self.verbose:
                self._verbose(itr, cost)

        return cost

    #建立初始蜂群
    def __init__(self                 ,
                 lower, upper         ,
                 fun          = None  ,
                 numb_bees    = 50    ,
                 max_itrs     = None  ,
                 max_trials   = None  ,
                 selfun       = None  ,
                 seed         = None  ,
                 verbose      = False ,
                 extra_params = None ,):

        assert (len(upper) == len(lower)), "'lower' and 'upper' must be a list of the same length."

        if (seed == None):
            self.seed = random.randint(0, 1000)
        else:
            self.seed = seed
        random.seed(self.seed)

        self.size = int((numb_bees + numb_bees % 2))

        self.dim = len(lower)
        self.max_itrs = max_itrs
        if (max_trials == None):
            self.max_trials = 0.6 * self.size * self.dim
        else:
            self.max_trials = max_trials
        self.selfun = selfun
        self.extra_params = extra_params

        self.evaluate = fun
        self.lower    = lower
        self.upper    = upper

        self.best = sys.float_info.max
        self.solution = None

        self.population = [ Bee(lower, upper, fun) for i in range(self.size) ]

        self.find_best()

        self.compute_probability()

        self.verbose = verbose

    #為雇傭蜂產生候選的解決方案
    def find_best(self):
        values = [ bee.value for bee in self.population ]
        index  = values.index(min(values))
        if (values[index] < self.best):
            self.best     = values[index]
            self.solution = self.population[index].vector

    def compute_probability(self):
        values = [bee.fitness for bee in self.population]
        max_values = max(values)

        if (self.selfun == None):
            self.probas = [0.9 * v / max_values + 0.1 for v in values]
        else:
            if (self.extra_params != None):
                self.probas = self.selfun(list(values), **self.extra_params)
            else:
                self.probas = self.selfun(values)

        return [sum(self.probas[:i+1]) for i in range(self.size)]

    def send_employee(self, index):
        zombee = copy.deepcopy(self.population[index])
        d = random.randint(0, self.dim-1)
        bee_ix = index;
        while (bee_ix == index): bee_ix = random.randint(0, self.size-1)
        zombee.vector[d] = self._mutate(d, index, bee_ix)
        zombee.vector = self._check(zombee.vector, dim=d)
        zombee.value = self.evaluate(zombee.vector)
        zombee._fitness()
        if (zombee.fitness > self.population[index].fitness):
            self.population[index] = copy.deepcopy(zombee)
            self.population[index].counter = 0
        else:
            self.population[index].counter += 1

    #送出觀察蜂，觀察蜂會嘗試為雇傭蜂決定要使用的解決途徑做改進
    def send_onlookers(self):
        numb_onlookers = 0; beta = 0
        while (numb_onlookers < self.size):
            phi = random.random()

            beta += phi * max(self.probas)
            beta %= max(self.probas)

            index = self.select(beta)

            self.send_employee(index)

            numb_onlookers += 1

    #使用輪轉法保留表現好的解決途徑與少數表現差的解決途徑，用以維持差異性。
    def select(self, beta):
        probas = self.compute_probability()

        for index in range(self.size):
            if (beta < probas[index]):
                return index

    #送出偵查蜂並觀察每個蜜源是否達到實驗上限，若達到則放棄該蜜源，並生成新的蜜源代替
    def send_scout(self):
        trials = [ self.population[i].counter for i in range(self.size) ]

        index = trials.index(max(trials))

        if (trials[index] > self.max_trials):
            self.population[index] = Bee(self.lower, self.upper, self.evaluate)
            self.send_employee(index)

    def _mutate(self, dim, current_bee, other_bee):
        return self.population[current_bee].vector[dim]    + \
               (random.random() - 0.5) * 2                 * \
               (self.population[current_bee].vector[dim] - self.population[other_bee].vector[dim])

    def _check(self, vector, dim=None):
        if (dim == None):
            range_ = range(self.dim)
        else:
            range_ = [dim]

        for i in range_:
            if  (vector[i] < self.lower[i]):
                vector[i] = self.lower[i]

            elif (vector[i] > self.upper[i]):
                vector[i] = self.upper[i]

        return vector

    def _verbose(self, itr, cost):
        msg = "# Iter = {} | Best Evaluation Value = {} | Mean Evaluation Value = {} "
        print(msg.format(int(itr), cost["best"][itr], cost["mean"][itr]))