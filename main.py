import neat
from game import play
from train import train
from utils.utils import loadFile


config_file = "config/neat-config.txt"
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_file)
genome = loadFile("winner/winner-genome.pkl")

print("Play Flappy Bird\nSelect Option")
print("1. Play")
print("2. Check AI")
print("3. Train New Bird")

choice = int(input("Select 1, 2 or 3: "))

if choice == 1:
    play()
elif choice == 2:
    play(genome, config)
elif choice == 3:
    train(config_file)
