import pandas as pd
import matplotlib.pyplot as plt
import math
import random

NUMBER_OF_CITIES = 30
INITIAL_TEMPERATURE = 15000.0
COOLING_RATE = 0.004

columns = [6, 17, 18, 20]
df = pd.read_csv('cities.csv', header=0, usecols=columns)
df = df.sort_values('Население', ascending=False, na_position='last')
df = df[0:NUMBER_OF_CITIES]
df = df.reset_index(drop=True)
print(df)


def get_km(lat1, lat2, lon1, lon2):
    radius = 6373.0
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    t = math.sin((lat2 - lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1)/2)**2
    return 2 * radius * math.atan2(math.sqrt(t), math.sqrt(1 - t))


def get_distance(index1, index2):
    lat1 = df.iloc[index1]['Широта']
    lat2 = df.iloc[index2]['Широта']
    lon1 = df.iloc[index1]['Долгота']
    lon2 = df.iloc[index2]['Долгота']
    return get_km(lat1, lat2, lon1, lon2)


def get_solution_length(solution):
    length = 0.0
    for i in range(NUMBER_OF_CITIES - 1):
        length += get_distance(solution[i], solution[i+1])
    length += get_distance(solution[NUMBER_OF_CITIES - 1], solution[0])
    return length


# Returns true if we should change current solution, false otherwise
def choose_solution(current_length, new_length, temperature):
    if new_length < current_length:
        return True
    return math.exp((current_length - new_length) / temperature) > random.random()


def perform_annealing():
    temp = INITIAL_TEMPERATURE
    current_solution = random.sample(range(NUMBER_OF_CITIES), NUMBER_OF_CITIES)
    plot_points = list()
    plot_points.append(list())
    plot_points.append(list())
    epochs = 0
    while temp > 1:
        epochs += 1
        if random.random() < 0.01:
            print('Current temperature', temp)
            plot_points[0].append(epochs)
            plot_points[1].append(get_solution_length(current_solution))
        [first_index, second_index] = sorted(random.sample(range(NUMBER_OF_CITIES), 2))
        first_city = current_solution[first_index]
        second_city = current_solution[second_index]
        new_solution = current_solution.copy()
        new_solution[first_index] = second_city
        new_solution[second_index] = first_city

        if choose_solution(get_solution_length(current_solution), get_solution_length(new_solution), temp):
            current_solution = new_solution.copy()

        plot_points[0].append(epochs)
        plot_points[1].append(get_solution_length(current_solution))

        temp *= (1 - COOLING_RATE)
    print('Best found solution:')
    print(current_solution)
    print('Length:')
    print(get_solution_length(current_solution))
    print('Number of epochs:')
    print(epochs)
    print("Cooling rate:")
    print(COOLING_RATE)
    fig = plt.figure()
    ax = fig.subplots()
    ax.set_xlabel('epochs')
    ax.set_ylabel('total length')
    ax.plot(plot_points[0], plot_points[1])
    plt.show()


print('Annealing has started. Initial temperature is:', INITIAL_TEMPERATURE)
perform_annealing()


