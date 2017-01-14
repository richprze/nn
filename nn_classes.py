from random import randint
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
            weights.append(randint(-1000,1000)/1000.0)
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
            print the_layer

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
                print outputs
        return outputs

    def sigmoid(self, number):
        return (1 / (1 + exp(-number)/1))


class Population: # genetic algorithm for evolving a population
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

    ######################
    # 
    # The general flow
    # 1. Evaluate fitness of each chromosome (should be done already?)
    # 2. Create a new population
    # 3. Replace old population with new one
    # 4. Test - 

    # TODO: initiatilize pop with chromosomes of random weights and fitness = 0
    # Question: use random weights, or use from initializing NN, or initialize NN here?


    def mutate(self, chromo):
        return chromo

    def get_roulette_chromo(self):
        # uses roulette / random selection to pick a chromosome from the pop
        return none

    def crossover(self, mom, dad):
        return none

    def evolve(self):
        # evolves the population in 1 generation


        return none

    def get_N_best(self):
        # returns the N best genomes
        return none

    def calc_fitness_stats(self):
        # update init variables
        return none

    def reset(self):
        # reset all fitness vars/stats
        self.total_fitness = 0
        self.best_fitness = 0
        self.worst_fitness = 999999999
        self.avg_fitness = 0
