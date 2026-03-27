import numpy as np
import random
import matplotlib.pyplot as plt

def load_matrix_from_triangle(path):
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    idx = 1
    for i in range(n):
        values = list(map(float, lines[idx].split()))
        for j in range(len(values)):
            matrix[i][j] = matrix[j][i] = values[j]
        idx += 1

    return matrix

def evaluate_individual(individual, matrix):
    distance = 0.0
    for i in range(len(individual) - 1):
        city_a = individual[i]
        city_b = individual[i + 1]
        if 0 <= city_a < len(matrix) and 0 <= city_b < len(matrix[0]):
            distance += matrix[city_a][city_b]
        else:
            return float('inf')

    if 0 <= individual[-1] < len(matrix) and 0 <= individual[0] < len(matrix[0]):
        distance += matrix[individual[-1]][individual[0]]
    else:
        return float('inf')

    return distance 

def evaluate_population(population, matrix):
    scores = []
    for individual in population:
        score = evaluate_individual(individual, matrix)
        scores.append(score)
    return scores 

def tournament_selection(population, scores, k):
    new_population = []
    population_size = len(population)

    for _ in range(population_size):
        tournament_indices = random.sample(range(population_size), k)
        tournament_individuals = [population[i] for i in tournament_indices]
        tournament_scores = [scores[i] for i in tournament_indices]

        best_in_tournament_index = tournament_scores.index(min(tournament_scores))
        best_individual = tournament_individuals[best_in_tournament_index]
        new_population.append(best_individual)

    return new_population  

def inversion_mutation(individual):
    size = len(individual)
    point1, point2 = sorted(random.sample(range(size), 2))

    individual[point1:point2] = individual[point1:point2][::-1]
    return individual 

def ox_crossover(parent1, parent2):
    size = len(parent1)
    child1 = [-1] * size
    child2 = [-1] * size

    point1, point2 = sorted(random.sample(range(size), 2))

    child1[point1:point2] = parent1[point1:point2]
    child2[point1:point2] = parent2[point1:point2]

    current_child1_position = point2
    current_parent2_position = point2
    while -1 in child1:
        if current_parent2_position == size:
            current_parent2_position = 0
        gene = parent2[current_parent2_position]
        if gene not in child1:
            if current_child1_position == size:
                current_child1_position = 0
            child1[current_child1_position] = gene
            current_child1_position += 1
        current_parent2_position += 1

    current_child2_position = point2
    current_parent1_position = point2
    while -1 in child2:
        if current_parent1_position == size:
            current_parent1_position = 0
        gene = parent1[current_parent1_position]
        if gene not in child2:
            if current_child2_position == size:
                current_child2_position = 0
            child2[current_child2_position] = gene
            current_child2_position += 1
        current_parent1_position += 1

    return child1, child2 


#MAIN PART OF THE PROGRAM
num_generations = 5000
crossover_probability = 0.8
mutation_probability = 0.1
tournament_k = 5


path = 'a280.txt'
distance_matrix = load_matrix_from_triangle(path)


for i in range(5):
    print(distance_matrix[i][:5])

num_individuals = 100
n_cities = 280

population = []
for _ in range(num_individuals):
    individual = list(range(n_cities))
    random.shuffle(individual)
    population.append(individual)

scores = evaluate_population(population, distance_matrix)

global_best_individual = None
global_best_score = float('inf')
best_score_history = []

print("Starting genetic algorithm")

for generation in range(num_generations):
    new_population_after_selection = tournament_selection(population, scores, tournament_k)

    children = []
    for i in range(0, len(new_population_after_selection), 2):
        parent1 = new_population_after_selection[i]
        if i + 1 < len(new_population_after_selection):
            parent2 = new_population_after_selection[i+1]
        else:
            parent2 = random.choice(new_population_after_selection)

        if random.random() < crossover_probability:
            child1, child2 = ox_crossover(parent1, parent2)
        else:
            child1, child2 = parent1[:], parent2[:]

        if random.random() < mutation_probability:
            child1 = inversion_mutation(child1)
        if random.random() < mutation_probability:
            child2 = inversion_mutation(child2)

        children.extend([child1, child2])

    population = children[:len(population)]
    scores = evaluate_population(population, distance_matrix)

    generation_best_score = min(scores)
    generation_best_index = scores.index(generation_best_score)
    generation_best_individual = population[generation_best_index]

    if generation_best_score < global_best_score:
        global_best_score = generation_best_score
        global_best_individual = generation_best_individual[:]

    best_score_history.append(generation_best_score)

    if (generation + 1) % 100 == 0:
        print(f"Generation {generation + 1}: Best score = {global_best_score}")

print("\nAlgorithm finished.")
print(f"Best found route: {global_best_individual}")
print(f"Best route length: {global_best_score}")


#VISUALIZATION OF RESULTS
print("\nConvergence plot of the genetic algorithm:")
plt.figure(figsize=(10, 6))
plt.plot(best_score_history, color='blue', linewidth=2)
plt.title('Genetic Algorithm Convergence (TSP Problem)', fontsize=14)
plt.xlabel('Generation', fontsize=12)
plt.ylabel('Best route length', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()