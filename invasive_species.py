import random
import math 
import numpy as np

def seasonal_adjustment(day, amplitude=0.2):
    """
    Calculates how much seasonal adjustment should be added for the king crab's growth rate based off of a sine wave.

    day: The current day of the simulation
    amplitude: The variability of the sine wave

    returns: the calculated seasonal factor
    """
    return 1 + amplitude * math.sin(day * (2 * math.pi / 365))

def calculate_availability(prey, predator, factor=1, m=1):
    """
    Calculates the availability of a specific kind of prey for a predator

    prey: number of available prey
    predator: number of predators alive
    factor: the predation factor of how much that predator consumes the prey
    m: an adjustable scalar for fine-tuning

    returns: the percentage availability for a given prey and predator
    """
    if prey == 0:
        return 0
        
    percent = (predator * factor * m / prey)
    if percent > 1:
        return 1
    else:
        return percent

def king_crab(day, creatures, birth_rate=0.5, death_rate=0.1):
    """
    Calculates the population change for the invasive king crab, as well as its consumption

    day: The current day of the simulation
    creatures: The creatures dictionary it will be affecting
    birth_rate: The birth rate of the king crab
    death_rate: The death rate of the king crab

    returns: An array containing the adjusted creatures dictionary as well as an array with information of the king crab's growth, death, and consumption metrics
    """
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