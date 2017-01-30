from random import random
from nn_classes import Population, Sweeper, obj_tuple, Board, create_mines
import time
import inputs
import settings

if __name__ == '__main__':

    times = inputs.NUMTICKS  
    gens = inputs.GENERATIONS # of generations to evolve; 1 = no evolution

    if inputs.CANVAS: settings.board = Board()
    create_mines()

    population = Population()

    last_update = time.time()
    for k in range(0,gens):
        print("Starting generation: {}".format(population.generation))
        for l in range(0,times):
            # move sweepers to next positions
            for sweeper in population.sweepers:
                sweeper.move_sweeper()
                sweeper.handle_mines()
            # update fitness and label
            population.total_fitness = settings.num_mines_found
            if inputs.CANVAS:
                settings.board.label.configure(text="Gen: {} | Tick: {} | Mines: {}".format(population.generation, l+1, settings.num_mines_found))
                # wait for 1 / FPS seconds to pass
                delta = time.time() - last_update
                time.sleep(max(0,1/inputs.FPS - delta))
                # update board
                settings.board.update()

                last_update = time.time()

        # EVOLVE + UPDATE pop
        population.evolve()

        population.reset()
        if inputs.CANVAS:
            settings.board.reset()
            time.sleep(.5 )
        create_mines()

        # place new sweepers
        if inputs.CANVAS:
            for sweeper in population.sweepers:
                sweeper.place()

        print(population.sweepers)

        if inputs.CANVAS: settings.board.update()

        print("Gen | Mines | High")
        for stat in settings.stats:
            print("{} | {} | {}".format(stat['gen'], stat['mines'], stat['high']))


    if inputs.CANVAS: settings.board.root.mainloop()
