import random
import math 
import numpy as np

def seasonal_adjustment(day, amplitude=0.2):
    return 1 + amplitude * math.sin(day * (2 * math.pi / 365))

def calculate_availability(prey, predator, factor=1, m=1):
    if prey == 0:
        return 0
        
    percent = (predator * factor * m / prey)
    if percent > 1:
        return 1
    else:
        return percent

def new_king_crab(day, creatures):
    birth_rate = 0.5
    death_rate = 0.1
    carrying_capacity = 800
    predation_factor = {'krill': 200, 'cod': 2}

    # Season
    season_factor = seasonal_adjustment(day)

    # Consumption
    # Krill
    krill_availability = calculate_availability(creatures['krill'], creatures['king crab'], predation_factor['krill'])
    krill_eaten = int(creatures['king crab'] * predation_factor['krill'] * krill_availability * season_factor)
    creatures['krill'] = max(0, creatures['krill'] - krill_eaten)

    # Cod
    cod_availability = calculate_availability(creatures['arctic cod'], creatures['king crab'], predation_factor['cod'], m=1)
    cod_eaten = int(creatures['king crab'] * predation_factor['cod'] * cod_availability * season_factor)
    creatures['arctic cod'] = max(0, creatures['arctic cod'] - cod_eaten)

    # Reproduction
    resource_availability = min(1, (creatures['krill'] + creatures['arctic cod']) / (creatures['king crab'] + 0.0001) * 0.001)
    crab_growth = int(creatures['king crab'] * birth_rate * resource_availability * season_factor)
    creatures['king crab'] += crab_growth

    # Death
    resource_unavailability = 1 - resource_availability
    density = max(0, (creatures['king crab'] - carrying_capacity) / carrying_capacity)
    crab_deaths = int(creatures['king crab'] * (death_rate * (1 + resource_unavailability / 2) + density) * season_factor)
    creatures['king crab'] = max(0, creatures['king crab'] - crab_deaths)

    return (creatures, [crab_growth, crab_deaths, krill_eaten, cod_eaten])