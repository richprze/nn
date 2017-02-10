from tkinter import *
from random import random, randint, uniform
from math import exp, pi, sqrt, sin, cos, acos, atan2
import inputs
import settings
import time

# vector maths
def vec_dist(vec1, vec2):
    return sqrt((vec1[0]-vec2[0])**2 + (vec1[1]-vec2[1])**2)

def vec_diff(sweeper, mine):
    # should be [mine] - [sweeper] to get vec direction from sweeper to mine
    return [mine[0]-sweeper[0], mine[1]-sweeper[1]]

def vec_diff_unit(sweeper, mine):
    vec = vec_diff(sweeper, mine)
    mag = vec_dist(sweeper, mine)
    return [x / mag for x in vec]

def vector_angle_to(from_vec, to_vec):
    return atan2(from_vec[1], from_vec[0]) - atan2(to_vec[1], to_vec[0])

def vector_abs_angle(vec1, vec2):
    dot_product = sum(x * y for x, y in zip(vec1, vec2))
    return acos(dot_product)

def obj_tuple(pos, pad):
    return (pos[0] - pad, pos[1] - pad, pos[0] + pad, pos[1] + pad)

def create_mines():
    settings.mines = []
    for i in range(0, inputs.NUMMINES):
        x = round(random() * inputs.XSIZE)
        y = round(random() * inputs.YSIZE)
        if inputs.CANVAS:
            settings.mines.append({'pos': [x, y], 'id': settings.board.place_object('mine', [x, y])})
        else:
            settings.mines.append({'pos': [x, y], 'id': -1})


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
            weights.append(uniform(-1,1))
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
        # Overflow error when -number is > 700
        try:
            ans = (1 / (1 + exp(-number)/1))
        except OverflowError:
            ans = (1 / (1 + exp(700)/1))
            # print("ERROR: overflow with number to sigmoid = {}".format(number))
        return ans

class Sweeper:
    def __init__(self):
        self.brain = NeuralNet(inputs.INPUTS, inputs.OUTPUTS,  inputs.LAYERS, inputs.NEURONS)
        self.fitness = 0

        # random start position & look direction
        self.position = [randint(0,inputs.XSIZE),randint(0,inputs.YSIZE)]
        self.id = -1
        self.boardid = -1 #settings.board.place_object('sweeper', self.position)
        self.rotation = random() * 2 * pi

        self.closest_mine_id = -1
        self.closest_mine = []

        self.get_closest_mine()


    def __repr__(self):
        return "<Sweeper - pos: {}, id: {}, rot: {}, fitness: {}>".format(self.position, self.id, self.rotation, self.fitness)

    def place(self, type='sweeper'):
        self.boardid = settings.board.place_object(type, self.position)

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

        self.closest_mine = closest_mine
        self.closest_mine_id = closest_mine_id

    def move_sweeper(self):
        # get left and right track
        tracks = self.get_output([self.closest_mine[0], self.closest_mine[1], sin(self.rotation), cos(self.rotation)])

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
        if inputs.CANVAS: settings.board.canvas.coords(self.boardid, obj_tuple(self.position, inputs.SWEEPERSIZE))

    def move_sweeper_ideal(self):
        # get nearest mine
        self.get_closest_mine()

        # to move need a direction and a magnitude
        # get angle of rotation to face mine
        # calculate rotational angle in radians (between 0 and 180 deg, 90 deg = straight)
        unit_vec_to_mine = vec_diff_unit(self.position, self.closest_mine)
        sweeper_look = [sin(self.rotation), cos(self.rotation)]  # x,y
        rot_angle_to_mine = vector_angle_to(sweeper_look, unit_vec_to_mine)
        # limit to 90 deg (pi / 2)
        rot_angle = min(pi / 2, max(-1 * pi / 2, rot_angle_to_mine))

        # add to current rotation
        self.rotation += rot_angle
        # new look
        look = [sin(self.rotation), cos(self.rotation)]  # x,y

        # calculate absolute speed / magnitude
        # old - need a way to represent that relationshp between angle and max speed
            # min speed is what happens if rotate 90 degrees
            # max speed is what happens if go straight
            # BUT, max speed should be tempered if sweeper will go past mine
            # BUT, BUT, this is actually handled because the error rate of hitting a mine == the max speed
            #   , so we can never "go past"
        speed = (((pi / 2) - abs(rot_angle)) / (pi / 2) + 1 ) * inputs.MAXSPEED

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
        if inputs.CANVAS: settings.board.canvas.coords(self.boardid, obj_tuple(self.position, inputs.SWEEPERSIZE))

    def handle_mines(self):
        # check if landed on closest mine
        # future - or if land on ANY mine? Because could go in wrong direction
        #           ** If 2 sweepers find same mine, first one in array "gets" it (record this somehow)

        if vec_dist(self.closest_mine, self.position) <= inputs.MAXSPEED:
            # handle it
            self.fitness += 1
            settings.num_mines_found += 1
            if inputs.CANVAS: settings.board.canvas.delete(settings.mines[self.closest_mine_id]['id'])
            x = round(random() * inputs.XSIZE)
            y = round(random() * inputs.YSIZE)
            if inputs.CANVAS:
                settings.mines[self.closest_mine_id] = {'pos': [x, y], 'id': settings.board.place_object('new mine', [x, y])}
            else:
                settings.mines[self.closest_mine_id] = {'pos': [x, y], 'id': -1}
            return self.closest_mine_id
        else:
            return None


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
            if inputs.CANVAS: sweeper.place()
            self.sweepers.append(sweeper)

        # TODO: remove later, this is just for show
        # draw lines to closest mine
        '''
        for sweeper in self.sweepers:
            closest_mine, id = sweeper.get_closest_mine()
            settings.board.draw_line(sweeper.position, closest_mine)
        '''

        # initialize "ideal" sweeper
        # in 500 ticks, ideal sweeper will find around 40 mines
        '''
        ideal = Sweeper()
        if inputs.CANVAS: ideal.place('ideal')
        self.ideal = ideal
        '''
        if inputs.BEST:
            best = Sweeper()
            best.brain.update_weights(inputs.BESTWEIGHTS)
            if inputs.CANVAS: best.place('ideal')
            self.best = best

        if inputs.CANVAS: settings.board.update()



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

    def crossover_average(self, mom, dad):
        if random() < inputs.CROSSOVERRATE:
            print("Crossing over, average")
            kid = [float(x + y) / 2 for x, y in zip(mom, dad)]
            return [kid, kid[:]]

        print("No crossover, average")
        return [mom, dad]

    def crossover_sum(self, mom, dad):
        if random() < inputs.CROSSOVERRATE:
            print("crossing over, sum")
            kid = [x + y for x, y in zip(mom, dad)]
            return [kid, kid[:]]

        print("No crossover, sum")
        return [mom, dad]

    def mutate(self, chromo):
        for i, v in enumerate(chromo):
            if random() < inputs.MUTATIONRATE:
                # pertube
                chromo[i] += uniform(-1,1) * inputs.MAXPERTUBATION

                # OR #
                # Flip sign
                # chromo[i] *= -1
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
        for sweeper in self.sweepers_sorted[0:inputs.NUMELITE]:
            weights = self.sweepers[sweeper['id']].brain.get_weights()
            print("Elite ID: {}, Fitness: {}".format(sweeper['id'], sweeper['fitness']))
            print(weights)
            new = Sweeper()
            new.brain.update_weights(weights)
            new_pop.append(new)


        while len(new_pop) < len(self.sweepers):
            # crossover
            # get 2 parents' weights
            print("Roulette selection:")
            mom_id = self.get_chromo_roulette()
            mom = self.sweepers[mom_id].brain.get_weights()
            dad_id = self.get_chromo_roulette()
            dad = self.sweepers[dad_id].brain.get_weights()
            print("Fitnesses: mom = {} | dad = {}".format(self.sweepers[mom_id].fitness, self.sweepers[dad_id].fitness))

            if inputs.CROSSOVERTYPE == 'point':
                kids = self.crossover(mom, dad)
            elif inputs.CROSSOVERTYPE == 'average':
                kids = self.crossover_average(mom, dad)
            else:
                kids = self.crossover_sum(mom, dad)

            # Mutate
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
        # print("ideal fitness: {}".format(self.ideal.fitness))
        settings.stats.append({'gen': self.generation, 'mines': self.total_fitness, 'high': self.best_fitness})


        # update population.sweepers to new pop
        self.sweepers = new_pop
        self.sweepers_sorted = []

        self.generation += 1


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


class Board():
    def __init__(self):
        self.root = Tk()
        # self.root = parent
        self.canvas = Canvas(self.root, bg="white", height=inputs.YSIZE, width=inputs.XSIZE)
        self.label = Label(self.root, text="Gen: 0 | Tick: 0 | Mines: 0")
        self.label.pack()
        self.canvas.pack()

    def update(self):
        self.canvas.update()

    def place_object(self, obj, pos):
        if obj == 'sweeper':
            pad = inputs.SWEEPERSIZE
            data = {"fill": "", "outline": "green", "width": 1}
        elif obj == 'new mine':
            pad = inputs.MINESIZE
            data = {"fill": "red", "outline": "red"}
        elif obj == 'ideal':
            pad = inputs.SWEEPERSIZE
            data = {"fill": "black", "outline": "black", "width": 1}
        else:
            pad = inputs.MINESIZE
            data = {"fill": "#F5A9A9", "outline": "#F5A9A9"}

        return self.canvas.create_rectangle(obj_tuple(pos, pad), data)

    def draw_line(self, start, end):
        return self.canvas.create_line(start[0], start[1], end[0], end[1], fill="#D6D6D6")

    def reset(self):
        self.canvas.delete('all')
        self.canvas.update()



