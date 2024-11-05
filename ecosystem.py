# Ecosystem model
import numpy as np
import random

creatures = {"baleen whale":25,
             "krill":100000000,
             "leopard seal": 25,
             "arctic cod": 10000,
             "penguin": 750,
             "orca":10,
             "plankton": np.inf # Infinite Plankton
}

def krill(step=1):
    global creatures
    # Eat plankton

    # Reproduce
    creatures['krill'] += 10000 * int(creatures['krill'] / 2) * step # 10K reproduce a day per krill

def arctic_cod():
    # https://waves-vagues.dfo-mpo.gc.ca/library-bibliotheque/40695827.pdf
    # No solid source on how many lbs cod eat a day
    # Guess: 1% of bodyweight
    # estimate: ~ 1920 krill eaten per day (per cod)
    for i in range(creatures['arctic cod']):
        creatures['krill'] -= 1920

    # Reproduction
    # thousands of eggs, annually
    mates = int(creatures['arctic cod'] / 2)
    for i in range(mates):
        creatures['arctic cod'] += random.randint(500, 1500)

    # DEATH
    # live 7 years
    yrs = 7
    death_chance = step / (yrs * 365.25)
    for i in range(creatures['arctic cod']):
        death = random.choices(
            population=[0,1],
            weights = [1 - death_chance, death_chance]
        )[0]
        creatures['arctic cod'] -= death


    

def leopard_seal(step=1):
    global creatures
    # Leopard seals eat 4-6% of their bodyweight a day
    # however they do not eat during molten season, so we will adjust as 3.5 to 5%
    # SOURCE https://www.fisheries.noaa.gov/species/gray-seal
    cod_mass = 48
    krill_mass = .0025

    # Consumption
    for i in range(creatures['leopard_seal']):
        weight = random.randint(650, 800)
        intake_max = random.uniform(.035, .05) * weight
        intake_max *= step
        
        consumed = 0
        while consumed < intake_max:
            
            prey_total = creatures['krill'] + creatures['arctic cod']
            k_weight = creatures['krill'] / prey_total
            c_weight = creatures['arctic cod'] / prey_total
            
            prey = random.choices(
                population=['k', 'c'],
                weights = [k_weight, c_weight]
            )[0] # Need 0 to get rid of array type
            if prey == 'k':
                creatures['krill'] -= 1
                consumed += krill_mass
            elif prey == 'c':
                creatures['arctic cod'] -= 1
                consumed += cod_mass

    # Reproduction
    # https://animaldiversity.org/accounts/Hydrurga_leptonyx
    # once, yearly
    yrs = 1
    reproduce_chance = step / (yrs * 365.25)
    mates = int(creatures['leopard seal'] / 2)
    for i in range(mates):
        birth = random.choices(
            population=[0,1],
            weights = [1 - reproduce_chance, reproduce_chance]
        )[0]
        creatures['leopard seal'] += birth

    # DEATH
    # https://www.antarctica.gov.au/about-antarctica/animals/seals/leopard-seal
    # live 26 years
    yrs = 26
    death_chance = step / (yrs * 365.25)
    for i in range(creatures['leopard seal']):
        death = random.choices(
            population=[0,1],
            weights = [1 - death_chance, death_chance]
        )[0]
        creatures['leopard seal'] -= death
    

def penguin(step=1):
    global creatures
    # https://www.aquariumofpacific.org/onlinelearningcenter/species/emperor_penguin
    # consume 4.4 to 11 lbs a day
    for i in range(creatures['penguin']):
        intake_max = random.uniform(4.4, 11) * step
    
        # Krill weigh .0025 lbs
        krill_cons = 0
        lbs_eaten = 0
        while lbs_eaten < intake_max:
            lbs_eaten += .0025
            krill_cons += 1
    
        creatures['krill'] -= krill_cons

    # Reproduction
    # https://www.newquayzoo.org.uk/blog/5-surprising-facts-you-didnt-know-about-penguin-eggs
    # 2 eggs per year
    rep_chance = .33
    mates = int(creatures['penguin'] / 2)
    for i in range(mates):
        birth = random.choices(
            population=[0,1,2],
            weights = [rep_chance, rep_chance, rep_chance]
        )[0]
        creatures['penguin'] += birth

    # DEATH
    # Penguins live 15 - 20 years
    # We will use 16 years
    yrs = 16
    death_chance = step / (yrs * 365.25)
    for i in range(creatures['penguin']):
        death = random.choices(
            population=[0,1],
            weights = [1 - death_chance, death_chance]
        )[0]
        creatures['penguin'] -= death
    

def orca(step=1): # STEP = HOW MANY DAYS IN A STEP
    global creatures
    # https://seaworld.org/animals/all-about/killer-whale/diet/
    # 1 - 3.5% of body mass per day (step)
    # average mass of an orca: 6,600 -> 8,800

    # Mass in Pounds
    penguin_mass = 75 # https://seaworld.org/animals/facts/birds/penguins/
    cod_mass = 48
    seal_mass = 815

    # Consumption
    for i in range(creatures['orca']):
        consumed = 0

        weight = random.randint(6600, 8800)
        intake_max = random.uniform(.01, .035) * weight
        intake_max *= step
    
        while consumed < intake_max:
    
            prey_total = creatures['penguin'] + creatures['leopard seal'] + creatures['arctic cod']
            p_weight = creatures['penguin'] / prey_total
            s_weight = creatures['leopard seal'] / prey_total
            c_weight = creatures['arctic cod'] / prey_total
            
            prey = random.choices(
                population=['p', 's', 'c'],
                weights = [p_weight, s_weight, c_weight]
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
    mates = int(creatures['orca'] / 2)
    for i in range(mates):
        birth = random.choices(
            population=[0,1],
            weights = [1 - reproduce_chance, reproduce_chance]
        )[0]
        creatures['orca'] += birth

    # DEATH
    # Orcas live 50 - 90 years
    # We will use 75
    yrs = 75
    death_chance = step / (yrs * 365.25)
    for i in range(creatures['orca']):
        death = random.choices(
            population=[0,1],
            weights = [1 - death_chance, death_chance]
        )[0]
        creatures['orca'] -= death

def baleen_whale(step=1):
    global creatures
    # baleen whales only eat krill
    # intake: 2600 lbs
    # source: https://seaworld.org/animals/all-about/baleen-whales/diet
    # krill weight 0.0025 pounds
    # thus, eats 1040000 krill a day
    for i in range(creatures['baleen whale']):
        creatures['krill'] -= 1040000

    # Reproduction
    # https://baleinesendirect.org/en/discover/life-of-whales/behaviour/reproduction/
    # Gives birth every 1.5 - 3 years
    # Using 2 years
    yrs = 2
    reproduce_chance = step / (yrs * 365.25)
    mates = int(creatures['baleen_whale'] / 2)
    for i in range(mates):
        birth = random.choices(
            population=[0,1],
            weights = [1 - reproduce_chance, reproduce_chance]
        )[0]
        if birth == 1:
            creatures['baleen_whale'] += 1

    # DEATH
    # Baleen whales lifespan is unknown, but we will estimate using other whales
    # Guess: 80 years
    yrs = 80
    death_chance = step / (yrs * 365.25)
    for i in range(creatures['baleen_whale']):
        death = random.choices(
            population=[0,1],
            weights = [1 - death_chance, death_chance]
        )[0]
        creatures['baleen_whale'] -= death

def cycle():
    pass

    
