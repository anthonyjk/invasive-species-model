# Ecosystem model
import numpy as np
import random

creatures = {"baleen whale":25,
             "krill":1000000,
             "leopard seal": 25,
             "arctic cod": 10000,
             "penguin": 750,
             "orca":10,
             "plankton": np.inf # Infinite Plankton
}

def krill():
    # https://marinesanctuary.org/blog/krill-behavior-diet-lifecycle/
    pass
    # increase pop number by random amount from source

def arctic_cod():
    #
    pass
    # increase pop number by random amount
    # decrease krill pop by related number
    # ex: growth of 25, kills 10,000 krill

def leopard_seal():
    pass

def penguin():
    pass


def orca(weight, step=1): # STEP = HOW MANY DAYS IN A STEP
    global creatures
    # https://seaworld.org/animals/all-about/killer-whale/diet/
    # 1 - 3.5% of body mass per day (step)
    # average mass of an orca: 6,600 -> 8,800
    intake_max = random.uniform(.01, .035) * weight
    intake_max *= step

    # Mass in Pounds
    penguin_mass = 75 # https://seaworld.org/animals/facts/birds/penguins/
    cod_mass = 48
    seal_mass = 815

    # Consumption
    consumed = 0

    while consumed < intake_max:

        prey_total = creatures['penguin'] + creatures['leopard seal'] + creatures['arctic cod']
        p_weight = creatures['penguin'] / prey_total
        s_weight = creatures['leopard seal'] / prey_total
        c_chance = creatures['arctic cod'] / prey_total
        
        prey = random.choices(
            population=['p', 's', 'c'],
            weights = [p_weight, s_weight, c_chance]
        )[0] # Need 0 to get rid of array type
        if prey == 'p':
            creatures['penguin'] -= 1
            consumed += penguin_mass
        elif prey == 's':
            creatures['leopard seal'] -= 1
            consumed += seal_mass
        elif prey == 'c':
            creatures['arctic cod'] -= 1
            consumed += cod_mass

    # Reproduction
    # https://www.nationalgeographic.com/animals/mammals/facts/orca
    # 3 - 10 years for 1 baby
    # Using 6.5 years
    yrs = 6.5
    reproduce_chance = step / (yrs * 365.25)

    birth = random.choices(
        population=[0,1],
        weights = [1 - reproduce_chance, reproduce_chance]
    )[0]
    if birth == 1:
        creatures['orca'] += 1

def baleen_whale(step=1):
    global creatures
    creatures['baleen_whale']
    # baleen whales only eat krill

    # Reproduction
    # https://baleinesendirect.org/en/discover/life-of-whales/behaviour/reproduction/
    # Gives birth every 1.5 - 3 years
    # Using 2 years
    yrs = 2
    reproduce_chance = step / (yrs * 365.25)
    birth = random.choices(
        population=[0,1],
        weights = [1 - reproduce_chance, reproduce_chance]
    )[0]
    if birth == 1:
        creatures['baleen_whale'] += 1

    
