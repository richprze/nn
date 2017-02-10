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
        gen_start_time = time.time()
        for l in range(0,times):
            # move sweepers to next positions
            found_mine_ids = []
            for sweeper in population.sweepers:
                sweeper.move_sweeper()
                result = sweeper.handle_mines()
                if result: found_mine_ids.append(result)
            '''
            population.ideal.move_sweeper_ideal()
            population.ideal.handle_mines()
            '''
            if inputs.BEST:
                population.best.move_sweeper()
                result = population.best.handle_mines()
                if result: found_mine_ids.append(result)

            # if mines found, get new closest mine for all sweepers that had a found mine
            for sweeper in population.sweepers:
                if sweeper.closest_mine_id in found_mine_ids:
                    sweeper.get_closest_mine()

            # handle for best
            if inputs.BEST:
                if population.best.closest_mine_id in found_mine_ids:
                    population.best.get_closest_mine()
            
            # update fitness and label
            population.total_fitness = settings.num_mines_found # - population.ideal.fitness
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

        # population.ideal.fitness = 0

        if inputs.CANVAS:
            settings.board.reset()
            time.sleep(.5 )
        create_mines()

        # place new sweepers
        if inputs.CANVAS:
            for sweeper in population.sweepers:
                sweeper.place()
            # population.ideal.place('ideal')

        print(population.sweepers)

        if inputs.CANVAS: settings.board.update()

        print("Gen | Mines | High")
        for stat in settings.stats:
            print("{} | {} | {}".format(stat['gen'], stat['mines'], stat['high']))

        print("Gen {} took {} seconds".format(settings.stats[len(settings.stats)-1]['gen'], time.time() - gen_start_time))


    if inputs.CANVAS: settings.board.root.mainloop()
