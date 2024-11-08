import numpy as np
import math
import random

creatures = {"baleen whale": 25,
             "krill": 1.35e6,
             "leopard seal": 50,
             "arctic cod": 2000,
             "penguin": 1000,
             "orca": 10,
             "plankton": np.inf  # Infinite Plankton
}

# Functions to represent seasonal variability
def seasonal_adjustment(day, amplitude=0.2):
    return 1 + amplitude * math.sin(day * (2 * math.pi / 365))

def krill(day):
    global creatures
    base_growth_rate = 1.05
    carrying_capacity = 1500000

    # Growth + Season
    season_factor = seasonal_adjustment(day)
    growth_rate = base_growth_rate * season_factor

    # Predation Pressure
    pred_max = 12500 + 1250 + 100
    predation_pressure = (1 - (creatures['arctic cod'] + creatures['penguin'] + creatures['leopard seal']) / ((pred_max + carrying_capacity) / 2))
    predation_pressure = max(predation_pressure, -1)
    growth_rate += predation_pressure

    # Growth
    krill_growth = int(creatures['krill'] * growth_rate)
    krill_growth = min(krill_growth, carrying_capacity)
    creatures['krill'] = krill_growth

    # Failsafe
    if creatures['krill'] < carrying_capacity / 5:
        creatures['krill'] *= 3

def cod(day):
    global creatures
    birth_rate = 0.2
    death_rate = 0.1
    carrying_capacity = 12500
    predation_factor = 20

    # Season
    season_factor = seasonal_adjustment(day)

    if creatures['arctic cod'] != 0:
        # Consumption
        krill_eaten = int(creatures['arctic cod'] * predation_factor * season_factor)
        creatures['krill'] = max(0, creatures['krill'] - krill_eaten)

        # Reproduction
        resource_availability = min(1, creatures['krill'] / (creatures['arctic cod'] + 0.001) * 0.001)
        cod_growth = int(creatures['arctic cod'] * birth_rate * resource_availability * season_factor)
        creatures['arctic cod'] += cod_growth

        # Death
        resource_unavailability = 1 - resource_availability
        density = max(0, (creatures['arctic cod'] - carrying_capacity) / carrying_capacity)
        cod_deaths = int(creatures['arctic cod'] * (death_rate * (1 + resource_unavailability / 2) + density) * season_factor)
        creatures['arctic cod'] = max(0, creatures['arctic cod'] - cod_deaths)

def penguin(day):
    global creatures
    birth_rate = 0.2
    death_rate = 0.1
    carrying_capacity = 1250
    predation_factor = 50

    # Seasonal Adjustment
    season_factor = seasonal_adjustment(day)

    # Consumption
    krill_availability = calculate_availability(creatures['krill'], creatures['penguin'], predation_factor)
    krill_eaten = int(creatures['penguin'] * predation_factor * krill_availability * season_factor)
    creatures['krill'] = max(0, creatures['krill'] - krill_eaten)

    # Reproduction
    resource_availability = min(1, creatures['krill'] / (creatures['penguin'] * 0.001))
    penguin_growth = int(creatures['penguin'] * birth_rate * resource_availability * season_factor)
    creatures['penguin'] += penguin_growth

    # Death
    resource_unavailability = 1 - resource_availability
    density = max(0, (creatures['penguin'] - carrying_capacity) / carrying_capacity)
    penguin_deaths = int(creatures['penguin'] * (death_rate * (1 + resource_unavailability / 2) + density) * season_factor)
    creatures['penguin'] = max(0, creatures['penguin'] - penguin_deaths)

def seal(day):
    global creatures
    birth_rate = 0.2
    death_rate = 0.1
    carrying_capacity = 100
    predation_factor = {'krill': 1000, 'cod': 10}

    # Season
    season_factor = seasonal_adjustment(day)

    # Consumption
    # Krill
    krill_availability = calculate_availability(creatures['krill'], creatures['leopard seal'], predation_factor['krill'])
    krill_eaten = int(creatures['leopard seal'] * predation_factor['krill'] * krill_availability * season_factor)
    creatures['krill'] = max(0, creatures['krill'] - krill_eaten)

    # Cod
    cod_availability = calculate_availability(creatures['arctic cod'], creatures['leopard seal'], predation_factor['cod'], m=5)
    cod_eaten = int(creatures['leopard seal'] * predation_factor['cod'] * cod_availability * season_factor)
    creatures['arctic cod'] = max(0, creatures['arctic cod'] - cod_eaten)

    # Reproduction
    resource_availability = min(1, (creatures['krill'] + creatures['arctic cod']) / (creatures['leopard seal'] + 0.0001) * 0.001)
    seal_growth = int(creatures['leopard seal'] * birth_rate * resource_availability * season_factor)
    creatures['leopard seal'] += seal_growth

    # Death
    resource_unavailability = 1 - resource_availability
    density = max(0, (creatures['leopard seal'] - carrying_capacity) / carrying_capacity)
    seal_deaths = int(creatures['leopard seal'] * (death_rate * (1 + resource_unavailability / 2) + density) * season_factor)
    creatures['leopard seal'] = max(0, creatures['leopard seal'] - seal_deaths)

def calculate_availability(prey, predator, factor, m=1):
    availability = 0
    if prey != 0:
        availability = max(0, 1 - (predator * factor * m / prey))
    return availability

def cycle(day):
    krill(day)
    cod(day)
    penguin(day)
    seal(day)

x, k, p, c = [], [], [], []
def run():
    for i in range(1000):
        if i > 5:
            x.append(i)
            k.append(creatures['krill'])
            p.append(creatures['penguin'])
            c.append(creatures['arctic cod'])
        cycle(day=i)
