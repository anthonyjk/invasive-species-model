import numpy as np
import math
import random
import pandas as pd
from invasive_species import king_crab

creatures = {"baleen whale": 25,
             "krill": 1.45e6,
             "leopard seal": 50,
             "arctic cod": 10000,#3000,
             "penguin": 1000,
             "orca": 10,
             "plankton": np.inf  # Infinite Plankton
}

# Functions to represent seasonal variability
def seasonal_adjustment(day, amplitude=0.2):
    """
    Calculates how much seasonal adjustment should be added for each animal's growth rates based off of a sine wave.

    day: The current day of the simulation
    amplitude: The variability of the sine wave

    returns: the calculated seasonal factor
    """
    return 1 + amplitude * math.sin(day * (2 * math.pi / 365))

def krill(day, base_growth_rate=1.05):
    """
    Calculates the population growth for krill

    day: The current day of the simulation
    base_growth_rate: The set growth rate for the krill

    returns: The number of krill the population grew by
    """
    global creatures
    carrying_capacity = 2000000

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

    return krill_growth

def cod(day, birth_rate=1.5, death_rate=0.1):
    """
    Calculates the population change for arctic cod, as well as its consumption

    day: The current day of the simulation
    birth rate: The set birth rate for the cod
    death rate: The set death rate for the cod

    returns: An array containing information of its growth, death, and consumption metrics
    """
    global creatures
    carrying_capacity = 20000
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

        return [cod_growth, cod_deaths, krill_eaten]
    return [0, 0, 0]

def penguin(day):
    """
    Calculates the population change for the penguin, as well as its consumption

    day: The current day of the simulation

    returns: An array containing information of its growth, death, and consumption metrics
    """
    global creatures
    birth_rate = 0.4
    death_rate = 0.1
    carrying_capacity = 1250
    predation_factor = 50

    # Season
    season_factor = seasonal_adjustment(day)

    # Consumption
    krill_availability = calculate_availability(creatures['krill'], creatures['penguin'], predation_factor)
    krill_eaten = int(creatures['penguin'] * predation_factor * krill_availability * season_factor)
    creatures['krill'] = max(0, creatures['krill'] - krill_eaten)

    # Reproduction
    resource_availability = min(1, creatures['krill'] / (creatures['penguin'] * 0.001 + 0.0001))
    penguin_growth = int(creatures['penguin'] * birth_rate * resource_availability * season_factor)
    creatures['penguin'] += penguin_growth

    # Death
    resource_unavailability = 1 - resource_availability
    density = max(0, (creatures['penguin'] - carrying_capacity) / carrying_capacity)
    penguin_deaths = int(creatures['penguin'] * (death_rate * (1 + resource_unavailability / 2) + density) * season_factor)
    creatures['penguin'] = max(0, creatures['penguin'] - penguin_deaths)

    return [penguin_growth, penguin_deaths, krill_eaten]

def seal(day, birth_rate=0.3, death_rate=0.05):
    """
    Calculates the population change for the leopard seal, as well as its consumption

    day: The current day of the simulation
    birth_rate: The seal's set birth rate
    death_rate: The seal's set death rate

    returns: An array containing information of its growth, death, and consumption metrics
    """
    global creatures
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
    cod_availability = calculate_availability(creatures['arctic cod'], creatures['leopard seal'], predation_factor['cod'], m=2)
    cod_eaten = int(creatures['leopard seal'] * predation_factor['cod'] * cod_availability * season_factor)
    creatures['arctic cod'] = max(0, creatures['arctic cod'] - cod_eaten)

    # Reproduction
    resource_availability = min(1, (creatures['krill'] + creatures['arctic cod']) / (creatures['leopard seal'] + 0.0001) * 0.0001)
    seal_growth = int(creatures['leopard seal'] * birth_rate * resource_availability * season_factor)
    creatures['leopard seal'] += seal_growth

    # Death
    resource_unavailability = 1 - resource_availability
    density = max(0, (creatures['leopard seal'] - carrying_capacity) / carrying_capacity)
    seal_deaths = int(creatures['leopard seal'] * (death_rate * (1 + resource_unavailability / 2) + density) * season_factor)
    creatures['leopard seal'] = max(0, creatures['leopard seal'] - seal_deaths)

    return [seal_growth, seal_deaths, krill_eaten, cod_eaten]

def orca(day):
    """
    Calculates the population change for the orca, as well as its consumption

    day: The current day of the simulation

    returns: An array containing information of its growth, death, and consumption metrics
    """
    global creatures
    birth_rate = 0.2
    death_rate = 0.15
    carrying_capacity = 20
    predation_factor = {'cod': 25, 'penguin': 10, 'leopard seal': 1}

    # Season
    season_factor = seasonal_adjustment(day)

    # Consumption
    # Cod
    cod_availability = calculate_availability(creatures['arctic cod'], creatures['orca'], predation_factor['cod'], m = 5)
    cod_eaten = int(creatures['orca'] * predation_factor['cod'] * cod_availability * season_factor)
    creatures['arctic cod'] = max(0, creatures['arctic cod'] - cod_eaten)

    # Penguin
    penguin_availability = calculate_availability(creatures['penguin'], creatures['orca'], predation_factor['penguin'])
    penguin_eaten = int(creatures['orca'] * predation_factor['penguin'] * penguin_availability * season_factor)
    creatures['penguin'] = max(0, creatures['penguin'] - penguin_eaten)

    # Seal
    seal_availability = calculate_availability(creatures['leopard seal'], creatures['orca'], predation_factor['leopard seal'])
    seal_eaten = int(creatures['orca'] * predation_factor['leopard seal'] * seal_availability * season_factor)
    creatures['leopard seal'] = max(0, creatures['leopard seal'] - seal_eaten)

    # Reproduction
    resource_availability = min(1, (creatures['leopard seal'] + creatures['arctic cod'] + creatures['penguin']) / (creatures['orca'] + 0.0001) * 0.01)
    orca_growth = int(creatures['orca'] * birth_rate * resource_availability * season_factor)
    creatures['orca'] += orca_growth

    # Death
    resource_unavailability = 1 - resource_availability
    density = max(0, (creatures['orca'] - carrying_capacity) / carrying_capacity)
    orca_deaths = int(creatures['orca'] * (death_rate * (1 + resource_unavailability / 2) + density) * season_factor)
    creatures['orca'] = max(0, creatures['orca'] - orca_deaths)

    return [orca_growth, orca_deaths, cod_eaten, penguin_eaten, seal_eaten]

def whale(day):
    """
    Calculates the population change for the baleen whale, as well as its consumption

    day: The current day of the simulation

    returns: An array containing information of its growth, death, and consumption metrics
    """
    global creatures
    birth_rate = 0.2
    death_rate = 0.1
    carrying_capacity = 50
    predation_factor = {'krill': 10000}

    # Season
    season_factor = seasonal_adjustment(day)

    # Consumption
    # Krill
    krill_availability = calculate_availability(creatures['krill'], creatures['baleen whale'], predation_factor['krill'])
    krill_eaten = int(creatures['baleen whale'] * predation_factor['krill'] * krill_availability * season_factor)
    creatures['krill'] = max(0, creatures['krill'] - krill_eaten)

    # Reproduction
    resource_availability = min(1, (creatures['krill']) / (creatures['baleen whale'] + 0.0001) * 0.00001)
    whale_growth = int(creatures['baleen whale'] * birth_rate * resource_availability * season_factor)
    creatures['baleen whale'] += whale_growth

    # Death
    resource_unavailability = 1 - resource_availability
    density = max(0, (creatures['baleen whale'] - carrying_capacity) / carrying_capacity)
    whale_deaths = int(creatures['baleen whale'] * (death_rate * (1 + resource_unavailability / 2) + density) * season_factor)
    creatures['baleen whale'] = max(0, creatures['baleen whale'] - whale_deaths)

    return [whale_growth, whale_deaths, krill_eaten]

def calculate_availability(prey, predator, factor, m=1):
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

    demand = predator * factor * m

    if demand == 0:
        return 0
    availability_percentage = min(1, prey / demand)
    
    return availability_percentage

eco_data = pd.DataFrame([])
crab_data = pd.DataFrame([])
def run(invasive=False, cod_birth_rate=1.5, cod_death_rate=0.1):
    '''
    Runs the simulation and adds the return information from each function to a pandas dataframe

    invasive: Whether the invasive king crab species should be included in the simulation
    cod_birth_rate: the birth rate of the cod
    cod_death_rate: the death rate of the cod

    returns: None
    '''
    global eco_data, creatures
    step = []
    krill_pop, krill_growth = [], []
    penguin_pop, penguin_growth, penguin_death, penguin_krill_consumed = [], [], [], []
    cod_pop, cod_growth, cod_death, cod_krill_consumed = [],[],[],[]
    seal_pop, seal_growth, seal_death, seal_krill_consumed, seal_cod_consumed = [],[],[],[],[]
    orca_pop, orca_growth, orca_death, orca_cod_consumed, orca_penguin_consumed, orca_seal_consumed = [], [], [], [], [], []
    whale_pop, whale_growth, whale_death, whale_krill_consumed = [],[],[],[]

    if invasive:
        creatures['king crab'] = 25
        crab_pop, crab_growth, crab_death, crab_krill_consumed, crab_cod_consumed = [],[],[],[],[]
    
    for i in range(int(365*5)): # 5 Years
        day = i+1
        step.append(day)
        # Population Tracking
        krill_pop.append(creatures['krill'])
        penguin_pop.append(creatures['penguin'])
        cod_pop.append(creatures['arctic cod'])
        seal_pop.append(creatures['leopard seal'])
        orca_pop.append(creatures['orca'])
        whale_pop.append(creatures['baleen whale'])
        if invasive:
            crab_pop.append(creatures['king crab'])
        # Other Variables
        # Krill
        krill_growth.append(krill(day))

        # Penguin
        g, d, kc = penguin(day)
        penguin_growth.append(g)
        penguin_death.append(d)
        penguin_krill_consumed.append(kc)

        # Arctic Cod
        g, d, kc = cod(day, cod_birth_rate, cod_death_rate)
        cod_growth.append(g)
        cod_death.append(d)
        cod_krill_consumed.append(kc)

        # Leopard Seal
        g, d, kc, cc = seal(day)
        seal_growth.append(g)
        seal_death.append(d)
        seal_krill_consumed.append(kc)
        seal_cod_consumed.append(cc)

        # Orca
        g, d, cc, pc, sc = orca(day)
        orca_growth.append(g)
        orca_death.append(d)
        orca_cod_consumed.append(cc)
        orca_penguin_consumed.append(pc)
        orca_seal_consumed.append(sc)

        # Whale
        g, d, kc = whale(day)
        whale_growth.append(g)
        whale_death.append(d)
        whale_krill_consumed.append(kc)

        # King Crab (Invasive)
        if invasive:
            creatures, data = king_crab(day, creatures)
            g, d, kc, cc = data
            crab_growth.append(g)
            crab_death.append(d)
            crab_krill_consumed.append(kc)
            crab_cod_consumed.append(cc)
        if day > 0:
            pass
            #print(creatures)

    eco_data = pd.DataFrame({
    'step': step,
    'krill_pop': krill_pop,
    'krill_growth': krill_growth,
    'penguin_pop': penguin_pop,
    'penguin_growth': penguin_growth,
    'penguin_death': penguin_death,
    'penguin_krill_consumed': penguin_krill_consumed,
    'cod_pop': cod_pop,
    'cod_growth': cod_growth,
    'cod_death': cod_death,
    'cod_krill_consumed': cod_krill_consumed,
    'seal_pop': seal_pop,
    'seal_growth': seal_growth,
    'seal_death': seal_death,
    'seal_krill_consumed': seal_krill_consumed,
    'seal_cod_consumed': seal_cod_consumed,
    'orca_pop': orca_pop,
    'orca_growth': orca_growth,
    'orca_death': orca_death,
    'orca_cod_consumed': orca_cod_consumed,
    'orca_penguin_consumed': orca_penguin_consumed,
    'orca_seal_consumed': orca_seal_consumed,
    'whale_pop': whale_pop,
    'whale_growth': whale_growth,
    'whale_death': whale_death,
    'whale_krill_consumed': whale_krill_consumed
    })

    if invasive:
        crab_data = pd.DataFrame({
            'step': step,
            'crab_pop': crab_pop,
            'crab_growth': crab_growth,
            'crab_death': crab_death,
            'crab_krill_consumed': crab_krill_consumed,
            'crab_cod_consumed': crab_cod_consumed
        })

def reset_pops():
    """
    Resets the population of the ecosystem back to its inital state
    """
    global creatures
    creatures = {"baleen whale": 25,
             "krill": 1.45e6,
             "leopard seal": 50,
             "arctic cod": 10000,#3000,
             "penguin": 1000,
             "orca": 10,
             "plankton": np.inf  # Infinite Plankton
    }