from random import random, randint, uniform
from math import exp, pi, sqrt, sin, cos
import inputs
import settings
import time

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
        self.id = -1 #settings.board.place_object('sweeper', self.position)
        self.rotation = random() * 2 * pi

        self.closest_mine_id = -1


    def __repr__(self):
        return "<Sweeper - pos: {}, id: {}, rot: {}, fitness: {}>".format(self.position, self.id, self.rotation, self.fitness)

    def place(self):
        self.id = settings.board.place_object('sweeper', self.position)

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
        #           ** If 2 sweepers find same mine, first one in array "gets" it (record this somehow)

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
    def __init__(self):
        self.pop_size = inputs.NUMSWEEPERS
        self.mutation_rate = inputs.MUTATIONRATE
        self.xover_rate = inputs.CROSSOVERRATE
        self.total_fitness = 0
        self.generation = 0
        self.most_fit = 0
        self.best_fitness = 0
        self.worst_fitness = 999999999
        self.avg_fitness = 0
        self.sweepers = []
        self.sweepers_sorted = []

        # initiatilize pop with Sweepers() - (random weights and fitness = 0)
        for i in range(0, self.pop_size):
            sweeper = Sweeper()
            sweeper.place()
            self.sweepers.append(sweeper)

        # TODO: remove later, this is just for show
        # draw lines to closest mine
        '''
        for sweeper in self.sweepers:
            closest_mine, id = sweeper.get_closest_mine()
            settings.board.draw_line(sweeper.position, closest_mine)
        '''

        settings.board.update()



    ######################
    # 
    # The general flow to evolve the population (create a new generation)
    #
    #   a. Create a new population:
    #       1. Selection
    #       2. Crossover
    #       3. Mutation
    #   b. Replace old population with new one
    #   c. Test if end condition is satisfied, if not -> a
    #       ** In this case just run through 50 generations and see how it has changed. Status
    #           - Tot # mines found by Pop
    #           - Distribution of mines found per sweeper
    #           - Rate of mines found (# / Ticks)
    #           - Graph of # mines found (Y) vs. Ticks (X)
    #
    ######################


    def sort_sweepers(self):
        sweeper_fits = [{'id': key, 'fitness': sweeper.fitness} for key, sweeper in enumerate(self.sweepers)]
        self.sweepers_sorted = sorted(sweeper_fits, key=lambda k: k['fitness'], reverse=True)
        self.most_fit = self.sweepers_sorted[0]['id']
        self.best_fitness = self.sweepers_sorted[0]['fitness']

    # uses roulette / random selection to pick a chromosome from the pop
    def get_chromo_roulette(self):
        total_fitness = 0
        sweeper_selection = []
        for sweeper in self.sweepers_sorted:
            # "+1" to include sweepers with 0 fitness (or do we not want to include them...?
            total_fitness += sweeper['fitness'] + 1
            sweeper_selection.extend([sweeper['id']] * (sweeper['fitness'] + 1))

        rand = round(random() * (total_fitness - 1))
        return sweeper_selection[rand]

    def get_chromo_rank_selection(self):
        total_fitness = 0
        sweeper_selection = []
        rank = len(self.sweepers_sorted)
        for sweeper in self.sweepers_sorted:
            total_fitness += rank
            sweeper_selection.extend([sweeper['id']] * rank)
            rank -= 1

        print(sweeper_selection)
        rand = round(random() * (total_fitness - 1))
        return sweeper_selection[rand]

    def crossover(self, mom, dad):
        if random() < inputs.CROSSOVERRATE:
            print("Crossing over")
            xover_pnt = round(random() * (len(mom) - 1))
            kid1 = mom[:xover_pnt] + dad[xover_pnt:]
            kid2 = dad[:xover_pnt] + mom[xover_pnt:]
            return [kid1, kid2]

        print("No crossover")
        return [mom, dad]

    def mutate(self, chromo):
        for i, v in enumerate(chromo):
            if random() < inputs.MUTATIONRATE:
                # print("mutating")
                # pertube
                chromo[i] += uniform(-1,1) * inputs.MAXPERTUBATION
        return chromo


    # evolves the population in 1 generation
    def evolve(self):
        # Repeat until new population size = original population size (complete, new generation)
        # 1. Selection - select 2 parents (weighted to choose ones with better fitness)
        # 2. Crossover - crossover parents to create offspring given crossover probability, else return parents
        # 3. Mutation - mutate the offspring given mutation rate
        # 4. Placement - put new offspring in new population

        print("Evolving {} sweepers!".format(len(self.sweepers)))
        print("Num_mines_found = {}; total_fitness = {}".format(settings.num_mines_found, self.total_fitness))

        # Sort
        self.sort_sweepers()

        new_pop = []

        
        # elitism - take top 2 or 4 sweepers and pass on
        for sweeper in self.sweepers_sorted[0:2]:
            weights = self.sweepers[sweeper['id']].brain.get_weights()
            print("Elite ID: {}".format(sweeper['id']))
            print(weights)
            new = Sweeper()
            new.brain.update_weights(weights)
            new_pop.append(new)


        while len(new_pop) < len(self.sweepers):
            # crossover
            # get 2 parents' weights
            mom = self.sweepers[self.get_chromo_roulette()].brain.get_weights()
            dad = self.sweepers[self.get_chromo_roulette()].brain.get_weights()

            kids = self.crossover(mom, dad)

            # Mutate
            print('\nPre and most mutation:')
            orig_kids = [x[:] for x in kids]
            kids = [self.mutate(x) for x in kids]
            if kids == orig_kids:
                print("no mutation")
            else:
                print("Mutation!")


            # add to new pop
            for kid in kids:
                newkid = Sweeper()
                newkid.brain.update_weights(kid)
                new_pop.append(newkid)


        print("New pop len: {}".format(len(new_pop)))
        print("Old pop len: {}".format(len(self.sweepers)))

        print(self.sweepers_sorted)
        print("Summary for gen {}:".format(self.generation))
        print("total fitness: {} | most fit: {} | best fitness: {}".format(self.total_fitness, self.most_fit, self.best_fitness))
        settings.stats.append({'gen': self.generation, 'mines': self.total_fitness, 'high': self.best_fitness})


        # update population.sweepers to new pop
        self.sweepers = new_pop
        self.sweepers_sorted = []

        self.generation += 1



    # returns the N best genomes
    def get_N_best(self):
        return None

    # update init variables
    def calc_fitness_stats(self):
        return none

    # reset all fitness vars/stats
    def reset(self):
        self.total_fitness = 0
        self.most_fit = 0
        self.best_fitness = 0
        self.worst_fitness = 999999999
        self.avg_fitness = 0
        settings.num_mines_found = 0
