from random import random, randint
from math import exp, pi, sqrt, sin, cos
import inputs
import settings

# vector maths
def vec_dist(vec1, vec2):
    return sqrt((vec1[0]-vec2[0])**2 + (vec1[1]-vec2[1])**2)

def vec_diff(sweeper, mine):
    # should be [mine] - [sweeper] to get vec direction from sweeper to mine
    return [mine[0]-sweeper[0], mine[1]-sweeper[1]]

def obj_tuple(pos, pad):
    return (pos[0] - pad, pos[1] - pad, pos[0] + pad, pos[1] + pad)

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
                # print(outputs)
        return outputs

    def sigmoid(self, number):
        return (1 / (1 + exp(-number)/1))

class Sweeper:
    def __init__(self):
        self.brain = NeuralNet(inputs.INPUTS, inputs.OUTPUTS,  inputs.LAYERS, inputs.NEURONS)
        self.fitness = 0

        # random start position & look direction
        self.position = [randint(0,inputs.XSIZE),randint(0,inputs.YSIZE)]
        self.id = settings.board.place_object('sweeper', self.position)
        self.rotation = random() * 2 * pi

        self.closest_mine_id = -1

        if(self.id == 41): print(self.brain.get_weights)

    # Function to take inputs and get outputs
    def get_output(self, inputs):
        return self.brain.get_output(inputs)

    def get_closest_mine(self):
        closest_mine = []
        closest_mine_id = -1
        closest_dist = 9999999999
        # loop thru mines
        for key, mine in enumerate(settings.mines):
            distance = vec_dist(mine['pos'], self.position)
            if distance < closest_dist:
                closest_dist = distance
                closest_mine = mine['pos']
                closest_mine_id = key

        return closest_mine, closest_mine_id

    def move_sweeper(self):
        # get nearest mine
        closest_mine, self.closest_mine_id = self.get_closest_mine()

        # get left and right track
        # if(self.id == 41): print("Sweeper: {}".format(self.id))
        # if(self.id == 41): print("Mine - x: {}, y: {}".format(closest_mine[0], closest_mine[1]))
        # if (self.id == 41): print("Rotation: {}, look.x: {}, look.y: {}".format(self.rotation, sin(self.rotation), cos(self.rotation)))
        tracks = self.get_output([closest_mine[0], closest_mine[1], sin(self.rotation), cos(self.rotation)])
        # if (self.id == 41): print("Tracks - left: {}, right: {}".format(tracks[0], tracks[1]))

        # takes left and right track velocities / forces (outputs from NN) and moves the sweeper
        # will be between 0 and 1
        left = tracks[0]
        right = tracks[1]

        # calculate rotational angle in radians (between 0 and 180 deg, 90 deg = straight)
        rot_angle = (left - right) * pi / 2

        # update sweeper's facing direction (angle from 0 to 360, but in radians)
        self.rotation += rot_angle

        # calculate direction unit vector
        look = [sin(self.rotation), cos(self.rotation)]  # x,y

        # calculate absolute speed
        speed = (left + right) * inputs.MAXSPEED

        # vector to new position
        to_new_pos = [x * speed for x in look]

        # new position (sum the two vectors)
        self.position = [x + y for x, y in zip(self.position, to_new_pos)]

        # account for window and wrap around
        # if x is negative, have it come in from the right
        if self.position[0] < 0:
            self.position[0] = inputs.XSIZE + self.position[0]
        # if x is greater than window size, have it come in the left
        elif self.position[0] > inputs.XSIZE:
            self.position[0] = self.position[0] - inputs.XSIZE

        # if y is negative, have it come up from bottom
        if self.position[1] < 0:
            self.position[1] = inputs.YSIZE + self.position[1]
        # if y is > window size, have it come down from top
        elif self.position[1] > inputs.YSIZE:
            self.position[1] = self.position[1] - inputs.YSIZE

        # move on canvas
        settings.board.canvas.coords(self.id, obj_tuple(self.position, inputs.SWEEPERSIZE))

    def handle_mines(self):
        # check if landed on closest mine
        # future - or if land on ANY mine? Because could go in wrong direction
        closest_mine = settings.mines[self.closest_mine_id]['pos']
        if vec_dist(closest_mine, self.position) < 2:
            # handle it
            self.fitness += 1
            settings.num_mines_found += 1
            settings.board.canvas.delete(settings.mines[self.closest_mine_id]['id'])
            x = round(random() * inputs.XSIZE)
            y = round(random() * inputs.YSIZE)
            settings.mines[self.closest_mine_id] = {'pos': [x, y], 'id': settings.board.place_object('new mine', [x, y])}


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
