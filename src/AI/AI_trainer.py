import random
import config
import random
from AI.AI_player import AIPlayer
from AI.tournament import Tournament

class AITrainer():
    def __init__(self):
        pass

    # The main func of training the bots. Starts with default values of the gens,
    # and runs a tournament the number of gen_number, that shows in config
    def train(self):
        default_board_coefficients_1 = [500, 200, 100, 50, 10, 0.1, 0.1, -100, -200, 25]
        default_board_coefficients_2 = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        default_bonus_size = 25
        default_penalty_coefficient = 10 

        parent_1 = AIPlayer(default_board_coefficients_1, default_bonus_size, default_penalty_coefficient)
        parent_2 = AIPlayer(default_board_coefficients_2, default_bonus_size, default_penalty_coefficient)

        for i in range(config.GEN_NUMBER):
            print(f"Training generation {i}")
            gen_list = self.create_gen_list(parent_1, parent_2)
            self.create_tournament(gen_list)
            parent_1, parent_2 = self.get_best_survivors(gen_list)
            with open('./log.txt', "a") as file:
                file.write(f"Generation {i} \n")
                file.write(f"Parent 1: \n Board Coefficients: {parent_1.board_coefficients} \n Bonus Size: {parent_1.bonus_size} \n Penalty Coefficient: {parent_1.penalty_coefficient} \n Fitness: {parent_1.fitness_score}")
                file.write(f"Parent 2: \n Board Coefficients: {parent_2.board_coefficients} \n Bonus Size: {parent_2.bonus_size} \n Penalty Coefficient: {parent_2.penalty_coefficient} \n Fitness: {parent_2.fitness_score}")
                file.write(f"End generation {i} \n\n")
            file.close()
            
            print(f"Parent 1: \n Board Coefficients: {parent_1.board_coefficients} \n Bonus Size: {parent_1.bonus_size} \n Penalty Coefficient: {parent_1.penalty_coefficient} \n Fitness: {parent_1.fitness_score}")
            print(f"Parent 2: \n Board Coefficients: {parent_2.board_coefficients} \n Bonus Size: {parent_2.bonus_size} \n Penalty Coefficient: {parent_2.penalty_coefficient} \n Fitness: {parent_2.fitness_score}")

            parent_1.reset_fitness()
            parent_2.reset_fitness()

    # Returns a gen_list, that contains its parents, and mutated them. 
    def create_gen_list(self, parent_1, parent_2):
        gen_list = [parent_1, parent_2]
        for i in range(config.GEN_SIZE - len(gen_list)):
            survivor = self.mutation(parent_1, parent_2)
            gen_list.append(survivor)
        return gen_list

    # Creates a tournament by creating an instance of Tournament class with gen_list.
    def create_tournament(self, gen_list):
        gen_tournament = Tournament(gen_list)
        gen_tournament.start_tournament(gen_list)

    # Locates and returns the 2 best survivors in the gen by sorting their fitness scores
    def get_best_survivors(self, survivor_list: list[AIPlayer]):
        survivor_list.sort(key=lambda AIPlayer: AIPlayer.fitness_score, reverse=True)
        best_player = survivor_list[0]
        second_best_player = survivor_list[1]

        return best_player, second_best_player

    # Returns a survivor with randomally changed weights from 2 parents (best survivors)
    def mutation(self, parent_1: AIPlayer, parent_2: AIPlayer):
        if random.uniform(0, 1) <= config.CROSSOVER_CHANCE:
            parent = self.crossover(parent_1, parent_2)
        else:
            parent = random.choice([parent_1, parent_2])

        board_coefficients = parent.get_board_coefficients()
        bonus_size = parent.get_bonus_size()
        penalty_coefficient = parent.get_penalty_coefficient()

        mutated_board_coefficients = []
        for coefficient in board_coefficients:
            if random.uniform(0, 1) <= config.MUTATION_CHANCE:
                mutated_board_coefficients.append(coefficient + coefficient * random.uniform(- config.MUTATION_LIMIT, config.MUTATION_LIMIT))
            else:
                mutated_board_coefficients.append(coefficient)

        if random.uniform(0, 1) <= config.MUTATION_CHANCE:
            mutated_bonus_size = bonus_size + bonus_size * random.uniform(- config.MUTATION_LIMIT, config.MUTATION_LIMIT)
        else:
            mutated_bonus_size = bonus_size

        if random.uniform(0, 1) <= config.MUTATION_CHANCE:
            mutated_penalty_coefficient = penalty_coefficient + penalty_coefficient * random.uniform(- config.MUTATION_LIMIT, config.MUTATION_LIMIT)
        else:
            mutated_penalty_coefficient = penalty_coefficient

        return AIPlayer(mutated_board_coefficients, mutated_bonus_size, mutated_penalty_coefficient)

    # Returns a crossover parent from parent_1 and parent_2. 
    # The amout of gens from each parent in the crossover is equal
    def crossover(self, parent_1: AIPlayer, parent_2: AIPlayer):
        count_1 = 0
        count_2 = 0
        board_coefficient = []
        board_coefficient_1 = parent_1.get_board_coefficients()
        board_coefficient_2 = parent_2.get_board_coefficients()

        for i in range (len(board_coefficient_1)):
            if random.uniform(0, 1) <= 0.5 and count_1 <= 5:
                    board_coefficient.append(board_coefficient_1[i])
                    count_1 += 1
            else:
                    board_coefficient.append(board_coefficient_2[i])
                    count_2 += 1
        
        if random.uniform(0, 1) <= 0.5 and count_1 <= 5:
            bonus = parent_1.get_bonus_size()
            count_1 += 1
        else:
            bonus = parent_2.get_bonus_size()
            count_2 += 1
        
        if random.uniform(0, 1) <= 0.5 and count_1 <= 5:
            penalty = parent_1.get_penalty_coefficient()
            count_1 += 1
        else:
            penalty = parent_2.get_penalty_coefficient()
            count_2 += 1
        
        return AIPlayer(board_coefficient, bonus, penalty)