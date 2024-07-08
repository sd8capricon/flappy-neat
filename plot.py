import neat
import pickle
import numpy as np
import matplotlib.pyplot as plt

def loadFile(name):
    path = "winner/{name}".format(name=name)
    with open(path, "rb") as f:
        stats = pickle.load(f)
    return stats

def plot_stats(stats: neat.StatisticsReporter):
    generations = range(len(stats.most_fit_genomes))
    best_fitness = [c.fitness for c in stats.most_fit_genomes]
    avg_fitness = stats.get_fitness_mean()
    std_fitness = stats.get_fitness_stdev()

    plt.figure(figsize=(10, 5))
    plt.plot(generations, best_fitness, label="Best Fitness")
    plt.plot(generations, avg_fitness, label="Average Fitness")
    plt.plot(generations, std_fitness, label="Std Deviation")

    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Fitness over Generations")
    plt.legend()
    plt.show()

def plot_species(statistics):
    """ Visualizes speciation throughout evolution. """

    species_sizes = statistics.get_species_sizes()
    num_generations = len(species_sizes)
    curves = np.array(species_sizes).T

    fig, ax = plt.subplots()
    ax.stackplot(range(num_generations), *curves)

    plt.title("Speciation")
    plt.ylabel("Size per Species")
    plt.xlabel("Generations")

    plt.show()

stats = loadFile("stat.pkl")
genome = loadFile("winner-genome")
config_file = "config.txt"

plot_stats(stats)
plot_species(stats)