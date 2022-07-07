from AI.AI_trainer import AITrainer
from config import MUTATION_LIMIT, GEN_NUMBER

if __name__ == '__main__':
    with open('./log.txt', "w") as file:
        file.write("Start Training \n")
    file.close()
    trainer = AITrainer()
    trainer.train()