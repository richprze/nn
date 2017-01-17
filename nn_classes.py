from random import random, randint
from math import exp

class NeuralNet:
    def __init__(self, num_inputs, num_outputs, num_layers, num_neurons):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_layers = num_layers
        self.num_neurons = num_neurons
        self.layers = []
        # create layers: > 1 layer
        if (num_layers > 1):
            # create first layer (layer 0)
            self.layers.append(self.create_layer(num_neurons, num_inputs))
            # create middle layers (layers 1 thru N-1)
            for i in range(1,num_layers-1):
                self.layers.append(self.create_layer(num_neurons, num_neurons))
            # create output layer (layer N)
            self.layers.append(self.create_layer(num_outputs, num_neurons))
        # create layers: only 1 layer (output layer)
        elif (num_layers == 1):
            self.layers.append(self.create_layer(num_outputs, num_inputs))

    def __repr__(self):
        return "<Neural Net with {} inputs, {} outputs, {} layers, {} neurons per layer>".format(self.num_inputs, self.num_outputs, self.num_layers, self.num_neurons)

    def create_neuron(self, num_inputs):
        weights = []
        # the '+1' on inputs is for the bias/threshold
        for i in range(0,num_inputs+1):
            weights.append(random())
        return weights

    def create_layer(self, num_neurons, num_inputs):
        layer = []
        for i in range(0,num_neurons):
            layer.append(self.create_neuron(num_inputs))
        return layer

    def get_num_weights(self):
        num_weights = 0
        for layer in self.layers:
            for neuron in layer:
                for weight in neuron:
                    num_weights += 1
        return num_weights

    def get_weights(self):
        weights = []
        for layer in self.layers:
            for neuron in layer:
                for weight in neuron:
                    weights.append(weight)
        return weights

    def print_lnw(self):
        for layer in self.layers:
            the_layer = []
            for neuron in layer:
                the_layer.append(neuron)
            print(the_layer)

    def update_weights(self, weights):
        for i in range(0,len(self.layers)):
            for j in range(0,len(self.layers[i])):
                for k in range(0,len(self.layers[i][j])):
                    self.layers[i][j][k] = weights.pop(0)

    def get_output(self, inputs):
        if (len(inputs) == self.num_inputs):
            for layer in self.layers:
                outputs = []
                # add the -1 for bias/threshold to inputs
                inputs.append(-1)
                for neuron in layer:
                    outputs.append(self.sigmoid(sum([x*y for x,y in zip(inputs, neuron)])))
                inputs = outputs
                print(outputs)
        return outputs

    def sigmoid(self, number):
        return (1 / (1 + exp(-number)/1))

class Sweeper:
    def __init__(self, net, fitness=0):
        self.brain = net
        self.fitness = fitness

        # random start position
        self.position = [randint(0,inputs.XSIZE),randint(0,inputs.YSIZE)]

    # Function to take inputs and get outputs
    def move(self, inputs):
        return none



class Population: # Holds the population. Does the "game" then the genetic algorithm to evolve a population
    # This class will control the sweepers sweeping
    def __init__(self, pop_size, mutation_rate, xover_rate, num_weights):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.xover_rate = xover_rate
        self.chromo_len = num_weights
        self.total_fitness = 0
        self.generation = 0
        self.most_fit = 0
        self.best_fitness = 0
        self.worst_fitness = 999999999
        self.avg_fitness = 0
        self.chromosomes = []

        # TODO: initiatilize pop with chromosomes of random weights and fitness = 0
        # Question: use random weights, or use from initializing NN, or initialize NN here?

        # create population of chromosomes 
        for i in range(0,pop_size):
            self.chromosomes.append(NeuralNet(inputs.INPUTS, inputs.OUTPUTS, inputs.LAYERS, inputs.NEURONS))



    ######################
    # 
    # The general flow
    # 1. Run "ticks" - let the sweepers sweep for X number of runs
    #       a. get inputs for each sweeper: closest mine + facing vector
    #       b. get output from NN for each sweeper using above inputs
	#       c. move the sweepers
	#       d. if found mine -> update fitness
	#           ** If 2 sweepers find same mine, first one in array "gets" it (record this somehow)
    #       e. repeat X times
    # 2. Evolve the population (create a new generation)
    #       a. Create a new population
    #       b. Replace old population with new one
    #       c. Test if end condition is satisfied, if not -> a
    #
    ######################


    def mutate(self, chromo):
        return chromo

    # uses roulette / random selection to pick a chromosome from the pop
    def get_roulette_chromo(self):
        return chromosomes

    def crossover(self, mom, dad):
        return none

    # evolves the population in 1 generation
    def evolve(self):
        # Repeat until new population size = original population size (complete, new generation)
        # 1. Selection - select 2 parents (weighted to choose ones with better fitness)
        # 2. Crossover - crossover parents to create offspring given crossover probability, else return parents
        # 3. Mutation - mutate the offspring given mutation rate
        # 4. Placement - put new offspring in new population

        # get 2 parents
        parents = get_roulette_chromo()

        return none

    # returns the N best genomes
    def get_N_best(self):
        return none

    # update init variables
    def calc_fitness_stats(self):
        return none

    # reset all fitness vars/stats
    def reset(self):
        self.total_fitness = 0
        self.best_fitness = 0
        self.worst_fitness = 999999999
        self.avg_fitness = 0
